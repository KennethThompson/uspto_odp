"""
Unit tests for attorney endpoint.
"""
import pytest
from unittest.mock import Mock, AsyncMock
import aiohttp
from uspto_odp.controller.uspto_odp_client import USPTOClient, USPTOError
from uspto_odp.models.patent_attorney import AttorneyResponse, ApplicationAttorney, RecordAttorney


@pytest.fixture
def client():
    api_key = "test_api_key"
    mock_session = Mock(spec=aiohttp.ClientSession)
    return USPTOClient(api_key=api_key, session=mock_session), mock_session


@pytest.mark.asyncio
async def test_get_attorney_success(client):
    """Test get_attorney method with successful response"""
    client, mock_session = client
    
    # Create mock response data
    mock_response_data = {
        "count": 1,
        "patentFileWrapperDataBag": [{
            "applicationNumberText": "14412875",
            "recordAttorney": {
                "attorneyNameText": "John Doe",
                "attorneyRegistrationNumber": "12345",
                "attorneyDocketNumber": "DOCKET-001",
                "attorneyAddress": {
                    "addressLineOneText": "123 Main St",
                    "addressLineTwoText": "Suite 100",
                    "cityName": "Washington",
                    "geographicRegionCode": "DC",
                    "postalCode": "20001",
                    "countryCode": "US"
                },
                "attorneyPhoneNumber": "202-555-1234",
                "attorneyEmail": "john.doe@example.com",
                "attorneyType": "Attorney"
            }
        }],
        "requestIdentifier": "test-attorney-request-id"
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
    result = await client.get_attorney("14412875")
    
    # Assertions
    assert result is not None
    assert isinstance(result, AttorneyResponse)
    assert result.count == 1
    assert len(result.attorneys) == 1
    assert result.request_identifier == "test-attorney-request-id"
    
    attorney_data = result.attorneys[0]
    assert attorney_data.application_number == "14412875"
    assert attorney_data.record_attorney is not None
    assert attorney_data.record_attorney.attorney_name == "John Doe"
    assert attorney_data.record_attorney.registration_number == "12345"
    assert attorney_data.record_attorney.attorney_docket_number == "DOCKET-001"
    assert attorney_data.record_attorney.phone_number == "202-555-1234"
    assert attorney_data.record_attorney.email == "john.doe@example.com"
    assert attorney_data.record_attorney.attorney_type == "Attorney"
    
    # Verify address
    assert attorney_data.record_attorney.address is not None
    assert attorney_data.record_attorney.address.address_line_one == "123 Main St"
    assert attorney_data.record_attorney.address.city_name == "Washington"
    assert attorney_data.record_attorney.address.geographic_region_code == "DC"
    
    # Verify GET was called with correct URL
    assert mock_session.get.call_count == 1
    args, kwargs = mock_session.get.call_args_list[0]
    assert "14412875" in args[0] or "14412875" in str(args[0])
    assert "attorney" in args[0] or "attorney" in str(args[0])
    assert kwargs["headers"]["X-API-KEY"] == "test_api_key"


@pytest.mark.asyncio
async def test_get_attorney_empty_response(client):
    """Test get_attorney with empty response"""
    client, mock_session = client
    
    mock_response_data = {
        "count": 0,
        "patentFileWrapperDataBag": [],
        "requestIdentifier": "test-empty-request-id"
    }
    
    mock_response = Mock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value=mock_response_data)
    
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = mock_response
    mock_session.get.return_value = async_cm
    
    result = await client.get_attorney("14412875")
    
    assert result is not None
    assert result.count == 0
    assert len(result.attorneys) == 0


@pytest.mark.asyncio
async def test_get_attorney_not_found(client):
    """Test get_attorney with non-existent application number"""
    client, mock_session = client
    
    # Create mock error response
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
    
    # Execute test and expect USPTOError
    with pytest.raises(USPTOError) as exc_info:
        await client.get_attorney("99999999")
    
    assert exc_info.value.code == 404
    assert "Not Found" in str(exc_info.value)


@pytest.mark.asyncio
async def test_get_attorney_bad_request(client):
    """Test get_attorney with bad request"""
    client, mock_session = client
    
    mock_error_data = {
        "code": 400,
        "error": "Bad Request",
        "errorDetails": "Invalid application number format",
        "requestIdentifier": "test-bad-request-id"
    }
    
    mock_response = Mock()
    mock_response.status = 400
    mock_response.json = AsyncMock(return_value=mock_error_data)
    
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = mock_response
    mock_session.get.return_value = async_cm
    
    with pytest.raises(USPTOError) as exc_info:
        await client.get_attorney("invalid")
    
    assert exc_info.value.code == 400
    assert "Bad Request" in str(exc_info.value)
