'''
MIT License

Copyright (c) 2024 Ken Thompson, https://github.com/KennethThompson, all rights reserved.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

from dataclasses import dataclass
from typing import Optional, Union
import aiohttp
import logging
from uspto_odp.models.patent_file_wrapper import PatentFileWrapper
from uspto_odp.models.patent_documents import PatentDocumentCollection, PatentDocument
from uspto_odp.models.patent_continuity import ContinuityCollection
from uspto_odp.models.foreign_priority import ForeignPriorityCollection
from uspto_odp.models.patent_transactions import TransactionCollection
from uspto_odp.models.patent_assignment import AssignmentCollection
from uspto_odp.models.patent_status_codes import StatusCodeCollection
from uspto_odp.models.patent_metadata import ApplicationMetadataResponse
from uspto_odp.models.patent_attorney import AttorneyResponse
from uspto_odp.models.patent_adjustment import AdjustmentResponse
from uspto_odp.models.patent_associated_documents import AssociatedDocumentsResponse
from uspto_odp.models.patent_search_download import PatentDataResponse
import os
import re
try:
    from enum import StrEnum  # Python 3.11+
except ImportError:
    from strenum import StrEnum  # Python 3.9+

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class USPTOError(Exception):
    """Exception for USPTO API errors."""
    def __init__(self, code: int, error: str, error_details: Optional[str] = None, request_identifier: Optional[str] = None):
        self.code = code
        self.error = error
        self.error_details = error_details
        self.request_identifier = request_identifier
        super().__init__(f"{code}: {error} - {error_details or 'No details provided'}")

    @classmethod
    def from_dict(cls, data: dict, status_code: int) -> 'USPTOError':
        default_messages = {
            400: "Bad Request",
            403: "Forbidden",
            404: "Not Found",
            500: "Internal Server Error"
        }
        return cls(
            code=data.get('code', status_code),
            error=data.get('error', default_messages.get(status_code, "Unknown Error")),
            error_details=data.get('errorDetails') or data.get('errorDetailed'),
            request_identifier=data.get('requestIdentifier')
        )

class USPTOClient:
    """Async client for USPTO Patent Application API"""
    
    BASE_API_URL = "https://api.uspto.gov/api"

    def __init__(self, api_key: str, session: Optional[aiohttp.ClientSession] = None):
        self.API_KEY = api_key
        self.headers = {
            "accept": "application/json",
            "X-API-KEY": self.API_KEY
        }
        self.session = session or aiohttp.ClientSession()

    @property
    def _patent_applications_endpoint(self) -> str:
        """
        Patent Applications service endpoint.
        Base path: /v1/patent/applications
        """
        return f"{self.BASE_API_URL}/v1/patent/applications"

    @property
    def _bulk_data_endpoint(self) -> str:
        """
        Bulk Data service endpoint (for future implementation).
        Base path: /v1/bulkdata
        """
        return f"{self.BASE_API_URL}/v1/bulkdata"

    @property
    def _petition_decisions_endpoint(self) -> str:
        """
        Petition Decisions service endpoint (for future implementation).
        Base path: /v1/petitions/decisions
        """
        return f"{self.BASE_API_URL}/v1/petitions/decisions"

    @property
    def _ptab_trials_endpoint(self) -> str:
        """
        PTAB Trials service endpoint (for future implementation).
        Base path: /v1/ptab/trials
        """
        return f"{self.BASE_API_URL}/v1/ptab/trials"

    @property
    def _status_codes_endpoint(self) -> str:
        """
        Status Codes service endpoint.
        Base path: /v1/patent/status-codes
        """
        return f"{self.BASE_API_URL}/v1/patent/status-codes"

    def _build_url(self, service_endpoint: str, *path_segments: str) -> str:
        """
        Build a full URL from a service endpoint and additional path segments.
        
        Args:
            service_endpoint: The base service endpoint (e.g., from _patent_applications_endpoint)
            *path_segments: Additional path segments to append
            
        Returns:
            str: Complete URL
            
        Example:
            url = self._build_url(self._patent_applications_endpoint, "12345678", "documents")
            # Returns: https://api.uspto.gov/api/v1/patent/applications/12345678/documents
        """
        path = "/".join(str(segment) for segment in path_segments if segment)
        if path:
            return f"{service_endpoint}/{path}"
        return service_endpoint

    async def _handle_response(self, response, parse_func):
        try:
            data = await response.json()
        except Exception:
            data = {}
        
        if response.status == 200:
            return parse_func(data)
        
        error = USPTOError.from_dict(data, response.status)
        self._log_error(error)
        raise error

    def _log_error(self, error: USPTOError):
        logger.error(
            f"USPTO API Error: {error.code}\n"
            f"Error Message: {error.error}\n"
            f"Details: {error.error_details or 'No details provided'}\n"
            f"Request ID: {error.request_identifier or 'No request ID provided'}"
        )

    async def get_patent_wrapper(self, serial_number: str) -> PatentFileWrapper:
        """
        Retrieve the patent application wrapper information.

        Args:
            serial_number (str): The USPTO patent application serial number (e.g., '16123456' or 'PCTUS2004027676')
                               If a non-PCT number starts with 'US', it will be stripped (e.g., 'US0506853' -> '0506853')

        Returns:
            PatentFileWrapper: Object containing patent wrapper information

        Raises:
            USPTOError: If the API request fails
        """
        # Strip 'US' prefix from non-PCT application numbers
        if serial_number.startswith('US'):
            serial_number = serial_number[2:]

        # Check if this is a PCT application number
        if serial_number.startswith('PCT'):
            # Pattern to match PCT numbers and extract country code, year and remaining digits
            # Group 1: Country code (US|IB|AU)
            # Group 2: Year (2 digits, optionally prefixed with 20)
            # Group 3: Remaining digits
            pct_pattern = r'PCT(US|IB|AU)?(?:20)?(\d{2})(\d+)'
            match = re.match(pct_pattern, serial_number)
            
            if match:
                country, year, number = match.groups()
                # Use US as default if no country code
                country = country or 'US'
                # First try with original number
                standardized = f"PCT{country}{year}{number}"
                
                try:
                    url = self._build_url(self._patent_applications_endpoint, standardized)
                    async with self.session.get(url, headers=self.headers) as response:
                        if response.status == 404 and number.startswith('0'):
                            # If 404 and has leading zero, try without it
                            number_no_zero = str(int(number))
                            standardized = f"PCT{country}{year}{number_no_zero}"
                            url = self._build_url(self._patent_applications_endpoint, standardized)
                            async with self.session.get(url, headers=self.headers) as retry_response:
                                return await self._handle_response(retry_response, PatentFileWrapper.parse_response)
                        return await self._handle_response(response, PatentFileWrapper.parse_response)
                except Exception as e:
                    # If any error occurs during retry, raise the original error
                    raise e
            else:
                raise ValueError(f"Invalid PCT application number format: {serial_number}")
        
        url = self._build_url(self._patent_applications_endpoint, serial_number)
        async with self.session.get(url, headers=self.headers) as response:
            return await self._handle_response(response, PatentFileWrapper.parse_response)

    async def get_patent_documents(self, serial_number: str) -> PatentDocumentCollection:
        """
        Retrieve all documents associated with a patent application.

        Args:
            serial_number (str): The USPTO patent application serial number (e.g., '16123456')

        Returns:
            PatentDocumentCollection: Collection of patent documents

        Raises:
            USPTOError: If the API request fails
        """
        url = self._build_url(self._patent_applications_endpoint, serial_number, "documents")
        async with self.session.get(url, headers=self.headers) as response:
            return await self._handle_response(response, PatentDocumentCollection.from_dict)

    async def download_document(
        self, 
        document: PatentDocument, 
        save_path: str,
        filename: Optional[str] = None,
        mime_type: str = "PDF"
    ) -> str:
        """
        Download a specific patent document to local storage.

        Args:
            document (PatentDocument): The patent document object to download
            save_path (str): Directory path where the file should be saved
            filename (Optional[str]): Custom filename for the downloaded document. 
                                    If None, generates automatic filename
            mime_type (str): Document format to download. Options: "PDF", "MS_WORD", "XML"

        Returns:
            str: Full path to the downloaded file

        Raises:
            FileNotFoundError: If save_path doesn't exist
            PermissionError: If save_path isn't writable
            ValueError: If requested mime_type isn't available
            USPTOError: If the API request fails
            Exception: If download fails
        """
        if not os.path.exists(save_path):
            raise FileNotFoundError(f"Save path does not exist: {save_path}")
        if not os.access(save_path, os.W_OK):
            raise PermissionError(f"Save path is not writable: {save_path}")
            
        download_option = next(
            (opt for opt in document.download_options if opt.mime_type == mime_type),
            None
        )
        
        if not download_option:
            available_types = [opt.mime_type for opt in document.download_options]
            raise ValueError(
                f"Mime type '{mime_type}' not available for this document. "
                f"Available types: {', '.join(available_types)}"
            )
            
        if not filename:
            extension = ".pdf" if mime_type == "PDF" else ".doc" if mime_type == "MS_WORD" else ".xml"
            filename = f"{document.application_number}_{document.document_code}_{document.document_identifier}{extension}"
            
        full_path = os.path.join(save_path, filename)
        
        async with self.session.get(download_option.download_url, headers=self.headers) as response:
            if response.status != 200:
                raise Exception(f"Download failed with status {response.status}")
                
            with open(full_path, 'wb') as f:
                while True:
                    chunk = await response.content.read(8192)
                    if not chunk:
                        break
                    f.write(chunk)
                        
        logger.info(
            f"Successfully downloaded document {document.document_identifier} "
            f"({mime_type}) to {full_path}"
        )
        
        return full_path

    async def get_continuity(self, serial_number: str) -> ContinuityCollection:
        """
        Retrieve continuity information for a patent application.

        Args:
            serial_number (str): The USPTO patent application serial number (e.g., '16123456')

        Returns:
            ContinuityCollection: Collection of continuity relationships

        Raises:
            USPTOError: If the API request fails
        """
        url = self._build_url(self._patent_applications_endpoint, serial_number, "continuity")
        async with self.session.get(url, headers=self.headers) as response:
            return await self._handle_response(response, ContinuityCollection.from_dict)

    async def get_foreign_priority(self, serial_number: str) -> ForeignPriorityCollection:
        """
        Retrieve foreign priority claims for a patent application.

        Args:
            serial_number (str): The USPTO patent application serial number (e.g., '16123456')

        Returns:
            ForeignPriorityCollection: Collection of foreign priority claims

        Raises:
            USPTOError: If the API request fails
        """
        url = self._build_url(self._patent_applications_endpoint, serial_number, "foreign-priority")
        async with self.session.get(url, headers=self.headers) as response:
            return await self._handle_response(response, ForeignPriorityCollection.from_dict)

    async def get_patent_transactions(self, serial_number: str) -> TransactionCollection:
        """
        Retrieve transaction history for a patent application.

        Args:
            serial_number (str): The USPTO patent application serial number (e.g., '16123456')

        Returns:
            TransactionCollection: Collection of patent transactions

        Raises:
            USPTOError: If the API request fails
        """
        url = self._build_url(self._patent_applications_endpoint, serial_number, "transactions")
        async with self.session.get(url, headers=self.headers) as response:
            return await self._handle_response(response, TransactionCollection.from_dict)

    async def get_patent_assignments(self, serial_number: str) -> AssignmentCollection:
        """
        Retrieve assignment information for a patent application.

        Args:
            serial_number (str): The USPTO patent application serial number (e.g., '16123456')

        Returns:
            AssignmentCollection: Collection of patent assignments

        Raises:
            USPTOError: If the API request fails
        """
        url = self._build_url(self._patent_applications_endpoint, serial_number, "assignment")
        async with self.session.get(url, headers=self.headers) as response:
            return await self._handle_response(response, AssignmentCollection.from_dict)

    async def get_attorney(self, serial_number: str) -> AttorneyResponse:
        """
        Retrieve attorney/agent information for a patent application.

        Args:
            serial_number (str): The USPTO patent application serial number (e.g., '16123456')

        Returns:
            AttorneyResponse: Attorney/agent data for the application

        Raises:
            USPTOError: If the API request fails
        """
        url = self._build_url(self._patent_applications_endpoint, serial_number, "attorney")
        async with self.session.get(url, headers=self.headers) as response:
            return await self._handle_response(response, AttorneyResponse.from_dict)

    async def get_adjustment(self, serial_number: str) -> AdjustmentResponse:
        """
        Retrieve patent term adjustment information for a patent application.

        Args:
            serial_number (str): The USPTO patent application serial number (e.g., '16123456')

        Returns:
            AdjustmentResponse: Patent term adjustment data for the application

        Raises:
            USPTOError: If the API request fails
        """
        url = self._build_url(self._patent_applications_endpoint, serial_number, "adjustment")
        async with self.session.get(url, headers=self.headers) as response:
            return await self._handle_response(response, AdjustmentResponse.from_dict)

    async def get_associated_documents(self, serial_number: str) -> AssociatedDocumentsResponse:
        """
        Retrieve associated documents (PGPub and Grant) metadata for a patent application.

        Args:
            serial_number (str): The USPTO patent application serial number (e.g., '16123456')

        Returns:
            AssociatedDocumentsResponse: Associated documents metadata for the application

        Raises:
            USPTOError: If the API request fails
        """
        url = self._build_url(self._patent_applications_endpoint, serial_number, "associated-documents")
        async with self.session.get(url, headers=self.headers) as response:
            return await self._handle_response(response, AssociatedDocumentsResponse.from_dict)

    async def search_patent_applications(self, payload: dict) -> dict:
        """
        Search for patent applications using a JSON payload (POST method).

        Endpoint: POST /api/v1/patent/applications/search

        Args:
            payload (dict): The search criteria as a JSON-compatible dictionary.
                           Can include fields like query text, sort options, filters, etc.

        Returns:
            dict: The search results as returned by the USPTO API

        Raises:
            USPTOError: If the API request fails (400, 403, 404, 413, 500)
        """
        url = self._build_url(self._patent_applications_endpoint, "search")
        async with self.session.post(url, json=payload, headers=self.headers) as response:
            return await self._handle_response(response, lambda x: x)  # Return raw JSON response

    async def search_patent_applications_get(
        self,
        q: Optional[str] = None,
        sort: Optional[str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        facets: Optional[str] = None,
        fields: Optional[str] = None,
        filters: Optional[str] = None,
        range_filters: Optional[str] = None
    ) -> dict:
        """
        Search for patent applications using query parameters (GET method).

        Endpoint: GET /api/v1/patent/applications/search

        Args:
            q (str, optional): Search query string. Accepts boolean operators (AND, OR, NOT),
                              wildcards (*), and exact phrases (""). Example: 'applicationNumberText:14412875'
            sort (str, optional): Field to sort by followed by order. Example: 'applicationMetaData.filingDate asc'
            offset (int, optional): Position in dataset to start from. Default: 0
            limit (int, optional): Number of results to return. Default: 25
            facets (str, optional): Comma-separated list of fields to facet.
                                   Example: 'applicationMetaData.applicationTypeCode,applicationMetaData.docketNumber'
            fields (str, optional): Comma-separated list of fields to include in response.
                                   Example: 'applicationNumberText,applicationMetaData.patentNumber'
            filters (str, optional): Filter by field value. Format: 'fieldName value1,value2'
                                    Example: 'applicationMetaData.applicationTypeCode UTL,DES'
            range_filters (str, optional): Filter by range. Format: 'fieldName min:max'
                                          Example: 'applicationMetaData.grantDate 2010-01-01:2011-01-01'

        Returns:
            dict: The search results as returned by the USPTO API

        Raises:
            USPTOError: If the API request fails (400, 403, 404, 413, 500)

        Examples:
            # Search by application number
            results = await client.search_patent_applications_get(q='applicationNumberText:14412875')

            # Search with pagination
            results = await client.search_patent_applications_get(q='Utility', limit=50, offset=0)

            # Complex search with sorting and filtering
            results = await client.search_patent_applications_get(
                q='applicationMetaData.inventorBag.inventorNameText:Smith',
                sort='applicationMetaData.filingDate desc',
                filters='applicationMetaData.applicationTypeCode UTL',
                limit=100
            )
        """
        url = self._build_url(self._patent_applications_endpoint, "search")

        # Build query parameters, only including non-None values
        params = {}
        if q is not None:
            params['q'] = q
        if sort is not None:
            params['sort'] = sort
        if offset is not None:
            params['offset'] = offset
        if limit is not None:
            params['limit'] = limit
        if facets is not None:
            params['facets'] = facets
        if fields is not None:
            params['fields'] = fields
        if filters is not None:
            params['filters'] = filters
        if range_filters is not None:
            params['rangeFilters'] = range_filters

        async with self.session.get(url, params=params, headers=self.headers) as response:
            return await self._handle_response(response, lambda x: x)  # Return raw JSON response

    async def search_patent_applications_download(self, payload: dict) -> PatentDataResponse:
        """
        Download patent application search results using a JSON payload (POST method).

        Endpoint: POST /api/v1/patent/applications/search/download

        This endpoint is similar to search_patent_applications but optimized for downloads.

        Args:
            payload (dict): The search criteria as a JSON-compatible dictionary.
                           Can include fields like query text, sort options, filters, etc.

        Returns:
            PatentDataResponse: The download response containing search results

        Raises:
            USPTOError: If the API request fails (400, 403, 404, 413, 500)
        """
        url = self._build_url(self._patent_applications_endpoint, "search", "download")
        async with self.session.post(url, json=payload, headers=self.headers) as response:
            return await self._handle_response(response, PatentDataResponse.from_dict)

    async def search_patent_applications_download_get(
        self,
        q: Optional[str] = None,
        sort: Optional[str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        facets: Optional[str] = None,
        fields: Optional[str] = None,
        filters: Optional[str] = None,
        range_filters: Optional[str] = None,
        format: Optional[str] = None
    ) -> PatentDataResponse:
        """
        Download patent application search results using query parameters (GET method).

        Endpoint: GET /api/v1/patent/applications/search/download

        This endpoint is similar to search_patent_applications_get but optimized for downloads.
        Supports a format parameter for download format (json or csv).

        Args:
            q (str, optional): Search query string. Accepts boolean operators (AND, OR, NOT),
                              wildcards (*), and exact phrases (""). Example: 'applicationNumberText:14412875'
            sort (str, optional): Field to sort by followed by order. Example: 'applicationMetaData.filingDate asc'
            offset (int, optional): Position in dataset to start from. Default: 0
            limit (int, optional): Number of results to return. Default: 25
            facets (str, optional): Comma-separated list of fields to facet.
                                   Example: 'applicationMetaData.applicationTypeCode,applicationMetaData.docketNumber'
            fields (str, optional): Comma-separated list of fields to include in response.
                                   Example: 'applicationNumberText,applicationMetaData.patentNumber'
            filters (str, optional): Filter by field value. Format: 'fieldName value1,value2'
                                    Example: 'applicationMetaData.applicationTypeCode UTL,DES'
            range_filters (str, optional): Filter by range. Format: 'fieldName min:max'
                                          Example: 'applicationMetaData.grantDate 2010-01-01:2011-01-01'
            format (str, optional): Download format. Options: 'json' or 'csv'. Default: 'json'

        Returns:
            PatentDataResponse: The download response containing search results

        Raises:
            USPTOError: If the API request fails (400, 403, 404, 413, 500)

        Examples:
            # Download search results in JSON format
            results = await client.search_patent_applications_download_get(q='applicationNumberText:14412875', format='json')

            # Download search results in CSV format
            results = await client.search_patent_applications_download_get(q='Utility', format='csv', limit=100)
        """
        url = self._build_url(self._patent_applications_endpoint, "search", "download")
        params = {}
        if q is not None:
            params['q'] = q
        if sort is not None:
            params['sort'] = sort
        if offset is not None:
            params['offset'] = offset
        if limit is not None:
            params['limit'] = limit
        if facets is not None:
            params['facets'] = facets
        if fields is not None:
            params['fields'] = fields
        if filters is not None:
            params['filters'] = filters
        if range_filters is not None:
            params['rangeFilters'] = range_filters
        if format is not None:
            params['format'] = format

        async with self.session.get(url, params=params, headers=self.headers) as response:
            return await self._handle_response(response, PatentDataResponse.from_dict)

    async def get_app_metadata(self, application_number: str) -> ApplicationMetadataResponse:
        """
        Get application metadata directly from the /meta-data endpoint using an application number.
        
        This is the direct implementation of the /api/v1/patent/applications/{applicationNumberText}/meta-data endpoint.
        
        Args:
            application_number (str): The application number (e.g., "14412875" or "14/412,875")
            
        Returns:
            ApplicationMetadataResponse: The application metadata response containing application number and metadata
            
        Raises:
            USPTOError: If the API request fails (e.g., 404 if application not found)
        """
        # Build URL for the meta-data endpoint: /api/v1/patent/applications/{applicationNumberText}/meta-data
        url = self._build_url(self._patent_applications_endpoint, application_number, "meta-data")
        
        async with self.session.get(url, headers=self.headers) as response:
            return await self._handle_response(response, ApplicationMetadataResponse.from_dict)

    async def get_app_metadata_from_patent_number(self, patent_number: str) -> Optional[ApplicationMetadataResponse]:
        """
        Get the application metadata associated with a patent number.
        
        This method searches for the application number using the patent number, then calls
        the direct meta-data endpoint. This is a convenience method for users who have a patent
        number but need the application metadata.
        
        Args:
            patent_number (str): The patent number to search for (e.g., "US9,022,434" or "9022434")
            
        Returns:
            Optional[ApplicationMetadataResponse]: The application metadata if found, None otherwise
            
        Raises:
            USPTOError: If the API request fails
        """
        # Sanitize the patent number by removing "US" prefix and any non-digit characters
        sanitized_patent = ''.join(c for c in patent_number if c.isdigit())
        
        # Create the search payload to find the application number from the patent number
        payload = {
            "q" : "applicationMetaData.patentNumber:" + sanitized_patent,
            "filters": [
                {
                    "name": "applicationMetaData.applicationTypeLabelName",
                    "value": ["Utility"]
                },
                {
                    "name": "applicationMetaData.publicationCategoryBag",
                    "value": ["Granted/Issued"]
                }
            ],
            "sort": [
                {
                    "field": "applicationMetaData.filingDate",
                    "order": "desc"
                }
            ],
            "pagination": {
                "offset": 0,
                "limit": 25
            },
            "fields": ["applicationNumberText", "applicationMetaData"],
            "facets": [
                "applicationMetaData.applicationTypeLabelName"
            ]        
        }
        
        # Make the search request to find the application number
        response = await self.search_patent_applications(payload)
        
        # Check if we got results
        if response.get('count', 0) > 0 and 'patentFileWrapperDataBag' in response:
            # Extract the application number from the first result
            application_number = response['patentFileWrapperDataBag'][0].get('applicationNumberText')
            
            if application_number:
                # Use the direct meta-data endpoint with the found application number
                return await self.get_app_metadata(application_number)
        
        return None

    async def search_status_codes_get(
        self,
        q: Optional[str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None
    ) -> StatusCodeCollection:
        """
        Search for patent application status codes using query parameters (GET method).

        Endpoint: GET /api/v1/patent/status-codes

        Args:
            q (str, optional): Search query string. Accepts boolean operators (AND, OR, NOT),
                              wildcards (*), and exact phrases (""). 
                              Example: 'applicationStatusDescriptionText:Preexam'
            offset (int, optional): Position in dataset to start from. Default: 0
            limit (int, optional): Number of results to return. Default: 25

        Returns:
            StatusCodeCollection: Collection of status codes matching the search criteria

        Raises:
            USPTOError: If the API request fails (400, 403, 404, 500)

        Examples:
            # Search by status description
            result = await client.search_status_codes_get(q='applicationStatusDescriptionText:Preexam')

            # Search with comparison operator
            result = await client.search_status_codes_get(q='applicationStatusCode:>100', limit=50)

            # Search with pagination
            result = await client.search_status_codes_get(q='Application AND Preexam', limit=10, offset=0)
        """
        url = self._build_url(self._status_codes_endpoint)

        # Build query parameters, only including non-None values
        params = {}
        if q is not None:
            params['q'] = q
        if offset is not None:
            params['offset'] = offset
        if limit is not None:
            params['limit'] = limit

        async with self.session.get(url, params=params, headers=self.headers) as response:
            return await self._handle_response(response, StatusCodeCollection.from_dict)

    async def search_status_codes(self, payload: dict) -> StatusCodeCollection:
        """
        Search for patent application status codes using a JSON payload (POST method).

        Endpoint: POST /api/v1/patent/status-codes

        Args:
            payload (dict): The search criteria as a JSON-compatible dictionary.
                           Can include fields like query text, pagination, etc.
                           All fields in the request are optional.

        Returns:
            StatusCodeCollection: Collection of status codes matching the search criteria

        Raises:
            USPTOError: If the API request fails (400, 403, 404, 500)

        Example:
            payload = {
                "q": "applicationStatusCode:>100",
                "pagination": {
                    "offset": 0,
                    "limit": 25
                }
            }
            result = await client.search_status_codes(payload)
        """
        url = self._build_url(self._status_codes_endpoint)
        async with self.session.post(url, json=payload, headers=self.headers) as response:
            return await self._handle_response(response, StatusCodeCollection.from_dict)
