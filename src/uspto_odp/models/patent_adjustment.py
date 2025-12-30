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
from typing import List, Optional
from datetime import date


@dataclass
class PatentTermAdjustment:
    """Represents patent term adjustment data for a patent application"""
    # PTA (Patent Term Adjustment) fields
    pta_days: Optional[int] = None
    pta_type_a_days: Optional[int] = None  # Type A delays (USPTO delays)
    pta_type_b_days: Optional[int] = None  # Type B delays (applicant delays)
    pta_type_c_days: Optional[int] = None  # Type C delays (overlap)
    
    # PTE (Patent Term Extension) fields
    pte_days: Optional[int] = None
    pte_type: Optional[str] = None
    
    # Dates
    grant_date: Optional[date] = None
    issue_date: Optional[date] = None
    adjustment_date: Optional[date] = None
    
    # Reason codes and descriptions
    adjustment_reason_codes: List[str] = field(default_factory=list)
    adjustment_reason_descriptions: List[str] = field(default_factory=list)
    
    # Total adjustment
    total_adjustment_days: Optional[int] = None
    
    # Other fields that may be present
    patent_number: Optional[str] = None
    application_number: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'PatentTermAdjustment':
        """
        Parse patent term adjustment data from API response.
        Handles various field name variations that may exist in the API.
        """
        # Helper to safely parse dates
        def parse_date(date_str):
            if date_str:
                try:
                    return date.fromisoformat(date_str)
                except (ValueError, TypeError):
                    return None
            return None
        
        # Helper to get integer value safely
        def get_int(key, alt_keys=None):
            if key in data and data[key] is not None:
                try:
                    return int(data[key])
                except (ValueError, TypeError):
                    pass
            if alt_keys:
                for alt_key in alt_keys:
                    if alt_key in data and data[alt_key] is not None:
                        try:
                            return int(data[alt_key])
                        except (ValueError, TypeError):
                            pass
            return None
        
        # Helper to get list value
        def get_list(key, alt_keys=None):
            value = data.get(key)
            if isinstance(value, list):
                return value
            if alt_keys:
                for alt_key in alt_keys:
                    value = data.get(alt_key)
                    if isinstance(value, list):
                        return value
            return []
        
        return cls(
            pta_days=get_int('ptaDays', ['pta_days', 'PTADays']),
            pta_type_a_days=get_int('ptaTypeADays', ['pta_type_a_days', 'PTATypeADays']),
            pta_type_b_days=get_int('ptaTypeBDays', ['pta_type_b_days', 'PTATypeBDays']),
            pta_type_c_days=get_int('ptaTypeCDays', ['pta_type_c_days', 'PTATypeCDays']),
            pte_days=get_int('pteDays', ['pte_days', 'PTEDays']),
            pte_type=data.get('pteType') or data.get('pte_type') or data.get('PTEType'),
            grant_date=parse_date(data.get('grantDate') or data.get('grant_date')),
            issue_date=parse_date(data.get('issueDate') or data.get('issue_date')),
            adjustment_date=parse_date(data.get('adjustmentDate') or data.get('adjustment_date')),
            adjustment_reason_codes=get_list('adjustmentReasonCodes', ['adjustment_reason_codes', 'reasonCodes']),
            adjustment_reason_descriptions=get_list('adjustmentReasonDescriptions', ['adjustment_reason_descriptions', 'reasonDescriptions']),
            total_adjustment_days=get_int('totalAdjustmentDays', ['total_adjustment_days', 'totalDays']),
            patent_number=data.get('patentNumber') or data.get('patent_number'),
            application_number=data.get('applicationNumber') or data.get('application_number')
        )


@dataclass
class ApplicationAdjustment:
    """Represents adjustment data for a patent application"""
    application_number: str
    patent_term_adjustment: Optional[PatentTermAdjustment] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'ApplicationAdjustment':
        return cls(
            application_number=data.get('applicationNumberText', ''),
            patent_term_adjustment=PatentTermAdjustment.from_dict(
                data.get('patentTermAdjustmentData', {})
            ) if data.get('patentTermAdjustmentData') else None
        )


@dataclass
class AdjustmentResponse:
    """Response model for the /adjustment endpoint"""
    count: int
    adjustments: List[ApplicationAdjustment] = field(default_factory=list)
    request_identifier: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'AdjustmentResponse':
        """
        Parse the adjustment endpoint response.
        
        The API returns:
        {
            "count": 1,
            "patentFileWrapperDataBag": [
                {
                    "applicationNumberText": "...",
                    "patentTermAdjustmentData": {...}
                }
            ],
            "requestIdentifier": "..."
        }
        """
        return cls(
            count=data.get('count', 0),
            adjustments=[ApplicationAdjustment.from_dict(pw) 
                        for pw in data.get('patentFileWrapperDataBag', [])],
            request_identifier=data.get('requestIdentifier')
        )
