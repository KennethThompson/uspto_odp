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
class InterferenceDecision:
    """
    Individual interference decision record.
    """
    document_identifier: Optional[str] = None
    interference_number: Optional[str] = None
    decision_type: Optional[str] = None
    decision_date: Optional[str] = None
    decision_mail_date: Optional[str] = None
    document_type: Optional[str] = None
    document_title: Optional[str] = None
    patent_number: Optional[str] = None
    application_number_text: Optional[str] = None
    filing_date: Optional[str] = None
    # Additional fields that may be present
    proceeding_status: Optional[str] = None
    senior_party_name: Optional[str] = None
    junior_party_name: Optional[str] = None
    technology_center: Optional[str] = None
    art_unit: Optional[str] = None
    document_url: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'InterferenceDecision':
        """
        Parse an interference decision record from API response.
        
        Args:
            data (dict): Raw dictionary from API response
            
        Returns:
            InterferenceDecision: Parsed interference decision record
        """
        return cls(
            document_identifier=data.get('documentIdentifier'),
            interference_number=data.get('interferenceNumber'),
            decision_type=data.get('decisionType'),
            decision_date=data.get('decisionDate'),
            decision_mail_date=data.get('decisionMailDate'),
            document_type=data.get('documentType'),
            document_title=data.get('documentTitle'),
            patent_number=data.get('patentNumber'),
            application_number_text=data.get('applicationNumberText'),
            filing_date=data.get('filingDate'),
            proceeding_status=data.get('proceedingStatus'),
            senior_party_name=data.get('seniorPartyName'),
            junior_party_name=data.get('juniorPartyName'),
            technology_center=data.get('technologyCenter'),
            art_unit=data.get('artUnit'),
            document_url=data.get('documentUrl')
        )


@dataclass
class InterferenceDecisionResponseBag:
    """
    Response container for interference decision search results.
    """
    count: int = 0
    interference_decision_bag: List[InterferenceDecision] = field(default_factory=list)
    request_identifier: Optional[str] = None
    facets: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'InterferenceDecisionResponseBag':
        """
        Parse the search response data into an InterferenceDecisionResponseBag object.
        
        Args:
            data (dict): The raw JSON response from the API
            
        Returns:
            InterferenceDecisionResponseBag: A structured representation of the search results
        """
        result = cls(
            count=data.get('count', 0),
            request_identifier=data.get('requestIdentifier'),
            facets=data.get('facets')
        )
        
        # Parse interference decision bag (API uses camelCase: interferenceDecisionBag)
        if 'interferenceDecisionBag' in data:
            result.interference_decision_bag = [
                InterferenceDecision.from_dict(decision_data)
                for decision_data in data['interferenceDecisionBag']
            ]
        
        return result


@dataclass
class InterferenceDecisionIdentifierResponseBag:
    """
    Response container for individual interference decision lookup by document identifier.
    Similar to InterferenceDecisionResponseBag but for single record retrieval.
    """
    count: int = 0
    interference_decision_bag: List[InterferenceDecision] = field(default_factory=list)
    request_identifier: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'InterferenceDecisionIdentifierResponseBag':
        """
        Parse the individual interference decision response by document identifier.
        
        Args:
            data (dict): The raw JSON response from the API
            
        Returns:
            InterferenceDecisionIdentifierResponseBag: A structured representation of the interference decision
        """
        result = cls(
            count=data.get('count', 0),
            request_identifier=data.get('requestIdentifier')
        )
        
        # Parse interference decision bag (typically contains one record)
        if 'interferenceDecisionBag' in data:
            result.interference_decision_bag = [
                InterferenceDecision.from_dict(decision_data)
                for decision_data in data['interferenceDecisionBag']
            ]
        
        return result


@dataclass
class InterferenceDecisionByInterferenceResponseBag:
    """
    Response container for interference decisions lookup by interference number.
    Similar to InterferenceDecisionResponseBag but for decisions retrieved by interference number.
    """
    count: int = 0
    interference_decision_bag: List[InterferenceDecision] = field(default_factory=list)
    request_identifier: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'InterferenceDecisionByInterferenceResponseBag':
        """
        Parse the interference decisions response by interference number.
        
        Args:
            data (dict): The raw JSON response from the API
            
        Returns:
            InterferenceDecisionByInterferenceResponseBag: A structured representation of the interference decisions
        """
        result = cls(
            count=data.get('count', 0),
            request_identifier=data.get('requestIdentifier')
        )
        
        # Parse interference decision bag (may contain multiple decisions for an interference)
        if 'interferenceDecisionBag' in data:
            result.interference_decision_bag = [
                InterferenceDecision.from_dict(decision_data)
                for decision_data in data['interferenceDecisionBag']
            ]
        
        return result
