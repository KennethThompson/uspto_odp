"""
Unit tests for Bulk Datasets endpoints.
"""
import pytest
from unittest.mock import Mock, AsyncMock
import aiohttp
from uspto_odp.controller.uspto_odp_client import USPTOClient, USPTOError
from uspto_odp.models.bulk_datasets import (
    DatasetProductSearchResponseBag,
    DatasetProductResponseBag,
    DatasetFileResponseBag,
    DatasetProduct
)


@pytest.fixture
def client():
    api_key = "test_api_key"
    mock_session = Mock(spec=aiohttp.ClientSession)
    return USPTOClient(api_key=api_key, session=mock_session), mock_session


@pytest.mark.asyncio
async def test_search_dataset_products_get_success(client):
    """Test search_dataset_products_get GET method with successful response"""
    client, mock_session = client
    
    mock_response_data = {
        "count": 2,
        "datasetProductBag": [
            {
                "productIdentifier": "product-001",
                "productName": "Patent Data 2020",
                "productType": "Patent",
                "releaseDate": "2020-01-15",
                "fileCount": 10
            },
            {
                "productIdentifier": "product-002",
                "productName": "Trademark Data 2020",
                "productType": "Trademark",
                "releaseDate": "2020-02-20",
                "fileCount": 5
            }
        ],
        "requestIdentifier": "test-request-id"
    }
    
    mock_response = Mock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value=mock_response_data)
    
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = mock_response
    mock_session.get.return_value = async_cm
    
    result = await client.search_dataset_products_get(q="Patent")
    
    assert result is not None
    assert isinstance(result, DatasetProductSearchResponseBag)
    assert result.count == 2
    assert len(result.dataset_product_bag) == 2
    assert result.request_identifier == "test-request-id"
    assert result.dataset_product_bag[0].product_identifier == "product-001"
    
    assert mock_session.get.call_count == 1
    args, kwargs = mock_session.get.call_args_list[0]
    assert "search" in args[0] or "search" in str(args[0])
    assert kwargs["params"]["q"] == "Patent"
    assert kwargs["headers"]["X-API-KEY"] == "test_api_key"


@pytest.mark.asyncio
async def test_search_dataset_products_get_all_params(client):
    """Test search_dataset_products_get with all parameters"""
    client, mock_session = client
    
    mock_response_data = {
        "count": 5,
        "datasetProductBag": [],
        "requestIdentifier": "test-all-params-id"
    }
    
    mock_response = Mock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value=mock_response_data)
    
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = mock_response
    mock_session.get.return_value = async_cm
    
    result = await client.search_dataset_products_get(
        q="Patent",
        sort="releaseDate desc",
        offset=10,
        limit=50,
        facets="productType",
        fields="productIdentifier,productName",
        filters="productType Patent",
        range_filters="releaseDate 2021-01-01:2025-01-01"
    )
    
    assert result is not None
    assert result.count == 5
    
    args, kwargs = mock_session.get.call_args_list[0]
    params = kwargs["params"]
    assert params["q"] == "Patent"
    assert params["sort"] == "releaseDate desc"
    assert params["offset"] == 10
    assert params["limit"] == 50
    assert params["facets"] == "productType"
    assert params["fields"] == "productIdentifier,productName"
    assert params["filters"] == "productType Patent"
    assert params["rangeFilters"] == "releaseDate 2021-01-01:2025-01-01"


