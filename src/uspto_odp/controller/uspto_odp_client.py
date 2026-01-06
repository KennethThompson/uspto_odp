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
from uspto_odp.models.patent_petition_decision import PetitionDecisionResponseBag, PetitionDecisionIdentifierResponseBag
from uspto_odp.models.patent_trials_proceedings import TrialProceedingResponseBag, TrialProceedingIdentifierResponseBag
from uspto_odp.models.patent_trials_decisions import TrialDecisionResponseBag, TrialDecisionIdentifierResponseBag, TrialDecisionByTrialResponseBag
from uspto_odp.models.patent_trials_documents import TrialDocumentResponseBag, TrialDocumentIdentifierResponseBag, TrialDocumentByTrialResponseBag
from uspto_odp.models.patent_appeals_decisions import AppealDecisionResponseBag, AppealDecisionIdentifierResponseBag, AppealDecisionByAppealResponseBag
from uspto_odp.models.patent_interferences_decisions import InterferenceDecisionResponseBag, InterferenceDecisionIdentifierResponseBag, InterferenceDecisionByInterferenceResponseBag
from uspto_odp.models.bulk_datasets import DatasetProductSearchResponseBag, DatasetProductResponseBag, DatasetFileResponseBag
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
    def _bulk_datasets_endpoint(self) -> str:
        """
        Bulk Datasets service endpoint.
        Base path: /v1/datasets/products
        """
        return f"{self.BASE_API_URL}/v1/datasets/products"

    @property
    def _petition_decisions_endpoint(self) -> str:
        """
        Petition Decisions service endpoint.
        Base path: /v1/petition/decisions
        """
        return f"{self.BASE_API_URL}/v1/petition/decisions"

    @property
    def _ptab_trials_endpoint(self) -> str:
        """
        PTAB Trials service endpoint (for future implementation).
        Base path: /v1/ptab/trials
        """
        return f"{self.BASE_API_URL}/v1/ptab/trials"

    @property
    def _ptab_trials_proceedings_endpoint(self) -> str:
        """
        PTAB Trials Proceedings service endpoint.
        Base path: /v1/patent/trials/proceedings
        """
        return f"{self.BASE_API_URL}/v1/patent/trials/proceedings"

    @property
    def _ptab_trials_decisions_endpoint(self) -> str:
        """
        PTAB Trials Decisions service endpoint.
        Base path: /v1/patent/trials/decisions
        """
        return f"{self.BASE_API_URL}/v1/patent/trials/decisions"

    @property
    def _ptab_trials_documents_endpoint(self) -> str:
        """
        PTAB Trials Documents service endpoint.
        Base path: /v1/patent/trials/documents
        """
        return f"{self.BASE_API_URL}/v1/patent/trials/documents"

    @property
    def _ptab_appeals_decisions_endpoint(self) -> str:
        """
        PTAB Appeals Decisions service endpoint.
        Base path: /v1/patent/appeals/decisions
        """
        return f"{self.BASE_API_URL}/v1/patent/appeals/decisions"

    @property
    def _ptab_interferences_decisions_endpoint(self) -> str:
        """
        PTAB Interferences Decisions service endpoint.
        Base path: /v1/patent/interferences/decisions
        """
        return f"{self.BASE_API_URL}/v1/patent/interferences/decisions"

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

    async def get_patent_documents(
        self, 
        serial_number: str,
        official_date_from: Optional[str] = None,
        official_date_to: Optional[str] = None,
        document_codes: Optional[str] = None
    ) -> PatentDocumentCollection:
        """
        Retrieve all documents associated with a patent application.

        Args:
            serial_number (str): The USPTO patent application serial number (e.g., '16123456')
            official_date_from (str, optional): Filter documents by official date from. 
                                               Format: 'yyyy-MM-dd' (e.g., '2023-01-01')
            official_date_to (str, optional): Filter documents by official date to. 
                                             Format: 'yyyy-MM-dd' (e.g., '2023-12-31')
            document_codes (str, optional): Filter by document codes. Single code or comma-separated 
                                           codes (e.g., 'WFEE' or 'SRFW,SRNT')

        Returns:
            PatentDocumentCollection: Collection of patent documents

        Raises:
            USPTOError: If the API request fails

        Examples:
            # Get all documents
            documents = await client.get_patent_documents("18571476")
            
            # Filter by date range
            documents = await client.get_patent_documents(
                "18571476",
                official_date_from="2023-01-01",
                official_date_to="2023-12-31"
            )
            
            # Filter by document codes
            documents = await client.get_patent_documents(
                "18571476",
                document_codes="WFEE"
            )
            
            # Combine filters
            documents = await client.get_patent_documents(
                "18571476",
                official_date_from="2023-01-01",
                official_date_to="2023-12-31",
                document_codes="SRFW,SRNT"
            )
        """
        url = self._build_url(self._patent_applications_endpoint, serial_number, "documents")
        
        # Build query parameters, only including non-None values
        params = {}
        if official_date_from is not None:
            params['officialDateFrom'] = official_date_from
        if official_date_to is not None:
            params['officialDateTo'] = official_date_to
        if document_codes is not None:
            params['documentCodes'] = document_codes
        
        async with self.session.get(url, params=params, headers=self.headers) as response:
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
            
            # Complex search by partial docket number and customer number with specific fields
            # This example searches for docket numbers beginning with "3NG" AND customerNumber 51886,
            # returns only specified fields, sorted by filing date descending
            results = await client.search_patent_applications_get(
                q='applicationMetaData.docketNumber:3NG* AND applicationMetaData.customerNumber:51886',
                fields='applicationNumberText,applicationMetaData.inventionTitle,applicationMetaData.patentNumber,applicationMetaData.filingDate,applicationMetaData.docketNumber',
                sort='applicationMetaData.filingDate desc',
                limit=50,
                offset=0
            )
            # Expected response includes:
            # - count: total number of matching results
            # - patentFileWrapperDataBag: array of applications with requested fields
            # - Each application includes: applicationNumberText and applicationMetaData with
            #   inventionTitle, patentNumber, filingDate, and docketNumber fields
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

    async def search_petition_decisions(self, payload: dict) -> PetitionDecisionResponseBag:
        """
        Search petition decisions using a JSON payload (POST method).

        Endpoint: POST /api/v1/petition/decisions/search

        Args:
            payload (dict): The search criteria as a JSON-compatible dictionary.
                           Can include fields like query text, sort options, filters, pagination, etc.

        Returns:
            PetitionDecisionResponseBag: The search response containing petition decision results

        Raises:
            USPTOError: If the API request fails (400, 403, 404, 500)
        """
        url = self._build_url(self._petition_decisions_endpoint, "search")
        async with self.session.post(url, json=payload, headers=self.headers) as response:
            return await self._handle_response(response, PetitionDecisionResponseBag.from_dict)

    async def search_petition_decisions_get(
        self,
        q: Optional[str] = None,
        sort: Optional[str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        facets: Optional[str] = None,
        fields: Optional[str] = None,
        filters: Optional[str] = None,
        range_filters: Optional[str] = None
    ) -> PetitionDecisionResponseBag:
        """
        Search petition decisions using query parameters (GET method).

        Endpoint: GET /api/v1/petition/decisions/search

        Args:
            q (str, optional): Search query string. Accepts boolean operators (AND, OR, NOT),
                              wildcards (*), and exact phrases (""). Example: 'decisionTypeCodeDescriptionText:Denied'
            sort (str, optional): Field to sort by followed by order. Example: 'petitionMailDate desc'
            offset (int, optional): Position in dataset to start from. Default: 0
            limit (int, optional): Number of results to return. Default: 25
            facets (str, optional): Comma-separated list of fields to facet.
            fields (str, optional): Comma-separated list of fields to include in response.
            filters (str, optional): Filter by field value. Format: 'fieldName value1,value2'
            range_filters (str, optional): Filter by range. Format: 'fieldName min:max'
                                          Example: 'petitionMailDate 2021-01-01:2025-01-01'

        Returns:
            PetitionDecisionResponseBag: The search response containing petition decision results

        Raises:
            USPTOError: If the API request fails (400, 403, 404, 500)

        Examples:
            # Search for denied decisions
            results = await client.search_petition_decisions_get(q='decisionTypeCodeDescriptionText:Denied')

            # Search with filters and pagination
            results = await client.search_petition_decisions_get(
                q='Denied',
                filters='businessEntityStatusCategory Small',
                limit=50,
                offset=0
            )
        """
        url = self._build_url(self._petition_decisions_endpoint, "search")
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
            return await self._handle_response(response, PetitionDecisionResponseBag.from_dict)

    async def search_petition_decisions_download(self, payload: dict) -> PetitionDecisionResponseBag:
        """
        Download petition decision search results using a JSON payload (POST method).

        Endpoint: POST /api/v1/petition/decisions/search/download

        This endpoint is similar to search_petition_decisions but optimized for downloads.

        Args:
            payload (dict): The search criteria as a JSON-compatible dictionary.

        Returns:
            PetitionDecisionResponseBag: The download response containing search results

        Raises:
            USPTOError: If the API request fails (400, 403, 404, 500)
        """
        url = self._build_url(self._petition_decisions_endpoint, "search", "download")
        async with self.session.post(url, json=payload, headers=self.headers) as response:
            return await self._handle_response(response, PetitionDecisionResponseBag.from_dict)

    async def search_petition_decisions_download_get(
        self,
        q: Optional[str] = None,
        sort: Optional[str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        fields: Optional[str] = None,
        filters: Optional[str] = None,
        range_filters: Optional[str] = None,
        format: Optional[str] = None
    ) -> PetitionDecisionResponseBag:
        """
        Download petition decision search results using query parameters (GET method).

        Endpoint: GET /api/v1/petition/decisions/search/download

        This endpoint is similar to search_petition_decisions_get but optimized for downloads.
        Supports a format parameter for download format (json or csv).

        Args:
            q (str, optional): Search query string.
            sort (str, optional): Field to sort by followed by order.
            offset (int, optional): Position in dataset to start from. Default: 0
            limit (int, optional): Number of results to return. Default: 25
            fields (str, optional): Comma-separated list of fields to include in response.
            filters (str, optional): Filter by field value. Format: 'fieldName value1,value2'
            range_filters (str, optional): Filter by range. Format: 'fieldName min:max'
            format (str, optional): Download format. Options: 'json' or 'csv'. Default: 'json'

        Returns:
            PetitionDecisionResponseBag: The download response containing search results

        Raises:
            USPTOError: If the API request fails (400, 403, 404, 500)

        Examples:
            # Download search results in JSON format
            results = await client.search_petition_decisions_download_get(q='Denied', format='json')

            # Download search results in CSV format
            results = await client.search_petition_decisions_download_get(q='Denied', format='csv', limit=100)
        """
        url = self._build_url(self._petition_decisions_endpoint, "search", "download")
        params = {}
        if q is not None:
            params['q'] = q
        if sort is not None:
            params['sort'] = sort
        if offset is not None:
            params['offset'] = offset
        if limit is not None:
            params['limit'] = limit
        if fields is not None:
            params['fields'] = fields
        if filters is not None:
            params['filters'] = filters
        if range_filters is not None:
            params['rangeFilters'] = range_filters
        if format is not None:
            params['format'] = format

        async with self.session.get(url, params=params, headers=self.headers) as response:
            return await self._handle_response(response, PetitionDecisionResponseBag.from_dict)

    async def get_petition_decision(
        self,
        petition_decision_record_identifier: str,
        include_documents: bool = False
    ) -> PetitionDecisionIdentifierResponseBag:
        """
        Retrieve a specific petition decision by its record identifier.

        Endpoint: GET /api/v1/petition/decisions/{petitionDecisionRecordIdentifier}

        Args:
            petition_decision_record_identifier (str): The petition decision record identifier (UUID format)
            include_documents (bool, optional): Whether to include petition decision documents in the response.
                                               Default: False

        Returns:
            PetitionDecisionIdentifierResponseBag: The petition decision data

        Raises:
            USPTOError: If the API request fails (400, 403, 404, 500)

        Examples:
            # Get petition decision without documents
            decision = await client.get_petition_decision('6779f1be-0f3b-5775-b9d3-dcfdb83171c3')

            # Get petition decision with documents
            decision = await client.get_petition_decision('6779f1be-0f3b-5775-b9d3-dcfdb83171c3', include_documents=True)
        """
        url = self._build_url(self._petition_decisions_endpoint, petition_decision_record_identifier)
        params = {}
        if include_documents:
            params['includeDocuments'] = 'true'
        else:
            params['includeDocuments'] = 'false'

        async with self.session.get(url, params=params, headers=self.headers) as response:
            return await self._handle_response(response, PetitionDecisionIdentifierResponseBag.from_dict)

    async def search_trial_proceedings(self, payload: dict) -> TrialProceedingResponseBag:
        """
        Search trial proceedings using a JSON payload (POST method).

        Endpoint: POST /api/v1/patent/trials/proceedings/search

        Args:
            payload (dict): The search criteria as a JSON-compatible dictionary.
                           Can include fields like query text, sort options, filters, pagination, etc.

        Returns:
            TrialProceedingResponseBag: The search response containing trial proceeding results

        Raises:
            USPTOError: If the API request fails (400, 403, 404, 500)
        """
        url = self._build_url(self._ptab_trials_proceedings_endpoint, "search")
        async with self.session.post(url, json=payload, headers=self.headers) as response:
            return await self._handle_response(response, TrialProceedingResponseBag.from_dict)

    async def search_trial_proceedings_get(
        self,
        q: Optional[str] = None,
        sort: Optional[str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        facets: Optional[str] = None,
        fields: Optional[str] = None,
        filters: Optional[str] = None,
        range_filters: Optional[str] = None
    ) -> TrialProceedingResponseBag:
        """
        Search trial proceedings using query parameters (GET method).

        Endpoint: GET /api/v1/patent/trials/proceedings/search

        Args:
            q (str, optional): Search query string. Accepts boolean operators (AND, OR, NOT),
                              wildcards (*), and exact phrases (""). Example: 'trialType:IPR'
            sort (str, optional): Field to sort by followed by order. Example: 'filingDate desc'
            offset (int, optional): Position in dataset to start from. Default: 0
            limit (int, optional): Number of results to return. Default: 25
            facets (str, optional): Comma-separated list of fields to facet.
            fields (str, optional): Comma-separated list of fields to include in response.
            filters (str, optional): Filter by field value. Format: 'fieldName value1,value2'
            range_filters (str, optional): Filter by range. Format: 'fieldName min:max'
                                          Example: 'filingDate 2021-01-01:2025-01-01'

        Returns:
            TrialProceedingResponseBag: The search response containing trial proceeding results

        Raises:
            USPTOError: If the API request fails (400, 403, 404, 500)

        Examples:
            # Search for IPR trials
            results = await client.search_trial_proceedings_get(q='trialType:IPR')

            # Search with filters and pagination
            results = await client.search_trial_proceedings_get(
                q='IPR',
                filters='proceedingStatus Instituted',
                limit=50,
                offset=0
            )
        """
        url = self._build_url(self._ptab_trials_proceedings_endpoint, "search")
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
            return await self._handle_response(response, TrialProceedingResponseBag.from_dict)

    async def search_trial_proceedings_download(self, payload: dict) -> TrialProceedingResponseBag:
        """
        Download trial proceeding search results using a JSON payload (POST method).

        Endpoint: POST /api/v1/patent/trials/proceedings/search/download

        This endpoint is similar to search_trial_proceedings but optimized for downloads.

        Args:
            payload (dict): The search criteria as a JSON-compatible dictionary.

        Returns:
            TrialProceedingResponseBag: The download response containing search results

        Raises:
            USPTOError: If the API request fails (400, 403, 404, 500)
        """
        url = self._build_url(self._ptab_trials_proceedings_endpoint, "search", "download")
        async with self.session.post(url, json=payload, headers=self.headers) as response:
            return await self._handle_response(response, TrialProceedingResponseBag.from_dict)

    async def search_trial_proceedings_download_get(
        self,
        q: Optional[str] = None,
        sort: Optional[str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        fields: Optional[str] = None,
        filters: Optional[str] = None,
        range_filters: Optional[str] = None,
        format: Optional[str] = None
    ) -> TrialProceedingResponseBag:
        """
        Download trial proceeding search results using query parameters (GET method).

        Endpoint: GET /api/v1/patent/trials/proceedings/search/download

        This endpoint is similar to search_trial_proceedings_get but optimized for downloads.
        Supports a format parameter for download format (json or csv).

        Args:
            q (str, optional): Search query string.
            sort (str, optional): Field to sort by followed by order.
            offset (int, optional): Position in dataset to start from. Default: 0
            limit (int, optional): Number of results to return. Default: 25
            fields (str, optional): Comma-separated list of fields to include in response.
            filters (str, optional): Filter by field value. Format: 'fieldName value1,value2'
            range_filters (str, optional): Filter by range. Format: 'fieldName min:max'
            format (str, optional): Download format. Options: 'json' or 'csv'. Default: 'json'

        Returns:
            TrialProceedingResponseBag: The download response containing search results

        Raises:
            USPTOError: If the API request fails (400, 403, 404, 500)

        Examples:
            # Download search results in JSON format
            results = await client.search_trial_proceedings_download_get(q='IPR', format='json')

            # Download search results in CSV format
            results = await client.search_trial_proceedings_download_get(q='IPR', format='csv', limit=100)
        """
        url = self._build_url(self._ptab_trials_proceedings_endpoint, "search", "download")
        params = {}
        if q is not None:
            params['q'] = q
        if sort is not None:
            params['sort'] = sort
        if offset is not None:
            params['offset'] = offset
        if limit is not None:
            params['limit'] = limit
        if fields is not None:
            params['fields'] = fields
        if filters is not None:
            params['filters'] = filters
        if range_filters is not None:
            params['rangeFilters'] = range_filters
        if format is not None:
            params['format'] = format

        async with self.session.get(url, params=params, headers=self.headers) as response:
            return await self._handle_response(response, TrialProceedingResponseBag.from_dict)

    async def get_trial_proceeding(self, trial_number: str) -> TrialProceedingIdentifierResponseBag:
        """
        Retrieve a specific trial proceeding by its trial number.

        Endpoint: GET /api/v1/patent/trials/proceedings/{trialNumber}

        Args:
            trial_number (str): The trial number identifier

        Returns:
            TrialProceedingIdentifierResponseBag: The trial proceeding data

        Raises:
            USPTOError: If the API request fails (400, 403, 404, 500)

        Examples:
            # Get trial proceeding
            proceeding = await client.get_trial_proceeding('IPR2020-00001')
        """
        url = self._build_url(self._ptab_trials_proceedings_endpoint, trial_number)

        async with self.session.get(url, headers=self.headers) as response:
            return await self._handle_response(response, TrialProceedingIdentifierResponseBag.from_dict)

    async def search_trial_decisions(self, payload: dict) -> TrialDecisionResponseBag:
        """
        Search trial decisions using a JSON payload (POST method).

        Endpoint: POST /api/v1/patent/trials/decisions/search

        Args:
            payload (dict): The search criteria as a JSON-compatible dictionary.
                           Can include fields like query text, sort options, filters, pagination, etc.

        Returns:
            TrialDecisionResponseBag: The search response containing trial decision results

        Raises:
            USPTOError: If the API request fails (400, 403, 404, 500)
        """
        url = self._build_url(self._ptab_trials_decisions_endpoint, "search")
        async with self.session.post(url, json=payload, headers=self.headers) as response:
            return await self._handle_response(response, TrialDecisionResponseBag.from_dict)

    async def search_trial_decisions_get(
        self,
        q: Optional[str] = None,
        sort: Optional[str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        facets: Optional[str] = None,
        fields: Optional[str] = None,
        filters: Optional[str] = None,
        range_filters: Optional[str] = None
    ) -> TrialDecisionResponseBag:
        """
        Search trial decisions using query parameters (GET method).

        Endpoint: GET /api/v1/patent/trials/decisions/search

        Args:
            q (str, optional): Search query string. Accepts boolean operators (AND, OR, NOT),
                              wildcards (*), and exact phrases (""). Example: 'trialType:IPR'
            sort (str, optional): Field to sort by followed by order. Example: 'decisionDate desc'
            offset (int, optional): Position in dataset to start from. Default: 0
            limit (int, optional): Number of results to return. Default: 25
            facets (str, optional): Comma-separated list of fields to facet.
            fields (str, optional): Comma-separated list of fields to include in response.
            filters (str, optional): Filter by field value. Format: 'fieldName value1,value2'
            range_filters (str, optional): Filter by range. Format: 'fieldName min:max'
                                          Example: 'decisionDate 2021-01-01:2025-01-01'

        Returns:
            TrialDecisionResponseBag: The search response containing trial decision results

        Raises:
            USPTOError: If the API request fails (400, 403, 404, 500)

        Examples:
            # Search for IPR trial decisions
            results = await client.search_trial_decisions_get(q='IPR')

            # Search with filters and pagination
            results = await client.search_trial_decisions_get(
                q='IPR',
                filters='decisionType Final',
                limit=50,
                offset=0
            )
        """
        url = self._build_url(self._ptab_trials_decisions_endpoint, "search")
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
            return await self._handle_response(response, TrialDecisionResponseBag.from_dict)

    async def search_trial_decisions_download(self, payload: dict) -> TrialDecisionResponseBag:
        """
        Download trial decision search results using a JSON payload (POST method).

        Endpoint: POST /api/v1/patent/trials/decisions/search/download

        This endpoint is similar to search_trial_decisions but optimized for downloads.

        Args:
            payload (dict): The search criteria as a JSON-compatible dictionary.

        Returns:
            TrialDecisionResponseBag: The download response containing search results

        Raises:
            USPTOError: If the API request fails (400, 403, 404, 500)
        """
        url = self._build_url(self._ptab_trials_decisions_endpoint, "search", "download")
        async with self.session.post(url, json=payload, headers=self.headers) as response:
            return await self._handle_response(response, TrialDecisionResponseBag.from_dict)

    async def search_trial_decisions_download_get(
        self,
        q: Optional[str] = None,
        sort: Optional[str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        fields: Optional[str] = None,
        filters: Optional[str] = None,
        range_filters: Optional[str] = None,
        format: Optional[str] = None
    ) -> TrialDecisionResponseBag:
        """
        Download trial decision search results using query parameters (GET method).

        Endpoint: GET /api/v1/patent/trials/decisions/search/download

        This endpoint is similar to search_trial_decisions_get but optimized for downloads.
        Supports a format parameter for download format (json or csv).

        Args:
            q (str, optional): Search query string.
            sort (str, optional): Field to sort by followed by order.
            offset (int, optional): Position in dataset to start from. Default: 0
            limit (int, optional): Number of results to return. Default: 25
            fields (str, optional): Comma-separated list of fields to include in response.
            filters (str, optional): Filter by field value. Format: 'fieldName value1,value2'
            range_filters (str, optional): Filter by range. Format: 'fieldName min:max'
            format (str, optional): Download format. Options: 'json' or 'csv'. Default: 'json'

        Returns:
            TrialDecisionResponseBag: The download response containing search results

        Raises:
            USPTOError: If the API request fails (400, 403, 404, 500)

        Examples:
            # Download search results in JSON format
            results = await client.search_trial_decisions_download_get(q='IPR', format='json')

            # Download search results in CSV format
            results = await client.search_trial_decisions_download_get(q='IPR', format='csv', limit=100)
        """
        url = self._build_url(self._ptab_trials_decisions_endpoint, "search", "download")
        params = {}
        if q is not None:
            params['q'] = q
        if sort is not None:
            params['sort'] = sort
        if offset is not None:
            params['offset'] = offset
        if limit is not None:
            params['limit'] = limit
        if fields is not None:
            params['fields'] = fields
        if filters is not None:
            params['filters'] = filters
        if range_filters is not None:
            params['rangeFilters'] = range_filters
        if format is not None:
            params['format'] = format

        async with self.session.get(url, params=params, headers=self.headers) as response:
            return await self._handle_response(response, TrialDecisionResponseBag.from_dict)

    async def get_trial_decision(self, document_identifier: str) -> TrialDecisionIdentifierResponseBag:
        """
        Retrieve a specific trial decision by its document identifier.

        Endpoint: GET /api/v1/patent/trials/decisions/{documentIdentifier}

        Args:
            document_identifier (str): The trial decision document identifier

        Returns:
            TrialDecisionIdentifierResponseBag: The trial decision data

        Raises:
            USPTOError: If the API request fails (400, 403, 404, 500)

        Examples:
            # Get trial decision by document identifier
            decision = await client.get_trial_decision('DOC-12345')
        """
        url = self._build_url(self._ptab_trials_decisions_endpoint, document_identifier)

        async with self.session.get(url, headers=self.headers) as response:
            return await self._handle_response(response, TrialDecisionIdentifierResponseBag.from_dict)

    async def get_trial_decisions_by_trial(self, trial_number: str) -> TrialDecisionByTrialResponseBag:
        """
        Retrieve all trial decisions for a specific trial number.

        Endpoint: GET /api/v1/patent/trials/{trialNumber}/decisions

        Args:
            trial_number (str): The trial number identifier (e.g., "IPR2020-00001")

        Returns:
            TrialDecisionByTrialResponseBag: The trial decisions data for the specified trial

        Raises:
            USPTOError: If the API request fails (400, 403, 404, 500)

        Examples:
            # Get all decisions for a trial
            decisions = await client.get_trial_decisions_by_trial('IPR2020-00001')
        """
        # Build URL: /api/v1/patent/trials/{trialNumber}/decisions
        url = self._build_url(
            f"{self.BASE_API_URL}/v1/patent/trials",
            trial_number,
            "decisions"
        )

        async with self.session.get(url, headers=self.headers) as response:
            return await self._handle_response(response, TrialDecisionByTrialResponseBag.from_dict)

    async def search_trial_documents(self, payload: dict) -> TrialDocumentResponseBag:
        """
        Search trial documents using a JSON payload (POST method).

        Endpoint: POST /api/v1/patent/trials/documents/search

        Args:
            payload (dict): The search criteria as a JSON-compatible dictionary.
                           Can include fields like query text, sort options, filters, pagination, etc.

        Returns:
            TrialDocumentResponseBag: The search response containing trial document results

        Raises:
            USPTOError: If the API request fails (400, 403, 404, 500)
        """
        url = self._build_url(self._ptab_trials_documents_endpoint, "search")
        async with self.session.post(url, json=payload, headers=self.headers) as response:
            return await self._handle_response(response, TrialDocumentResponseBag.from_dict)

    async def search_trial_documents_get(
        self,
        q: Optional[str] = None,
        sort: Optional[str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        facets: Optional[str] = None,
        fields: Optional[str] = None,
        filters: Optional[str] = None,
        range_filters: Optional[str] = None
    ) -> TrialDocumentResponseBag:
        """
        Search trial documents using query parameters (GET method).

        Endpoint: GET /api/v1/patent/trials/documents/search

        Args:
            q (str, optional): Search query string. Accepts boolean operators (AND, OR, NOT),
                              wildcards (*), and exact phrases (""). Example: 'trialType:IPR'
            sort (str, optional): Field to sort by followed by order. Example: 'documentDate desc'
            offset (int, optional): Position in dataset to start from. Default: 0
            limit (int, optional): Number of results to return. Default: 25
            facets (str, optional): Comma-separated list of fields to facet.
            fields (str, optional): Comma-separated list of fields to include in response.
            filters (str, optional): Filter by field value. Format: 'fieldName value1,value2'
            range_filters (str, optional): Filter by range. Format: 'fieldName min:max'
                                          Example: 'documentDate 2021-01-01:2025-01-01'

        Returns:
            TrialDocumentResponseBag: The search response containing trial document results

        Raises:
            USPTOError: If the API request fails (400, 403, 404, 500)

        Examples:
            # Search for IPR trial documents
            results = await client.search_trial_documents_get(q='IPR')

            # Search with filters and pagination
            results = await client.search_trial_documents_get(
                q='IPR',
                filters='documentType Petition',
                limit=50,
                offset=0
            )
        """
        url = self._build_url(self._ptab_trials_documents_endpoint, "search")
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
            return await self._handle_response(response, TrialDocumentResponseBag.from_dict)

    async def search_trial_documents_download(self, payload: dict) -> TrialDocumentResponseBag:
        """
        Download trial document search results using a JSON payload (POST method).

        Endpoint: POST /api/v1/patent/trials/documents/search/download

        This endpoint is similar to search_trial_documents but optimized for downloads.

        Args:
            payload (dict): The search criteria as a JSON-compatible dictionary.

        Returns:
            TrialDocumentResponseBag: The download response containing search results

        Raises:
            USPTOError: If the API request fails (400, 403, 404, 500)
        """
        url = self._build_url(self._ptab_trials_documents_endpoint, "search", "download")
        async with self.session.post(url, json=payload, headers=self.headers) as response:
            return await self._handle_response(response, TrialDocumentResponseBag.from_dict)

    async def search_trial_documents_download_get(
        self,
        q: Optional[str] = None,
        sort: Optional[str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        fields: Optional[str] = None,
        filters: Optional[str] = None,
        range_filters: Optional[str] = None,
        format: Optional[str] = None
    ) -> TrialDocumentResponseBag:
        """
        Download trial document search results using query parameters (GET method).

        Endpoint: GET /api/v1/patent/trials/documents/search/download

        This endpoint is similar to search_trial_documents_get but optimized for downloads.
        Supports a format parameter for download format (json or csv).

        Args:
            q (str, optional): Search query string.
            sort (str, optional): Field to sort by followed by order.
            offset (int, optional): Position in dataset to start from. Default: 0
            limit (int, optional): Number of results to return. Default: 25
            fields (str, optional): Comma-separated list of fields to include in response.
            filters (str, optional): Filter by field value. Format: 'fieldName value1,value2'
            range_filters (str, optional): Filter by range. Format: 'fieldName min:max'
            format (str, optional): Download format. Options: 'json' or 'csv'. Default: 'json'

        Returns:
            TrialDocumentResponseBag: The download response containing search results

        Raises:
            USPTOError: If the API request fails (400, 403, 404, 500)

        Examples:
            # Download search results in JSON format
            results = await client.search_trial_documents_download_get(q='IPR', format='json')

            # Download search results in CSV format
            results = await client.search_trial_documents_download_get(q='IPR', format='csv', limit=100)
        """
        url = self._build_url(self._ptab_trials_documents_endpoint, "search", "download")
        params = {}
        if q is not None:
            params['q'] = q
        if sort is not None:
            params['sort'] = sort
        if offset is not None:
            params['offset'] = offset
        if limit is not None:
            params['limit'] = limit
        if fields is not None:
            params['fields'] = fields
        if filters is not None:
            params['filters'] = filters
        if range_filters is not None:
            params['rangeFilters'] = range_filters
        if format is not None:
            params['format'] = format

        async with self.session.get(url, params=params, headers=self.headers) as response:
            return await self._handle_response(response, TrialDocumentResponseBag.from_dict)

    async def get_trial_document(self, document_identifier: str) -> TrialDocumentIdentifierResponseBag:
        """
        Retrieve a specific trial document by its document identifier.

        Endpoint: GET /api/v1/patent/trials/documents/{documentIdentifier}

        Args:
            document_identifier (str): The trial document identifier

        Returns:
            TrialDocumentIdentifierResponseBag: The trial document data

        Raises:
            USPTOError: If the API request fails (400, 403, 404, 500)

        Examples:
            # Get trial document by document identifier
            document = await client.get_trial_document('DOC-12345')
        """
        url = self._build_url(self._ptab_trials_documents_endpoint, document_identifier)

        async with self.session.get(url, headers=self.headers) as response:
            return await self._handle_response(response, TrialDocumentIdentifierResponseBag.from_dict)

    async def get_trial_documents_by_trial(self, trial_number: str) -> TrialDocumentByTrialResponseBag:
        """
        Retrieve all trial documents for a specific trial number.

        Endpoint: GET /api/v1/patent/trials/{trialNumber}/documents

        Args:
            trial_number (str): The trial number identifier (e.g., "IPR2020-00001")

        Returns:
            TrialDocumentByTrialResponseBag: The trial documents data for the specified trial

        Raises:
            USPTOError: If the API request fails (400, 403, 404, 500)

        Examples:
            # Get all documents for a trial
            documents = await client.get_trial_documents_by_trial('IPR2020-00001')
        """
        # Build URL: /api/v1/patent/trials/{trialNumber}/documents
        url = self._build_url(
            f"{self.BASE_API_URL}/v1/patent/trials",
            trial_number,
            "documents"
        )

        async with self.session.get(url, headers=self.headers) as response:
            return await self._handle_response(response, TrialDocumentByTrialResponseBag.from_dict)

    async def search_appeal_decisions(self, payload: dict) -> AppealDecisionResponseBag:
        """
        Search appeal decisions using a JSON payload (POST method).

        Endpoint: POST /api/v1/patent/appeals/decisions/search

        Args:
            payload (dict): The search criteria as a JSON-compatible dictionary.
                           Can include fields like query text, sort options, filters, pagination, etc.

        Returns:
            AppealDecisionResponseBag: The search response containing appeal decision results

        Raises:
            USPTOError: If the API request fails (400, 403, 404, 500)
        """
        url = self._build_url(self._ptab_appeals_decisions_endpoint, "search")
        async with self.session.post(url, json=payload, headers=self.headers) as response:
            return await self._handle_response(response, AppealDecisionResponseBag.from_dict)

    async def search_appeal_decisions_get(
        self,
        q: Optional[str] = None,
        sort: Optional[str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        facets: Optional[str] = None,
        fields: Optional[str] = None,
        filters: Optional[str] = None,
        range_filters: Optional[str] = None
    ) -> AppealDecisionResponseBag:
        """
        Search appeal decisions using query parameters (GET method).

        Endpoint: GET /api/v1/patent/appeals/decisions/search

        Args:
            q (str, optional): Search query string. Accepts boolean operators (AND, OR, NOT),
                              wildcards (*), and exact phrases (""). Example: 'decisionType:Final'
            sort (str, optional): Field to sort by followed by order. Example: 'decisionDate desc'
            offset (int, optional): Position in dataset to start from. Default: 0
            limit (int, optional): Number of results to return. Default: 25
            facets (str, optional): Comma-separated list of fields to facet.
            fields (str, optional): Comma-separated list of fields to include in response.
            filters (str, optional): Filter by field value. Format: 'fieldName value1,value2'
            range_filters (str, optional): Filter by range. Format: 'fieldName min:max'
                                          Example: 'decisionDate 2021-01-01:2025-01-01'

        Returns:
            AppealDecisionResponseBag: The search response containing appeal decision results

        Raises:
            USPTOError: If the API request fails (400, 403, 404, 500)

        Examples:
            # Search for appeal decisions
            results = await client.search_appeal_decisions_get(q='Final')

            # Search with filters and pagination
            results = await client.search_appeal_decisions_get(
                q='Final',
                filters='decisionType Final',
                limit=50,
                offset=0
            )
        """
        url = self._build_url(self._ptab_appeals_decisions_endpoint, "search")
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
            return await self._handle_response(response, AppealDecisionResponseBag.from_dict)

    async def search_appeal_decisions_download(self, payload: dict) -> AppealDecisionResponseBag:
        """
        Download appeal decision search results using a JSON payload (POST method).

        Endpoint: POST /api/v1/patent/appeals/decisions/search/download

        This endpoint is similar to search_appeal_decisions but optimized for downloads.

        Args:
            payload (dict): The search criteria as a JSON-compatible dictionary.

        Returns:
            AppealDecisionResponseBag: The download response containing search results

        Raises:
            USPTOError: If the API request fails (400, 403, 404, 500)
        """
        url = self._build_url(self._ptab_appeals_decisions_endpoint, "search", "download")
        async with self.session.post(url, json=payload, headers=self.headers) as response:
            return await self._handle_response(response, AppealDecisionResponseBag.from_dict)

    async def search_appeal_decisions_download_get(
        self,
        q: Optional[str] = None,
        sort: Optional[str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        fields: Optional[str] = None,
        filters: Optional[str] = None,
        range_filters: Optional[str] = None,
        format: Optional[str] = None
    ) -> AppealDecisionResponseBag:
        """
        Download appeal decision search results using query parameters (GET method).

        Endpoint: GET /api/v1/patent/appeals/decisions/search/download

        This endpoint is similar to search_appeal_decisions_get but optimized for downloads.
        Supports a format parameter for download format (json or csv).

        Args:
            q (str, optional): Search query string.
            sort (str, optional): Field to sort by followed by order.
            offset (int, optional): Position in dataset to start from. Default: 0
            limit (int, optional): Number of results to return. Default: 25
            fields (str, optional): Comma-separated list of fields to include in response.
            filters (str, optional): Filter by field value. Format: 'fieldName value1,value2'
            range_filters (str, optional): Filter by range. Format: 'fieldName min:max'
            format (str, optional): Download format. Options: 'json' or 'csv'. Default: 'json'

        Returns:
            AppealDecisionResponseBag: The download response containing search results

        Raises:
            USPTOError: If the API request fails (400, 403, 404, 500)

        Examples:
            # Download search results in JSON format
            results = await client.search_appeal_decisions_download_get(q='Final', format='json')

            # Download search results in CSV format
            results = await client.search_appeal_decisions_download_get(q='Final', format='csv', limit=100)
        """
        url = self._build_url(self._ptab_appeals_decisions_endpoint, "search", "download")
        params = {}
        if q is not None:
            params['q'] = q
        if sort is not None:
            params['sort'] = sort
        if offset is not None:
            params['offset'] = offset
        if limit is not None:
            params['limit'] = limit
        if fields is not None:
            params['fields'] = fields
        if filters is not None:
            params['filters'] = filters
        if range_filters is not None:
            params['rangeFilters'] = range_filters
        if format is not None:
            params['format'] = format

        async with self.session.get(url, params=params, headers=self.headers) as response:
            return await self._handle_response(response, AppealDecisionResponseBag.from_dict)

    async def get_appeal_decision(self, document_identifier: str) -> AppealDecisionIdentifierResponseBag:
        """
        Retrieve a specific appeal decision by its document identifier.

        Endpoint: GET /api/v1/patent/appeals/decisions/{documentIdentifier}

        Args:
            document_identifier (str): The appeal decision document identifier

        Returns:
            AppealDecisionIdentifierResponseBag: The appeal decision data

        Raises:
            USPTOError: If the API request fails (400, 403, 404, 500)

        Examples:
            # Get appeal decision by document identifier
            decision = await client.get_appeal_decision('DOC-12345')
        """
        url = self._build_url(self._ptab_appeals_decisions_endpoint, document_identifier)

        async with self.session.get(url, headers=self.headers) as response:
            return await self._handle_response(response, AppealDecisionIdentifierResponseBag.from_dict)

    async def get_appeal_decisions_by_appeal(self, appeal_number: str) -> AppealDecisionByAppealResponseBag:
        """
        Retrieve all appeal decisions for a specific appeal number.

        Endpoint: GET /api/v1/patent/appeals/{appealNumber}/decisions

        Args:
            appeal_number (str): The appeal number identifier (e.g., "2020-001234")

        Returns:
            AppealDecisionByAppealResponseBag: The appeal decisions data for the specified appeal

        Raises:
            USPTOError: If the API request fails (400, 403, 404, 500)

        Examples:
            # Get all decisions for an appeal
            decisions = await client.get_appeal_decisions_by_appeal('2020-001234')
        """
        # Build URL: /api/v1/patent/appeals/{appealNumber}/decisions
        url = self._build_url(
            f"{self.BASE_API_URL}/v1/patent/appeals",
            appeal_number,
            "decisions"
        )

        async with self.session.get(url, headers=self.headers) as response:
            return await self._handle_response(response, AppealDecisionByAppealResponseBag.from_dict)

    async def search_interference_decisions(self, payload: dict) -> InterferenceDecisionResponseBag:
        """
        Search interference decisions using a JSON payload (POST method).

        Endpoint: POST /api/v1/patent/interferences/decisions/search

        Args:
            payload (dict): The search criteria as a JSON-compatible dictionary.
                           Can include fields like query text, sort options, filters, pagination, etc.

        Returns:
            InterferenceDecisionResponseBag: The search response containing interference decision results

        Raises:
            USPTOError: If the API request fails (400, 403, 404, 500)
        """
        url = self._build_url(self._ptab_interferences_decisions_endpoint, "search")
        async with self.session.post(url, json=payload, headers=self.headers) as response:
            return await self._handle_response(response, InterferenceDecisionResponseBag.from_dict)

    async def search_interference_decisions_get(
        self,
        q: Optional[str] = None,
        sort: Optional[str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        facets: Optional[str] = None,
        fields: Optional[str] = None,
        filters: Optional[str] = None,
        range_filters: Optional[str] = None
    ) -> InterferenceDecisionResponseBag:
        """
        Search interference decisions using query parameters (GET method).

        Endpoint: GET /api/v1/patent/interferences/decisions/search

        Args:
            q (str, optional): Search query string. Accepts boolean operators (AND, OR, NOT),
                              wildcards (*), and exact phrases (""). Example: 'decisionType:Final'
            sort (str, optional): Field to sort by followed by order. Example: 'decisionDate desc'
            offset (int, optional): Position in dataset to start from. Default: 0
            limit (int, optional): Number of results to return. Default: 25
            facets (str, optional): Comma-separated list of fields to facet.
            fields (str, optional): Comma-separated list of fields to include in response.
            filters (str, optional): Filter by field value. Format: 'fieldName value1,value2'
            range_filters (str, optional): Filter by range. Format: 'fieldName min:max'
                                          Example: 'decisionDate 2021-01-01:2025-01-01'

        Returns:
            InterferenceDecisionResponseBag: The search response containing interference decision results

        Raises:
            USPTOError: If the API request fails (400, 403, 404, 500)

        Examples:
            # Search for interference decisions
            results = await client.search_interference_decisions_get(q='Final')

            # Search with filters and pagination
            results = await client.search_interference_decisions_get(
                q='Final',
                filters='decisionType Final',
                limit=50,
                offset=0
            )
        """
        url = self._build_url(self._ptab_interferences_decisions_endpoint, "search")
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
            return await self._handle_response(response, InterferenceDecisionResponseBag.from_dict)

    async def search_interference_decisions_download(self, payload: dict) -> InterferenceDecisionResponseBag:
        """
        Download interference decision search results using a JSON payload (POST method).

        Endpoint: POST /api/v1/patent/interferences/decisions/search/download

        This endpoint is similar to search_interference_decisions but optimized for downloads.

        Args:
            payload (dict): The search criteria as a JSON-compatible dictionary.

        Returns:
            InterferenceDecisionResponseBag: The download response containing search results

        Raises:
            USPTOError: If the API request fails (400, 403, 404, 500)
        """
        url = self._build_url(self._ptab_interferences_decisions_endpoint, "search", "download")
        async with self.session.post(url, json=payload, headers=self.headers) as response:
            return await self._handle_response(response, InterferenceDecisionResponseBag.from_dict)

    async def search_interference_decisions_download_get(
        self,
        q: Optional[str] = None,
        sort: Optional[str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        fields: Optional[str] = None,
        filters: Optional[str] = None,
        range_filters: Optional[str] = None,
        format: Optional[str] = None
    ) -> InterferenceDecisionResponseBag:
        """
        Download interference decision search results using query parameters (GET method).

        Endpoint: GET /api/v1/patent/interferences/decisions/search/download

        This endpoint is similar to search_interference_decisions_get but optimized for downloads.
        Supports a format parameter for download format (json or csv).

        Args:
            q (str, optional): Search query string.
            sort (str, optional): Field to sort by followed by order.
            offset (int, optional): Position in dataset to start from. Default: 0
            limit (int, optional): Number of results to return. Default: 25
            fields (str, optional): Comma-separated list of fields to include in response.
            filters (str, optional): Filter by field value. Format: 'fieldName value1,value2'
            range_filters (str, optional): Filter by range. Format: 'fieldName min:max'
            format (str, optional): Download format. Options: 'json' or 'csv'. Default: 'json'

        Returns:
            InterferenceDecisionResponseBag: The download response containing search results

        Raises:
            USPTOError: If the API request fails (400, 403, 404, 500)

        Examples:
            # Download search results in JSON format
            results = await client.search_interference_decisions_download_get(q='Final', format='json')

            # Download search results in CSV format
            results = await client.search_interference_decisions_download_get(q='Final', format='csv', limit=100)
        """
        url = self._build_url(self._ptab_interferences_decisions_endpoint, "search", "download")
        params = {}
        if q is not None:
            params['q'] = q
        if sort is not None:
            params['sort'] = sort
        if offset is not None:
            params['offset'] = offset
        if limit is not None:
            params['limit'] = limit
        if fields is not None:
            params['fields'] = fields
        if filters is not None:
            params['filters'] = filters
        if range_filters is not None:
            params['rangeFilters'] = range_filters
        if format is not None:
            params['format'] = format

        async with self.session.get(url, params=params, headers=self.headers) as response:
            return await self._handle_response(response, InterferenceDecisionResponseBag.from_dict)

    async def get_interference_decision(self, document_identifier: str) -> InterferenceDecisionIdentifierResponseBag:
        """
        Retrieve a specific interference decision by its document identifier.

        Endpoint: GET /api/v1/patent/interferences/decisions/{documentIdentifier}

        Args:
            document_identifier (str): The interference decision document identifier

        Returns:
            InterferenceDecisionIdentifierResponseBag: The interference decision data

        Raises:
            USPTOError: If the API request fails (400, 403, 404, 500)

        Examples:
            # Get interference decision by document identifier
            decision = await client.get_interference_decision('DOC-12345')
        """
        url = self._build_url(self._ptab_interferences_decisions_endpoint, document_identifier)

        async with self.session.get(url, headers=self.headers) as response:
            return await self._handle_response(response, InterferenceDecisionIdentifierResponseBag.from_dict)

    async def get_interference_decisions_by_interference(self, interference_number: str) -> InterferenceDecisionByInterferenceResponseBag:
        """
        Retrieve all interference decisions for a specific interference number.

        Endpoint: GET /api/v1/patent/interferences/{interferenceNumber}/decisions

        Args:
            interference_number (str): The interference number identifier (e.g., "106,001")

        Returns:
            InterferenceDecisionByInterferenceResponseBag: The interference decisions data for the specified interference

        Raises:
            USPTOError: If the API request fails (400, 403, 404, 500)

        Examples:
            # Get all decisions for an interference
            decisions = await client.get_interference_decisions_by_interference('106,001')
        """
        # Build URL: /api/v1/patent/interferences/{interferenceNumber}/decisions
        url = self._build_url(
            f"{self.BASE_API_URL}/v1/patent/interferences",
            interference_number,
            "decisions"
        )

        async with self.session.get(url, headers=self.headers) as response:
            return await self._handle_response(response, InterferenceDecisionByInterferenceResponseBag.from_dict)

    async def search_dataset_products_get(
        self,
        q: Optional[str] = None,
        sort: Optional[str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        facets: Optional[str] = None,
        fields: Optional[str] = None,
        filters: Optional[str] = None,
        range_filters: Optional[str] = None
    ) -> DatasetProductSearchResponseBag:
        """
        Search dataset products using query parameters (GET method).

        Endpoint: GET /api/v1/datasets/products/search

        Args:
            q (str, optional): Search query string. Accepts boolean operators (AND, OR, NOT),
                              wildcards (*), and exact phrases (""). Example: 'productType:Patent'
            sort (str, optional): Field to sort by followed by order. Example: 'releaseDate desc'
            offset (int, optional): Position in dataset to start from. Default: 0
            limit (int, optional): Number of results to return. Default: 25
            facets (str, optional): Comma-separated list of fields to facet.
            fields (str, optional): Comma-separated list of fields to include in response.
            filters (str, optional): Filter by field value. Format: 'fieldName value1,value2'
            range_filters (str, optional): Filter by range. Format: 'fieldName min:max'
                                          Example: 'releaseDate 2021-01-01:2025-01-01'

        Returns:
            DatasetProductSearchResponseBag: The search response containing dataset product results

        Raises:
            USPTOError: If the API request fails (400, 403, 404, 500)

        Examples:
            # Search for dataset products
            results = await client.search_dataset_products_get(q='Patent')

            # Search with filters and pagination
            results = await client.search_dataset_products_get(
                q='Patent',
                filters='productType Patent',
                limit=50,
                offset=0
            )
        """
        url = self._build_url(self._bulk_datasets_endpoint, "search")
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
            return await self._handle_response(response, DatasetProductSearchResponseBag.from_dict)

    async def get_dataset_product(
        self,
        product_identifier: str,
        file_data_from_date: Optional[str] = None,
        file_data_to_date: Optional[str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        include_files: Optional[str] = None,
        latest: Optional[str] = None
    ) -> DatasetProductResponseBag:
        """
        Retrieve a specific dataset product by its product identifier.

        Endpoint: GET /api/v1/datasets/products/{productIdentifier}

        Args:
            product_identifier (str): The dataset product identifier
            file_data_from_date (str, optional): Filter product files by date from.
                                                Format: 'yyyy-MM-dd' (e.g., '2023-01-01')
            file_data_to_date (str, optional): Filter product files by date to.
                                              Format: 'yyyy-MM-dd' (e.g., '2023-12-31')
            offset (int, optional): Number of product file records to skip. Default: 0
            limit (int, optional): Number of product file records to collect
            include_files (str, optional): Set to 'true' to include product files in response,
                                          'false' to omit them. Default: None (API default behavior)
            latest (str, optional): Set to 'true' to return only the latest product file,
                                   'false' otherwise. Default: None (API default behavior)

        Returns:
            DatasetProductResponseBag: The dataset product data

        Raises:
            USPTOError: If the API request fails (400, 403, 404, 500)

        Examples:
            # Get dataset product by product identifier
            product = await client.get_dataset_product('product-12345')

            # Get product with date range filter
            product = await client.get_dataset_product(
                'product-12345',
                file_data_from_date='2023-01-01',
                file_data_to_date='2023-12-31'
            )

            # Get product with latest file only
            product = await client.get_dataset_product('product-12345', latest='true')

            # Get product without files included
            product = await client.get_dataset_product('product-12345', include_files='false')
        """
        url = self._build_url(self._bulk_datasets_endpoint, product_identifier)
        params = {}

        if file_data_from_date is not None:
            params['fileDataFromDate'] = file_data_from_date
        if file_data_to_date is not None:
            params['fileDataToDate'] = file_data_to_date
        if offset is not None:
            params['offset'] = offset
        if limit is not None:
            params['limit'] = limit
        if include_files is not None:
            params['includeFiles'] = include_files
        if latest is not None:
            params['latest'] = latest

        async with self.session.get(url, params=params, headers=self.headers) as response:
            return await self._handle_response(response, DatasetProductResponseBag.from_dict)

    async def get_dataset_file(self, product_identifier: str, file_name: str) -> DatasetFileResponseBag:
        """
        Retrieve a specific dataset file by product identifier and file name.

        Endpoint: GET /api/v1/datasets/products/files/{productIdentifier}/{fileName}

        Args:
            product_identifier (str): The dataset product identifier
            file_name (str): The file name within the product

        Returns:
            DatasetFileResponseBag: The dataset file data (may contain download URL or metadata)

        Raises:
            USPTOError: If the API request fails (400, 403, 404, 500)

        Examples:
            # Get dataset file by product identifier and file name
            file_info = await client.get_dataset_file('product-12345', 'data.csv')
        """
        url = self._build_url(self._bulk_datasets_endpoint, "files", product_identifier, file_name)

        async with self.session.get(url, headers=self.headers) as response:
            return await self._handle_response(response, DatasetFileResponseBag.from_dict)

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
