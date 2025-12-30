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


@dataclass
class AttorneyAddress:
    """Represents an attorney/agent address"""
    address_line_one: Optional[str] = None
    address_line_two: Optional[str] = None
    address_line_three: Optional[str] = None
    city_name: Optional[str] = None
    geographic_region_code: Optional[str] = None
    postal_code: Optional[str] = None
    country_code: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'AttorneyAddress':
        return cls(
            address_line_one=data.get('addressLineOneText'),
            address_line_two=data.get('addressLineTwoText'),
            address_line_three=data.get('addressLineThreeText'),
            city_name=data.get('cityName'),
            geographic_region_code=data.get('geographicRegionCode'),
            postal_code=data.get('postalCode'),
            country_code=data.get('countryCode')
        )


@dataclass
class RecordAttorney:
    """Represents attorney/agent information for a patent application"""
    attorney_name: Optional[str] = None
    registration_number: Optional[str] = None
    attorney_docket_number: Optional[str] = None
    address: Optional[AttorneyAddress] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    attorney_type: Optional[str] = None  # e.g., "Attorney" or "Agent"

    @classmethod
    def from_dict(cls, data: dict) -> 'RecordAttorney':
        address_data = data.get('attorneyAddress') or data.get('address') or {}
        return cls(
            attorney_name=data.get('attorneyNameText') or data.get('attorneyName'),
            registration_number=data.get('attorneyRegistrationNumber') or data.get('registrationNumber'),
            attorney_docket_number=data.get('attorneyDocketNumber') or data.get('docketNumber'),
            address=AttorneyAddress.from_dict(address_data) if address_data else None,
            phone_number=data.get('attorneyPhoneNumber') or data.get('phoneNumber'),
            email=data.get('attorneyEmail') or data.get('email'),
            attorney_type=data.get('attorneyType') or data.get('type')
        )


@dataclass
class ApplicationAttorney:
    """Represents attorney data for a patent application"""
    application_number: str
    record_attorney: Optional[RecordAttorney] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'ApplicationAttorney':
        return cls(
            application_number=data.get('applicationNumberText', ''),
            record_attorney=RecordAttorney.from_dict(data.get('recordAttorney', {}))
        )


@dataclass
class AttorneyResponse:
    """Response model for the /attorney endpoint"""
    count: int
    attorneys: List[ApplicationAttorney] = field(default_factory=list)
    request_identifier: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'AttorneyResponse':
        """
        Parse the attorney endpoint response.
        
        The API returns:
        {
            "count": 1,
            "patentFileWrapperDataBag": [
                {
                    "applicationNumberText": "...",
                    "recordAttorney": {...}
                }
            ],
            "requestIdentifier": "..."
        }
        """
        return cls(
            count=data.get('count', 0),
            attorneys=[ApplicationAttorney.from_dict(pw) 
                      for pw in data.get('patentFileWrapperDataBag', [])],
            request_identifier=data.get('requestIdentifier')
        )
