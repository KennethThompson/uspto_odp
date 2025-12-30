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
class PatentDataResponse:
    """
    Response model for the /search/download endpoint.
    This is similar to the regular search response but optimized for downloads.
    """
    count: int
    patent_file_wrapper_data_bag: List[Dict[str, Any]] = field(default_factory=list)
    request_identifier: Optional[str] = None
    # Additional fields that may be present in download responses
    download_url: Optional[str] = None
    download_format: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'PatentDataResponse':
        """
        Parse the search/download endpoint response.
        
        The API returns:
        {
            "count": 123,
            "patentFileWrapperDataBag": [...],
            "requestIdentifier": "...",
            "downloadUrl": "..." (optional, for CSV format)
        }
        """
        return cls(
            count=data.get('count', 0),
            patent_file_wrapper_data_bag=data.get('patentFileWrapperDataBag', []),
            request_identifier=data.get('requestIdentifier'),
            download_url=data.get('downloadUrl'),
            download_format=data.get('format')
        )
