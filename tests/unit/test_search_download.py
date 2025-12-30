"""
Unit tests for search/download endpoint.
"""
import pytest
from unittest.mock import Mock, AsyncMock
import aiohttp
from uspto_odp.controller.uspto_odp_client import USPTOClient, USPTOError
from uspto_odp.models.patent_search_download import PatentDataResponse


@pytest.fixture
def client():
    api_key = "test_api_key"
    mock_session = Mock(spec=aiohttp.ClientSession)
    return USPTOClient(api_key=api_key, session=mock_session), mock_session


@pytest.mark.asyncio
async def test_search_patent_applications_download_post_success(client):
    """Test search_patent_applications_download POST method with successful response"""
    client, mock_session = client
    
    # Create mock response data
    mock_response_data = {
        "count": 2,
        "patentFileWrapperDataBag": [
            {
                "applicationNumberText": "14412875",
                "applicationMetaData": {
                    "patentNumber": "9022434",
                    "filingDate": "2014-12-31"
                }
            },
            {
                "applicationNumberText": "14412876",
                "applicationMetaData": {
                    "patentNumber": "9022435",
                    "filingDate": "2014-12-31"
                }
            }
        ],
        "requestIdentifier": "test-download-request-id"
    }
    
    # Create mock response
    mock_response = Mock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value=mock_response_data)
    
    # Create async context manager mock
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = mock_response
    mock_session.post.return_value = async_cm
    
    # Execute test
    payload = {
        "q": "applicationNumberText:14412875",
        "pagination": {
            "offset": 0,
            "limit": 10
        }
    }
    result = await client.search_patent_applications_download(payload)
    
    # Assertions
    assert result is not None
    assert isinstance(result, PatentDataResponse)
    assert result.count == 2
    assert len(result.patent_file_wrapper_data_bag) == 2
    assert result.request_identifier == "test-download-request-id"
    assert result.patent_file_wrapper_data_bag[0]["applicationNumberText"] == "14412875"
    
    # Verify POST was called with correct URL and payload
    assert mock_session.post.call_count == 1
    args, kwargs = mock_session.post.call_args_list[0]
    assert "search" in args[0] or "search" in str(args[0])
    assert "download" in args[0] or "download" in str(args[0])
    assert kwargs["json"] == payload
    assert kwargs["headers"]["X-API-KEY"] == "test_api_key"


@pytest.mark.asyncio
async def test_search_patent_applications_download_get_success(client):
    """Test search_patent_applications_download_get GET method with successful response"""
    client, mock_session = client
    
    # Create mock response data
    mock_response_data = {
        "count": 1,
        "patentFileWrapperDataBag": [
            {
                "applicationNumberText": "14412875",
                "applicationMetaData": {
                    "patentNumber": "9022434",
                    "filingDate": "2014-12-31"
                }
            }
        ],
        "requestIdentifier": "test-download-get-request-id"
    }
    
    # Create mock response
    mock_response = Mock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value=mock_response_data)
    
    # Create async context manager mock
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = mock_response
    mock_session.get.return_value = async_cm
    
    # Execute test
    result = await client.search_patent_applications_download_get(
        q="applicationNumberText:14412875",
        format="json"
    )
    
    # Assertions
    assert result is not None
    assert isinstance(result, PatentDataResponse)
    assert result.count == 1
    assert len(result.patent_file_wrapper_data_bag) == 1
    
    # Verify GET was called with correct URL and parameters
    assert mock_session.get.call_count == 1
    args, kwargs = mock_session.get.call_args_list[0]
    assert "search" in args[0] or "search" in str(args[0])
    assert "download" in args[0] or "download" in str(args[0])
    assert kwargs["params"]["q"] == "applicationNumberText:14412875"
    assert kwargs["params"]["format"] == "json"
    assert kwargs["headers"]["X-API-KEY"] == "test_api_key"


