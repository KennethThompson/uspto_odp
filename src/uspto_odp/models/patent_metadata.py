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
FITNESS FOR ANY PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
from dataclasses import dataclass, field
from typing import Optional
from uspto_odp.models.patent_file_wrapper import ApplicationMetadata

@dataclass
class ApplicationMetadataResponse:
    """
    Response model for the /meta-data endpoint.
    Contains application number and metadata.
    """
    application_number: str
    metadata: ApplicationMetadata
    request_identifier: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'ApplicationMetadataResponse':
        """
        Parse the meta-data endpoint response.
        
        The API returns:
        {
            "count": 1,
            "patentFileWrapperDataBag": [
                {
                    "applicationNumberText": "...",
                    "applicationMetaData": {...}
                }
            ],
            "requestIdentifier": "..."
        }
        """
        wrapper_data = data.get('patentFileWrapperDataBag', [{}])[0]
        
        return cls(
            application_number=wrapper_data.get('applicationNumberText', ''),
            metadata=ApplicationMetadata.from_dict(wrapper_data.get('applicationMetaData', {})),
            request_identifier=data.get('requestIdentifier')
        )
