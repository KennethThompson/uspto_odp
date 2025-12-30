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
class PetitionDecision:
    """
    Individual petition decision record.
    """
    petition_decision_record_identifier: Optional[str] = None
    patent_number: Optional[str] = None
    application_number_text: Optional[str] = None
    first_applicant_name: Optional[str] = None
    petition_mail_date: Optional[str] = None
    decision_type_code: Optional[int] = None
    decision_type_code_description_text: Optional[str] = None
    decision_date: Optional[str] = None
    decision_mail_date: Optional[str] = None
    final_deciding_office_name: Optional[str] = None
    petition_issue_considered_text_bag: List[str] = field(default_factory=list)
    technology_center: Optional[str] = None
    business_entity_status_category: Optional[str] = None
    decision_petition_type_code: Optional[str] = None
    decision_petition_type_code_description: Optional[str] = None
    prosecution_status_code_description_text: Optional[str] = None
    court_action_indicator: Optional[bool] = None
    action_taken_by_court_name: Optional[str] = None
    rule_bag: List[str] = field(default_factory=list)
    statute_bag: List[str] = field(default_factory=list)
    # Additional fields that may be present
    documents: Optional[List[Dict[str, Any]]] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'PetitionDecision':
        """
        Parse a petition decision record from API response.
        
        Args:
            data (dict): Raw dictionary from API response
            
        Returns:
            PetitionDecision: Parsed petition decision record
        """
        return cls(
            petition_decision_record_identifier=data.get('petitionDecisionRecordIdentifier'),
            patent_number=data.get('patentNumber'),
            application_number_text=data.get('applicationNumberText'),
            first_applicant_name=data.get('firstApplicantName'),
            petition_mail_date=data.get('petitionMailDate'),
            decision_type_code=data.get('decisionTypeCode'),
            decision_type_code_description_text=data.get('decisionTypeCodeDescriptionText'),
            decision_date=data.get('decisionDate'),
            decision_mail_date=data.get('decisionMailDate'),
            final_deciding_office_name=data.get('finalDecidingOfficeName'),
            petition_issue_considered_text_bag=data.get('petitionIssueConsideredTextBag', []),
            technology_center=data.get('technologyCenter'),
            business_entity_status_category=data.get('businessEntityStatusCategory'),
            decision_petition_type_code=data.get('decisionPetitionTypeCode'),
            decision_petition_type_code_description=data.get('decisionPetitionTypeCodeDescription'),
            prosecution_status_code_description_text=data.get('prosecutionStatusCodeDescriptionText'),
            court_action_indicator=data.get('courtActionIndicator'),
            action_taken_by_court_name=data.get('actionTakenByCourtName'),
            rule_bag=data.get('ruleBag', []),
            statute_bag=data.get('statuteBag', []),
            documents=data.get('documents')
        )


@dataclass
class PetitionDecisionResponseBag:
    """
    Response container for petition decision search results.
    """
    count: int = 0
    petition_decision_bag: List[PetitionDecision] = field(default_factory=list)
    request_identifier: Optional[str] = None
    facets: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'PetitionDecisionResponseBag':
        """
        Parse the search response data into a PetitionDecisionResponseBag object.
        
        Args:
            data (dict): The raw JSON response from the API
            
        Returns:
            PetitionDecisionResponseBag: A structured representation of the search results
        """
        result = cls(
            count=data.get('count', 0),
            request_identifier=data.get('requestIdentifier'),
            facets=data.get('facets')
        )
        
        # Parse petition decision bag
        if 'petitionDecisionBag' in data:
            result.petition_decision_bag = [
                PetitionDecision.from_dict(decision_data)
                for decision_data in data['petitionDecisionBag']
            ]
        
        return result


@dataclass
class PetitionDecisionIdentifierResponseBag:
    """
    Response container for individual petition decision lookup.
    Similar to PetitionDecisionResponseBag but for single record retrieval.
    """
    count: int = 0
    petition_decision_bag: List[PetitionDecision] = field(default_factory=list)
    request_identifier: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'PetitionDecisionIdentifierResponseBag':
        """
        Parse the individual petition decision response.
        
        Args:
            data (dict): The raw JSON response from the API
            
        Returns:
            PetitionDecisionIdentifierResponseBag: A structured representation of the petition decision
        """
        result = cls(
            count=data.get('count', 0),
            request_identifier=data.get('requestIdentifier')
        )
        
        # Parse petition decision bag (typically contains one record)
        if 'petitionDecisionBag' in data:
            result.petition_decision_bag = [
                PetitionDecision.from_dict(decision_data)
                for decision_data in data['petitionDecisionBag']
            ]
        
        return result
