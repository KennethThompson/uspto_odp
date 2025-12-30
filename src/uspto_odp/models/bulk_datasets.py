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
class DatasetProduct:
    """
    Individual dataset product record.
    """
    product_identifier: Optional[str] = None
    product_name: Optional[str] = None
    product_description: Optional[str] = None
    product_type: Optional[str] = None
    product_category: Optional[str] = None
    release_date: Optional[str] = None
    last_updated: Optional[str] = None
    file_count: Optional[int] = None
    total_size: Optional[int] = None
    # Additional fields that may be present
    product_url: Optional[str] = None
    download_url: Optional[str] = None
    files: Optional[List[Dict[str, Any]]] = None
    metadata: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'DatasetProduct':
        """
        Parse a dataset product record from API response.
        
        Args:
            data (dict): Raw dictionary from API response
            
        Returns:
            DatasetProduct: Parsed dataset product record
        """
        return cls(
            product_identifier=data.get('productIdentifier'),
            product_name=data.get('productName'),
            product_description=data.get('productDescription'),
            product_type=data.get('productType'),
            product_category=data.get('productCategory'),
            release_date=data.get('releaseDate'),
            last_updated=data.get('lastUpdated'),
            file_count=data.get('fileCount'),
            total_size=data.get('totalSize'),
            product_url=data.get('productUrl'),
            download_url=data.get('downloadUrl'),
            files=data.get('files'),
            metadata=data.get('metadata')
        )


@dataclass
class DatasetProductSearchResponseBag:
    """
    Response container for dataset product search results.
    """
    count: int = 0
    dataset_product_bag: List[DatasetProduct] = field(default_factory=list)
    request_identifier: Optional[str] = None
    facets: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'DatasetProductSearchResponseBag':
        """
        Parse the search response data into a DatasetProductSearchResponseBag object.
        
        Args:
            data (dict): The raw JSON response from the API
            
        Returns:
            DatasetProductSearchResponseBag: A structured representation of the search results
        """
        result = cls(
            count=data.get('count', 0),
            request_identifier=data.get('requestIdentifier'),
            facets=data.get('facets')
        )
        
        # Parse dataset product bag (API uses camelCase: datasetProductBag)
        if 'datasetProductBag' in data:
            result.dataset_product_bag = [
                DatasetProduct.from_dict(product_data)
                for product_data in data['datasetProductBag']
            ]
        elif 'productBag' in data:
            # Alternative field name
            result.dataset_product_bag = [
                DatasetProduct.from_dict(product_data)
                for product_data in data['productBag']
            ]
        
        return result


@dataclass
class DatasetProductResponseBag:
    """
    Response container for individual dataset product lookup by product identifier.
    Similar to DatasetProductSearchResponseBag but for single record retrieval.
    """
    count: int = 0
    dataset_product_bag: List[DatasetProduct] = field(default_factory=list)
    request_identifier: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'DatasetProductResponseBag':
        """
        Parse the individual dataset product response by product identifier.
        
        Args:
            data (dict): The raw JSON response from the API
            
        Returns:
            DatasetProductResponseBag: A structured representation of the dataset product
        """
        result = cls(
            count=data.get('count', 0),
            request_identifier=data.get('requestIdentifier')
        )
        
        # Parse dataset product bag (typically contains one record)
        if 'datasetProductBag' in data:
            result.dataset_product_bag = [
                DatasetProduct.from_dict(product_data)
                for product_data in data['datasetProductBag']
            ]
        elif 'productBag' in data:
            # Alternative field name
            result.dataset_product_bag = [
                DatasetProduct.from_dict(product_data)
                for product_data in data['productBag']
            ]
        elif 'product' in data:
            # Single product object
            result.dataset_product_bag = [DatasetProduct.from_dict(data['product'])]
            result.count = 1
        
        return result


@dataclass
class DatasetFileResponseBag:
    """
    Response container for dataset file download.
    This may contain file metadata or binary data information.
    """
    file_name: Optional[str] = None
    file_url: Optional[str] = None
    file_size: Optional[int] = None
    content_type: Optional[str] = None
    download_url: Optional[str] = None
    request_identifier: Optional[str] = None
    # Additional metadata
    metadata: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'DatasetFileResponseBag':
        """
        Parse the dataset file response.
        
        Args:
            data (dict): The raw JSON response from the API
            
        Returns:
            DatasetFileResponseBag: A structured representation of the file response
        """
        return cls(
            file_name=data.get('fileName') or data.get('filename'),
            file_url=data.get('fileUrl') or data.get('file_url'),
            file_size=data.get('fileSize') or data.get('file_size'),
            content_type=data.get('contentType') or data.get('content_type'),
            download_url=data.get('downloadUrl') or data.get('download_url'),
            request_identifier=data.get('requestIdentifier'),
            metadata=data.get('metadata')
        )
