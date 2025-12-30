"""
Unit tests for status codes endpoint.
These tests use mocks and do not require API access.
"""
import pytest
from unittest.mock import Mock, AsyncMock
import aiohttp
from uspto_odp.controller.uspto_odp_client import USPTOClient, USPTOError
from uspto_odp.models.patent_status_codes import StatusCode, StatusCodeCollection


@pytest.fixture
def client():
    api_key = "test_api_key"
    mock_session = Mock(spec=aiohttp.ClientSession)
    return USPTOClient(api_key=api_key, session=mock_session), mock_session


@pytest.mark.asyncio
async def test_search_status_codes_get_success(client):
    """Test GET /status-codes endpoint with query parameters"""
    client, mock_session = client
    
    # Create mock response data matching USPTO API response format
    mock_response_data = {
        "count": 2,
        "statusCodeDataBag": [
            {
                "applicationStatusCode": 150,
                "applicationStatusDescriptionText": "Patented Case"
            },
            {
                "applicationStatusCode": 161,
                "applicationStatusDescriptionText": "Abandoned -- Failure to Respond to an Office Action"
            }
        ],
        "requestIdentifier": "test-request-id"
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
    result = await client.search_status_codes_get(q="applicationStatusDescriptionText:Patented")
    
    # Assertions
    assert result is not None
    assert isinstance(result, StatusCodeCollection)
    assert result.count == 2
    assert len(result.status_codes) == 2
    assert result.request_identifier == "test-request-id"
    
    # Verify status code structure
    assert result.status_codes[0].application_status_code == 150
    assert result.status_codes[0].application_status_description_text == "Patented Case"
    assert result.status_codes[1].application_status_code == 161
    
    # Verify API call was made with correct parameters
    mock_session.get.assert_called_once()
    call_args = mock_session.get.call_args
    assert call_args[0][0].endswith("/status-codes")
    assert call_args[1]["params"]["q"] == "applicationStatusDescriptionText:Patented"
    mock_response.json.assert_called_once()


@pytest.mark.asyncio
async def test_search_status_codes_get_with_pagination(client):
    """Test GET /status-codes endpoint with pagination parameters"""
    client, mock_session = client
    
    # Create mock response data
    mock_response_data = {
        "count": 100,
        "statusCodeDataBag": [
            {
                "applicationStatusCode": i,
                "applicationStatusDescriptionText": f"Status {i}"
            } for i in range(10)
        ],
        "requestIdentifier": "test-request-id"
    }
    
    # Create mock response
    mock_response = Mock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value=mock_response_data)
    
    # Create async context manager mock
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = mock_response
    mock_session.get.return_value = async_cm
    
    # Execute test with pagination
    result = await client.search_status_codes_get(
        q="applicationStatusCode:>100",
        offset=10,
        limit=10
    )
    
    # Assertions
    assert result is not None
    assert result.count == 100
    assert len(result.status_codes) == 10
    
    # Verify API call was made with pagination parameters
    mock_session.get.assert_called_once()
    call_args = mock_session.get.call_args
    params = call_args[1]["params"]
    assert params["q"] == "applicationStatusCode:>100"
    assert params["offset"] == 10
    assert params["limit"] == 10


@pytest.mark.asyncio
async def test_search_status_codes_get_no_params(client):
    """Test GET /status-codes endpoint with no parameters"""
    client, mock_session = client
    
    # Create mock response data
    mock_response_data = {
        "count": 50,
        "statusCodeDataBag": [
            {
                "applicationStatusCode": 150,
                "applicationStatusDescriptionText": "Patented Case"
            }
        ],
        "requestIdentifier": "test-request-id"
    }
    
    # Create mock response
    mock_response = Mock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value=mock_response_data)
    
    # Create async context manager mock
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = mock_response
    mock_session.get.return_value = async_cm
    
    # Execute test with no parameters
    result = await client.search_status_codes_get()
    
    # Assertions
    assert result is not None
    assert result.count == 50
    
    # Verify API call was made with empty params
    mock_session.get.assert_called_once()
    call_args = mock_session.get.call_args
    params = call_args[1]["params"]
    assert params == {}  # No parameters should be sent


@pytest.mark.asyncio
async def test_search_status_codes_post_success(client):
    """Test POST /status-codes endpoint with JSON payload"""
    client, mock_session = client
    
    # Create mock response data
    mock_response_data = {
        "count": 1,
        "statusCodeDataBag": [
            {
                "applicationStatusCode": 150,
                "applicationStatusDescriptionText": "Patented Case"
            }
        ],
        "requestIdentifier": "test-request-id"
    }
    
    # Create mock response
    mock_response = Mock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value=mock_response_data)
    
    # Create async context manager mock
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = mock_response
    mock_session.post.return_value = async_cm
    
    # Create payload
    payload = {
        "q": "applicationStatusCode:150",
        "pagination": {
            "offset": 0,
            "limit": 25
        }
    }
    
    # Execute test
    result = await client.search_status_codes(payload)
    
    # Assertions
    assert result is not None
    assert isinstance(result, StatusCodeCollection)
    assert result.count == 1
    assert len(result.status_codes) == 1
    assert result.status_codes[0].application_status_code == 150
    
    # Verify API call was made with correct payload
    mock_session.post.assert_called_once()
    call_args = mock_session.post.call_args
    assert call_args[0][0].endswith("/status-codes")
    assert call_args[1]["json"] == payload
    mock_response.json.assert_called_once()


@pytest.mark.asyncio
async def test_search_status_codes_error_handling(client):
    """Test error handling for status codes endpoint"""
    client, mock_session = client
    
    # Create error response
    mock_response = Mock()
    mock_response.status = 404
    mock_response.json = AsyncMock(return_value={
        "code": 404,
        "error": "Not Found",
        "errorDetails": "No matching records found",
        "requestIdentifier": "test-request-id"
    })
    
    # Create async context manager mock
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = mock_response
    mock_session.get.return_value = async_cm
    
    # Test error handling
    with pytest.raises(USPTOError) as exc_info:
        await client.search_status_codes_get(q="invalid:query")
    
    # Verify error details
    assert exc_info.value.code == 404 or str(exc_info.value.code) == "404"
    assert exc_info.value.error == "Not Found"
    assert exc_info.value.error_details == "No matching records found"


@pytest.mark.asyncio
async def test_status_code_model_parsing(client):
    """Test StatusCode model parsing from API response"""
    client, mock_session = client
    
    # Create mock response with various status codes
    mock_response_data = {
        "count": 3,
        "statusCodeDataBag": [
            {
                "applicationStatusCode": 150,
                "applicationStatusDescriptionText": "Patented Case"
            },
            {
                "applicationStatusCode": 161,
                "applicationStatusDescriptionText": "Abandoned -- Failure to Respond to an Office Action"
            },
            {
                "applicationStatusCode": 19,
                "applicationStatusDescriptionText": "Application Undergoing Preexam Processing"
            }
        ],
        "requestIdentifier": "test-request-id"
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
    result = await client.search_status_codes_get()
    
    # Verify all status codes are properly parsed
    assert len(result.status_codes) == 3
    
    # Verify each status code
    status_150 = result.status_codes[0]
    assert isinstance(status_150, StatusCode)
    assert status_150.application_status_code == 150
    assert status_150.application_status_description_text == "Patented Case"
    
    status_161 = result.status_codes[1]
    assert status_161.application_status_code == 161
    assert "Abandoned" in status_161.application_status_description_text
    
    status_19 = result.status_codes[2]
    assert status_19.application_status_code == 19
    assert "Preexam" in status_19.application_status_description_text
