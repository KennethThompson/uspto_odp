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
from typing import List, Optional, Dict, Any


@dataclass
class TrialDocument:
    """
    Individual trial document record.
    """
    document_identifier: Optional[str] = None
    trial_number: Optional[str] = None
    trial_type: Optional[str] = None
    document_type: Optional[str] = None
    document_title: Optional[str] = None
    filing_date: Optional[str] = None
    document_date: Optional[str] = None
    patent_number: Optional[str] = None
    application_number_text: Optional[str] = None
    # Additional fields that may be present
    proceeding_status: Optional[str] = None
    petitioner_name: Optional[str] = None
    patent_owner_name: Optional[str] = None
    technology_center: Optional[str] = None
    art_unit: Optional[str] = None
    document_url: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'TrialDocument':
        """
        Parse a trial document record from API response.
        
        Args:
            data (dict): Raw dictionary from API response
            
        Returns:
            TrialDocument: Parsed trial document record
        """
        return cls(
            document_identifier=data.get('documentIdentifier'),
            trial_number=data.get('trialNumber'),
            trial_type=data.get('trialType'),
            document_type=data.get('documentType'),
            document_title=data.get('documentTitle'),
            filing_date=data.get('filingDate'),
            document_date=data.get('documentDate'),
            patent_number=data.get('patentNumber'),
            application_number_text=data.get('applicationNumberText'),
            proceeding_status=data.get('proceedingStatus'),
            petitioner_name=data.get('petitionerName'),
            patent_owner_name=data.get('patentOwnerName'),
            technology_center=data.get('technologyCenter'),
            art_unit=data.get('artUnit'),
            document_url=data.get('documentUrl')
        )


@dataclass
class TrialDocumentResponseBag:
    """
    Response container for trial document search results.
    """
    count: int = 0
    trial_document_bag: List[TrialDocument] = field(default_factory=list)
    request_identifier: Optional[str] = None
    facets: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'TrialDocumentResponseBag':
        """
        Parse the search response data into a TrialDocumentResponseBag object.
        
        Args:
            data (dict): The raw JSON response from the API
            
        Returns:
            TrialDocumentResponseBag: A structured representation of the search results
        """
        result = cls(
            count=data.get('count', 0),
            request_identifier=data.get('requestIdentifier'),
            facets=data.get('facets')
        )
        
        # Parse trial document bag (API uses camelCase: trialDocumentBag)
        if 'trialDocumentBag' in data:
            result.trial_document_bag = [
                TrialDocument.from_dict(document_data)
                for document_data in data['trialDocumentBag']
            ]
        
        return result


@dataclass
class TrialDocumentIdentifierResponseBag:
    """
    Response container for individual trial document lookup by document identifier.
    Similar to TrialDocumentResponseBag but for single record retrieval.
    """
    count: int = 0
    trial_document_bag: List[TrialDocument] = field(default_factory=list)
    request_identifier: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'TrialDocumentIdentifierResponseBag':
        """
        Parse the individual trial document response by document identifier.
        
        Args:
            data (dict): The raw JSON response from the API
            
        Returns:
            TrialDocumentIdentifierResponseBag: A structured representation of the trial document
        """
        result = cls(
            count=data.get('count', 0),
            request_identifier=data.get('requestIdentifier')
        )
        
        # Parse trial document bag (typically contains one record)
        if 'trialDocumentBag' in data:
            result.trial_document_bag = [
                TrialDocument.from_dict(document_data)
                for document_data in data['trialDocumentBag']
            ]
        
        return result


@dataclass
class TrialDocumentByTrialResponseBag:
    """
    Response container for trial documents lookup by trial number.
    Similar to TrialDocumentResponseBag but for documents retrieved by trial number.
    """
    count: int = 0
    trial_document_bag: List[TrialDocument] = field(default_factory=list)
    request_identifier: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'TrialDocumentByTrialResponseBag':
        """
        Parse the trial documents response by trial number.
        
        Args:
            data (dict): The raw JSON response from the API
            
        Returns:
            TrialDocumentByTrialResponseBag: A structured representation of the trial documents
        """
        result = cls(
            count=data.get('count', 0),
            request_identifier=data.get('requestIdentifier')
        )
        
        # Parse trial document bag (may contain multiple documents for a trial)
        if 'trialDocumentBag' in data:
            result.trial_document_bag = [
                TrialDocument.from_dict(document_data)
                for document_data in data['trialDocumentBag']
            ]
        
        return result
