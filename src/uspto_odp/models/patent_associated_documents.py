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
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


@dataclass
class PGPubFileMetaData:
    """Represents pre-grant publication (PGPub) file metadata"""
    product_identifier: Optional[str] = None
    zip_file_name: Optional[str] = None
    file_create_date_time: Optional[str] = None
    xml_file_name: Optional[str] = None
    file_location_uri: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'PGPubFileMetaData':
        """
        Parse PGPub file metadata from API response.
        Handles various field name variations that may exist in the API.
        """
        return cls(
            product_identifier=data.get('productIdentifier') or data.get('product_identifier'),
            zip_file_name=data.get('zipFileName') or data.get('zip_file_name'),
            file_create_date_time=data.get('fileCreateDateTime') or data.get('file_create_date_time'),
            xml_file_name=data.get('xmlFileName') or data.get('xml_file_name'),
            file_location_uri=data.get('fileLocationURI') or data.get('file_location_uri')
        )


@dataclass
class GrantFileMetaData:
    """Represents grant file metadata"""
    product_identifier: Optional[str] = None
    zip_file_name: Optional[str] = None
    file_create_date_time: Optional[str] = None
    xml_file_name: Optional[str] = None
    file_location_uri: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'GrantFileMetaData':
        """
        Parse grant file metadata from API response.
        Handles various field name variations that may exist in the API.
        """
        return cls(
            product_identifier=data.get('productIdentifier') or data.get('product_identifier'),
            zip_file_name=data.get('zipFileName') or data.get('zip_file_name'),
            file_create_date_time=data.get('fileCreateDateTime') or data.get('file_create_date_time'),
            xml_file_name=data.get('xmlFileName') or data.get('xml_file_name'),
            file_location_uri=data.get('fileLocationURI') or data.get('file_location_uri')
        )


@dataclass
class ApplicationAssociatedDocuments:
    """Represents associated documents data for a patent application"""
    application_number: str
    pgpub_document_meta_data: Optional[PGPubFileMetaData] = None
    grant_document_meta_data: Optional[GrantFileMetaData] = None
    request_identifier: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'ApplicationAssociatedDocuments':
        return cls(
            application_number=data.get('applicationNumberText', ''),
            pgpub_document_meta_data=PGPubFileMetaData.from_dict(
                data.get('pgpubDocumentMetaData', {})
            ) if data.get('pgpubDocumentMetaData') else None,
            grant_document_meta_data=GrantFileMetaData.from_dict(
                data.get('grantDocumentMetaData', {})
            ) if data.get('grantDocumentMetaData') else None,
            request_identifier=data.get('requestIdentifier')
        )


@dataclass
class AssociatedDocumentsResponse:
    """Response model for the /associated-documents endpoint"""
    count: int
    associated_documents: list[ApplicationAssociatedDocuments] = field(default_factory=list)
    request_identifier: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'AssociatedDocumentsResponse':
        """
        Parse the associated-documents endpoint response.
        
        The API returns:
        {
            "count": 1,
            "patentFileWrapperDataBag": [
                {
                    "applicationNumberText": "...",
                    "pgpubDocumentMetaData": {...},
                    "grantDocumentMetaData": {...},
                    "requestIdentifier": "..."
                }
            ],
            "requestIdentifier": "..." (optional at top level)
        }
        """
        return cls(
            count=data.get('count', 0),
            associated_documents=[ApplicationAssociatedDocuments.from_dict(pw) 
                                for pw in data.get('patentFileWrapperDataBag', [])],
            request_identifier=data.get('requestIdentifier')
        )
