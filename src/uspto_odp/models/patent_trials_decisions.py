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
class TrialDecision:
    """
    Individual trial decision record.
    """
    document_identifier: Optional[str] = None
    trial_number: Optional[str] = None
    trial_type: Optional[str] = None
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
    petitioner_name: Optional[str] = None
    patent_owner_name: Optional[str] = None
    technology_center: Optional[str] = None
    art_unit: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'TrialDecision':
        """
        Parse a trial decision record from API response.
        
        Args:
            data (dict): Raw dictionary from API response
            
        Returns:
            TrialDecision: Parsed trial decision record
        """
        return cls(
            document_identifier=data.get('documentIdentifier'),
            trial_number=data.get('trialNumber'),
            trial_type=data.get('trialType'),
            decision_type=data.get('decisionType'),
            decision_date=data.get('decisionDate'),
            decision_mail_date=data.get('decisionMailDate'),
            document_type=data.get('documentType'),
            document_title=data.get('documentTitle'),
            patent_number=data.get('patentNumber'),
            application_number_text=data.get('applicationNumberText'),
            filing_date=data.get('filingDate'),
            proceeding_status=data.get('proceedingStatus'),
            petitioner_name=data.get('petitionerName'),
            patent_owner_name=data.get('patentOwnerName'),
            technology_center=data.get('technologyCenter'),
            art_unit=data.get('artUnit')
        )


@dataclass
class TrialDecisionResponseBag:
    """
    Response container for trial decision search results.
    """
    count: int = 0
    trial_decision_bag: List[TrialDecision] = field(default_factory=list)
    request_identifier: Optional[str] = None
    facets: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'TrialDecisionResponseBag':
        """
        Parse the search response data into a TrialDecisionResponseBag object.
        
        Args:
            data (dict): The raw JSON response from the API
            
        Returns:
            TrialDecisionResponseBag: A structured representation of the search results
        """
        result = cls(
            count=data.get('count', 0),
            request_identifier=data.get('requestIdentifier'),
            facets=data.get('facets')
        )
        
        # Parse trial decision bag (API uses camelCase: trialDecisionBag)
        if 'trialDecisionBag' in data:
            result.trial_decision_bag = [
                TrialDecision.from_dict(decision_data)
                for decision_data in data['trialDecisionBag']
            ]
        
        return result


@dataclass
class TrialDecisionIdentifierResponseBag:
    """
    Response container for individual trial decision lookup by document identifier.
    Similar to TrialDecisionResponseBag but for single record retrieval.
    """
    count: int = 0
    trial_decision_bag: List[TrialDecision] = field(default_factory=list)
    request_identifier: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'TrialDecisionIdentifierResponseBag':
        """
        Parse the individual trial decision response by document identifier.
        
        Args:
            data (dict): The raw JSON response from the API
            
        Returns:
            TrialDecisionIdentifierResponseBag: A structured representation of the trial decision
        """
        result = cls(
            count=data.get('count', 0),
            request_identifier=data.get('requestIdentifier')
        )
        
        # Parse trial decision bag (typically contains one record)
        if 'trialDecisionBag' in data:
            result.trial_decision_bag = [
                TrialDecision.from_dict(decision_data)
                for decision_data in data['trialDecisionBag']
            ]
        
        return result


@dataclass
class TrialDecisionByTrialResponseBag:
    """
    Response container for trial decisions lookup by trial number.
    Similar to TrialDecisionResponseBag but for decisions retrieved by trial number.
    """
    count: int = 0
    trial_decision_bag: List[TrialDecision] = field(default_factory=list)
    request_identifier: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'TrialDecisionByTrialResponseBag':
        """
        Parse the trial decisions response by trial number.
        
        Args:
            data (dict): The raw JSON response from the API
            
        Returns:
            TrialDecisionByTrialResponseBag: A structured representation of the trial decisions
        """
        result = cls(
            count=data.get('count', 0),
            request_identifier=data.get('requestIdentifier')
        )
        
        # Parse trial decision bag (may contain multiple decisions for a trial)
        if 'trialDecisionBag' in data:
            result.trial_decision_bag = [
                TrialDecision.from_dict(decision_data)
                for decision_data in data['trialDecisionBag']
            ]
        
        return result
