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
class TrialProceeding:
    """
    Individual trial proceeding record.
    """
    trial_number: Optional[str] = None
    trial_type: Optional[str] = None
    proceeding_status: Optional[str] = None
    institution_date: Optional[str] = None
    filing_date: Optional[str] = None
    patent_number: Optional[str] = None
    application_number_text: Optional[str] = None
    petitioner_name: Optional[str] = None
    patent_owner_name: Optional[str] = None
    # Additional fields that may be present
    termination_date: Optional[str] = None
    technology_center: Optional[str] = None
    art_unit: Optional[str] = None
    proceeding_type: Optional[str] = None
    proceeding_category: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'TrialProceeding':
        """
        Parse a trial proceeding record from API response.
        
        Args:
            data (dict): Raw dictionary from API response
            
        Returns:
            TrialProceeding: Parsed trial proceeding record
        """
        return cls(
            trial_number=data.get('trialNumber'),
            trial_type=data.get('trialType'),
            proceeding_status=data.get('proceedingStatus'),
            institution_date=data.get('institutionDate'),
            filing_date=data.get('filingDate'),
            patent_number=data.get('patentNumber'),
            application_number_text=data.get('applicationNumberText'),
            petitioner_name=data.get('petitionerName'),
            patent_owner_name=data.get('patentOwnerName'),
            termination_date=data.get('terminationDate'),
            technology_center=data.get('technologyCenter'),
            art_unit=data.get('artUnit'),
            proceeding_type=data.get('proceedingType'),
            proceeding_category=data.get('proceedingCategory')
        )


@dataclass
class TrialProceedingResponseBag:
    """
    Response container for trial proceeding search results.
    """
    count: int = 0
    trial_proceeding_bag: List[TrialProceeding] = field(default_factory=list)
    request_identifier: Optional[str] = None
    facets: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'TrialProceedingResponseBag':
        """
        Parse the search response data into a TrialProceedingResponseBag object.
        
        Args:
            data (dict): The raw JSON response from the API
            
        Returns:
            TrialProceedingResponseBag: A structured representation of the search results
        """
        result = cls(
            count=data.get('count', 0),
            request_identifier=data.get('requestIdentifier'),
            facets=data.get('facets')
        )
        
        # Parse trial proceeding bag
        if 'trialProceedingBag' in data:
            result.trial_proceeding_bag = [
                TrialProceeding.from_dict(proceeding_data)
                for proceeding_data in data['trialProceedingBag']
            ]
        
        return result


@dataclass
class TrialProceedingIdentifierResponseBag:
    """
    Response container for individual trial proceeding lookup.
    Similar to TrialProceedingResponseBag but for single record retrieval.
    """
    count: int = 0
    trial_proceeding_bag: List[TrialProceeding] = field(default_factory=list)
    request_identifier: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'TrialProceedingIdentifierResponseBag':
        """
        Parse the individual trial proceeding response.
        
        Args:
            data (dict): The raw JSON response from the API
            
        Returns:
            TrialProceedingIdentifierResponseBag: A structured representation of the trial proceeding
        """
        result = cls(
            count=data.get('count', 0),
            request_identifier=data.get('requestIdentifier')
        )
        
        # Parse trial proceeding bag (typically contains one record)
        if 'trialProceedingBag' in data:
            result.trial_proceeding_bag = [
                TrialProceeding.from_dict(proceeding_data)
                for proceeding_data in data['trialProceedingBag']
            ]
        
        return result
