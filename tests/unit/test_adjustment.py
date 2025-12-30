"""
Unit tests for adjustment endpoint.
"""
import pytest
from unittest.mock import Mock, AsyncMock
import aiohttp
from uspto_odp.controller.uspto_odp_client import USPTOClient, USPTOError
from uspto_odp.models.patent_adjustment import AdjustmentResponse, ApplicationAdjustment, PatentTermAdjustment


@pytest.fixture
def client():
    api_key = "test_api_key"
    mock_session = Mock(spec=aiohttp.ClientSession)
    return USPTOClient(api_key=api_key, session=mock_session), mock_session


@pytest.mark.asyncio
async def test_get_adjustment_success(client):
    """Test get_adjustment method with successful response"""
    client, mock_session = client
    
    # Create mock response data
    mock_response_data = {
        "count": 1,
        "patentFileWrapperDataBag": [{
            "applicationNumberText": "14412875",
            "patentTermAdjustmentData": {
                "ptaDays": 100,
                "ptaTypeADays": 50,
                "ptaTypeBDays": 30,
                "ptaTypeCDays": 20,
                "pteDays": 0,
                "pteType": None,
                "grantDate": "2023-01-15",
                "issueDate": "2023-01-15",
                "adjustmentDate": "2023-01-20",
                "adjustmentReasonCodes": ["A", "B"],
                "adjustmentReasonDescriptions": ["USPTO delay", "Applicant delay"],
                "totalAdjustmentDays": 100,
                "patentNumber": "12345678"
            }
        }],
        "requestIdentifier": "test-adjustment-request-id"
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
    result = await client.get_adjustment("14412875")
    
    # Assertions
    assert result is not None
    assert isinstance(result, AdjustmentResponse)
    assert result.count == 1
    assert len(result.adjustments) == 1
    assert result.request_identifier == "test-adjustment-request-id"
    
    adjustment_data = result.adjustments[0]
    assert adjustment_data.application_number == "14412875"
    assert adjustment_data.patent_term_adjustment is not None
    
    pta = adjustment_data.patent_term_adjustment
    assert pta.pta_days == 100
    assert pta.pta_type_a_days == 50
    assert pta.pta_type_b_days == 30
    assert pta.pta_type_c_days == 20
    assert pta.total_adjustment_days == 100
    assert pta.patent_number == "12345678"
    assert len(pta.adjustment_reason_codes) == 2
    assert "A" in pta.adjustment_reason_codes
    
    # Verify GET was called with correct URL
    assert mock_session.get.call_count == 1
    args, kwargs = mock_session.get.call_args_list[0]
    assert "14412875" in args[0] or "14412875" in str(args[0])
    assert "adjustment" in args[0] or "adjustment" in str(args[0])
    assert kwargs["headers"]["X-API-KEY"] == "test_api_key"


@pytest.mark.asyncio
async def test_get_adjustment_empty_response(client):
    """Test get_adjustment with empty response"""
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
    
    result = await client.get_adjustment("14412875")
    
    assert result is not None
    assert result.count == 0
    assert len(result.adjustments) == 0


@pytest.mark.asyncio
async def test_get_adjustment_no_adjustment_data(client):
    """Test get_adjustment when patentTermAdjustmentData is None or missing"""
    client, mock_session = client
    
    mock_response_data = {
        "count": 1,
        "patentFileWrapperDataBag": [{
            "applicationNumberText": "14412875",
            "patentTermAdjustmentData": None
        }],
        "requestIdentifier": "test-no-data-request-id"
    }
    
    mock_response = Mock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value=mock_response_data)
    
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = mock_response
    mock_session.get.return_value = async_cm
    
    result = await client.get_adjustment("14412875")
    
    assert result is not None
    assert len(result.adjustments) == 1
    assert result.adjustments[0].patent_term_adjustment is None


@pytest.mark.asyncio
async def test_get_adjustment_not_found(client):
    """Test get_adjustment with non-existent application number"""
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
        await client.get_adjustment("99999999")
    
    assert exc_info.value.code == 404
    assert "Not Found" in str(exc_info.value)


@pytest.mark.asyncio
async def test_get_adjustment_bad_request(client):
    """Test get_adjustment with bad request"""
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
        await client.get_adjustment("invalid")
    
    assert exc_info.value.code == 400
    assert "Bad Request" in str(exc_info.value)