@pytest.mark.asyncio
async def test_get_dataset_product_success(client):
    """Test get_dataset_product with successful response"""
    client, mock_session = client
    
    mock_response_data = {
        "count": 1,
        "datasetProductBag": [
            {
                "productIdentifier": "product-001",
                "productName": "Patent Data 2020",
                "productType": "Patent",
                "productDescription": "Patent application data for 2020",
                "releaseDate": "2020-01-15",
                "fileCount": 10,
                "totalSize": 1000000
            }
        ],
        "requestIdentifier": "test-get-product-id"
    }
    
    mock_response = Mock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value=mock_response_data)
    
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = mock_response
    mock_session.get.return_value = async_cm
    
    product_identifier = "product-001"
    result = await client.get_dataset_product(product_identifier)
    
    assert result is not None
    assert isinstance(result, DatasetProductResponseBag)
    assert result.count == 1
    assert len(result.dataset_product_bag) == 1
    assert result.dataset_product_bag[0].product_identifier == product_identifier
    
    args, kwargs = mock_session.get.call_args_list[0]
    assert product_identifier in args[0] or product_identifier in str(args[0])


@pytest.mark.asyncio
async def test_get_dataset_file_success(client):
    """Test get_dataset_file with successful response"""
    client, mock_session = client
    
    mock_response_data = {
        "fileName": "data.csv",
        "fileUrl": "https://example.com/files/data.csv",
        "fileSize": 50000,
        "contentType": "text/csv",
        "downloadUrl": "https://example.com/download/data.csv",
        "requestIdentifier": "test-get-file-id"
    }
    
    mock_response = Mock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value=mock_response_data)
    
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = mock_response
    mock_session.get.return_value = async_cm
    
    product_identifier = "product-001"
    file_name = "data.csv"
    result = await client.get_dataset_file(product_identifier, file_name)
    
    assert result is not None
    assert isinstance(result, DatasetFileResponseBag)
    assert result.file_name == file_name
    assert result.file_size == 50000
    assert result.download_url == "https://example.com/download/data.csv"
    
    args, kwargs = mock_session.get.call_args_list[0]
    assert product_identifier in args[0] or product_identifier in str(args[0])
    assert file_name in args[0] or file_name in str(args[0])


@pytest.mark.asyncio
async def test_search_dataset_products_error_handling(client):
    """Test search_dataset_products_get with error response"""
    client, mock_session = client
    
    mock_error_data = {
        "code": 400,
        "error": "Bad Request",
        "errorDetails": "Invalid search query",
        "requestIdentifier": "test-error-id"
    }
    
    mock_response = Mock()
    mock_response.status = 400
    mock_response.json = AsyncMock(return_value=mock_error_data)
    
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = mock_response
    mock_session.get.return_value = async_cm
    
    with pytest.raises(USPTOError) as exc_info:
        await client.search_dataset_products_get(q="invalid:query:format")
    
    assert exc_info.value.code == 400
    assert "Bad Request" in str(exc_info.value)


@pytest.mark.asyncio
async def test_get_dataset_product_error_handling(client):
    """Test get_dataset_product with error response"""
    client, mock_session = client
    
    mock_error_data = {
        "code": 404,
        "error": "Not Found",
        "errorDetails": "Dataset product not found",
        "requestIdentifier": "test-error-id"
    }
    
    mock_response = Mock()
    mock_response.status = 404
    mock_response.json = AsyncMock(return_value=mock_error_data)
    
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = mock_response
    mock_session.get.return_value = async_cm
    
    with pytest.raises(USPTOError) as exc_info:
        await client.get_dataset_product("invalid-product-id")
    
    assert exc_info.value.code == 404
    assert "Not Found" in str(exc_info.value)


@pytest.mark.asyncio
async def test_get_dataset_file_error_handling(client):
    """Test get_dataset_file with error response"""
    client, mock_session = client
    
    mock_error_data = {
        "code": 404,
        "error": "Not Found",
        "errorDetails": "Dataset file not found",
        "requestIdentifier": "test-error-id"
    }
    
    mock_response = Mock()
    mock_response.status = 404
    mock_response.json = AsyncMock(return_value=mock_error_data)
    
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = mock_response
    mock_session.get.return_value = async_cm
    
    with pytest.raises(USPTOError) as exc_info:
        await client.get_dataset_file("product-001", "nonexistent.csv")
    
    assert exc_info.value.code == 404
    assert "Not Found" in str(exc_info.value)