@pytest.mark.asyncio
async def test_search_patent_applications_download_get_csv_format(client):
    """Test search_patent_applications_download_get with CSV format"""
    client, mock_session = client
    
    # Create mock response data for CSV format (may include downloadUrl)
    mock_response_data = {
        "count": 10,
        "downloadUrl": "https://example.com/download/file.csv",
        "format": "csv",
        "requestIdentifier": "test-csv-download-id"
    }
    
    mock_response = Mock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value=mock_response_data)
    
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = mock_response
    mock_session.get.return_value = async_cm
    
    result = await client.search_patent_applications_download_get(
        q="Utility",
        format="csv",
        limit=100
    )
    
    assert result is not None
    assert result.count == 10
    assert result.download_url == "https://example.com/download/file.csv"
    assert result.download_format == "csv"
    
    # Verify format parameter was passed
    args, kwargs = mock_session.get.call_args_list[0]
    assert kwargs["params"]["format"] == "csv"
    assert kwargs["params"]["limit"] == 100


@pytest.mark.asyncio
async def test_search_patent_applications_download_get_all_params(client):
    """Test search_patent_applications_download_get with all parameters"""
    client, mock_session = client
    
    mock_response_data = {
        "count": 5,
        "patentFileWrapperDataBag": [],
        "requestIdentifier": "test-all-params-id"
    }
    
    mock_response = Mock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value=mock_response_data)
    
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = mock_response
    mock_session.get.return_value = async_cm
    
    result = await client.search_patent_applications_download_get(
        q="Utility",
        sort="applicationMetaData.filingDate desc",
        offset=10,
        limit=50,
        facets="applicationMetaData.applicationTypeCode",
        fields="applicationNumberText,applicationMetaData.patentNumber",
        filters="applicationMetaData.applicationTypeCode UTL",
        range_filters="applicationMetaData.grantDate 2010-01-01:2011-01-01",
        format="json"
    )
    
    assert result is not None
    assert result.count == 5
    
    # Verify all parameters were passed
    args, kwargs = mock_session.get.call_args_list[0]
    params = kwargs["params"]
    assert params["q"] == "Utility"
    assert params["sort"] == "applicationMetaData.filingDate desc"
    assert params["offset"] == 10
    assert params["limit"] == 50
    assert params["facets"] == "applicationMetaData.applicationTypeCode"
    assert params["fields"] == "applicationNumberText,applicationMetaData.patentNumber"
    assert params["filters"] == "applicationMetaData.applicationTypeCode UTL"
    assert params["rangeFilters"] == "applicationMetaData.grantDate 2010-01-01:2011-01-01"
    assert params["format"] == "json"


@pytest.mark.asyncio
async def test_search_patent_applications_download_post_error(client):
    """Test search_patent_applications_download POST method with error"""
    client, mock_session = client
    
    mock_error_data = {
        "code": 400,
        "error": "Bad Request",
        "errorDetails": "Invalid search payload",
        "requestIdentifier": "test-error-id"
    }
    
    mock_response = Mock()
    mock_response.status = 400
    mock_response.json = AsyncMock(return_value=mock_error_data)
    
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = mock_response
    mock_session.post.return_value = async_cm
    
    with pytest.raises(USPTOError) as exc_info:
        await client.search_patent_applications_download({"invalid": "payload"})
    
    assert exc_info.value.code == 400
    assert "Bad Request" in str(exc_info.value)


@pytest.mark.asyncio
async def test_search_patent_applications_download_get_error(client):
    """Test search_patent_applications_download_get GET method with error"""
    client, mock_session = client
    
    mock_error_data = {
        "code": 404,
        "error": "Not Found",
        "errorDetails": "No matching records found",
        "requestIdentifier": "test-error-id"
    }
    
    mock_response = Mock()
    mock_response.status = 404
    mock_response.json = AsyncMock(return_value=mock_error_data)
    
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = mock_response
    mock_session.get.return_value = async_cm
    
    with pytest.raises(USPTOError) as exc_info:
        await client.search_patent_applications_download_get(q="invalid:query")
    
    assert exc_info.value.code == 404
    assert "Not Found" in str(exc_info.value)
