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
class StatusCode:
    """
    Represents a single patent application status code entry.
    
    Attributes:
        application_status_code: The numeric status code
        application_status_description_text: The description of the status code
    """
    application_status_code: int
    application_status_description_text: str

    @classmethod
    def from_dict(cls, data: dict) -> 'StatusCode':
        """
        Create a StatusCode instance from a dictionary.
        
        Args:
            data: Dictionary containing status code data from API response
            
        Returns:
            StatusCode instance
        """
        return cls(
            application_status_code=data.get('applicationStatusCode', 0),
            application_status_description_text=data.get('applicationStatusDescriptionText', '')
        )


@dataclass
class StatusCodeCollection:
    """
    Collection of patent application status codes returned from search.
    
    Attributes:
        count: Total number of status codes matching the search criteria
        status_codes: List of StatusCode objects
        request_identifier: Optional request identifier from the API
    """
    count: int
    status_codes: List[StatusCode] = field(default_factory=list)
    request_identifier: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'StatusCodeCollection':
        """
        Create a StatusCodeCollection instance from a dictionary.
        
        Args:
            data: Dictionary containing status code collection data from API response
            
        Returns:
            StatusCodeCollection instance
        """
        return cls(
            count=data.get('count', 0),
            status_codes=[StatusCode.from_dict(sc) 
                         for sc in data.get('statusCodeDataBag', [])],
            request_identifier=data.get('requestIdentifier')
        )
