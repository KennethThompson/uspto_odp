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
class AppealDecision:
    """
    Individual appeal decision record.
    """
    document_identifier: Optional[str] = None
    appeal_number: Optional[str] = None
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
    appellant_name: Optional[str] = None
    technology_center: Optional[str] = None
    art_unit: Optional[str] = None
    document_url: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'AppealDecision':
        """
        Parse an appeal decision record from API response.
        
        Args:
            data (dict): Raw dictionary from API response
            
        Returns:
            AppealDecision: Parsed appeal decision record
        """
        return cls(
            document_identifier=data.get('documentIdentifier'),
            appeal_number=data.get('appealNumber'),
            decision_type=data.get('decisionType'),
            decision_date=data.get('decisionDate'),
            decision_mail_date=data.get('decisionMailDate'),
            document_type=data.get('documentType'),
            document_title=data.get('documentTitle'),
            patent_number=data.get('patentNumber'),
            application_number_text=data.get('applicationNumberText'),
            filing_date=data.get('filingDate'),
            proceeding_status=data.get('proceedingStatus'),
            appellant_name=data.get('appellantName'),
            technology_center=data.get('technologyCenter'),
            art_unit=data.get('artUnit'),
            document_url=data.get('documentUrl')
        )


@dataclass
class AppealDecisionResponseBag:
    """
    Response container for appeal decision search results.
    """
    count: int = 0
    appeal_decision_bag: List[AppealDecision] = field(default_factory=list)
    request_identifier: Optional[str] = None
    facets: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'AppealDecisionResponseBag':
        """
        Parse the search response data into an AppealDecisionResponseBag object.
        
        Args:
            data (dict): The raw JSON response from the API
            
        Returns:
            AppealDecisionResponseBag: A structured representation of the search results
        """
        result = cls(
            count=data.get('count', 0),
            request_identifier=data.get('requestIdentifier'),
            facets=data.get('facets')
        )
        
        # Parse appeal decision bag (API uses camelCase: appealDecisionBag)
        if 'appealDecisionBag' in data:
            result.appeal_decision_bag = [
                AppealDecision.from_dict(decision_data)
                for decision_data in data['appealDecisionBag']
            ]
        
        return result


@dataclass
class AppealDecisionIdentifierResponseBag:
    """
    Response container for individual appeal decision lookup by document identifier.
    Similar to AppealDecisionResponseBag but for single record retrieval.
    """
    count: int = 0
    appeal_decision_bag: List[AppealDecision] = field(default_factory=list)
    request_identifier: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'AppealDecisionIdentifierResponseBag':
        """
        Parse the individual appeal decision response by document identifier.
        
        Args:
            data (dict): The raw JSON response from the API
            
        Returns:
            AppealDecisionIdentifierResponseBag: A structured representation of the appeal decision
        """
        result = cls(
            count=data.get('count', 0),
            request_identifier=data.get('requestIdentifier')
        )
        
        # Parse appeal decision bag (typically contains one record)
        if 'appealDecisionBag' in data:
            result.appeal_decision_bag = [
                AppealDecision.from_dict(decision_data)
                for decision_data in data['appealDecisionBag']
            ]
        
        return result


@dataclass
class AppealDecisionByAppealResponseBag:
    """
    Response container for appeal decisions lookup by appeal number.
    Similar to AppealDecisionResponseBag but for decisions retrieved by appeal number.
    """
    count: int = 0
    appeal_decision_bag: List[AppealDecision] = field(default_factory=list)
    request_identifier: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'AppealDecisionByAppealResponseBag':
        """
        Parse the appeal decisions response by appeal number.
        
        Args:
            data (dict): The raw JSON response from the API
            
        Returns:
            AppealDecisionByAppealResponseBag: A structured representation of the appeal decisions
        """
        result = cls(
            count=data.get('count', 0),
            request_identifier=data.get('requestIdentifier')
        )
        
        # Parse appeal decision bag (may contain multiple decisions for an appeal)
        if 'appealDecisionBag' in data:
            result.appeal_decision_bag = [
                AppealDecision.from_dict(decision_data)
                for decision_data in data['appealDecisionBag']
            ]
        
        return result
