"""
Unit tests for PTAB interferences decisions endpoints.
"""
import pytest
from unittest.mock import Mock, AsyncMock
import aiohttp
from uspto_odp.controller.uspto_odp_client import USPTOClient, USPTOError
from uspto_odp.models.patent_interferences_decisions import (
    InterferenceDecisionResponseBag,
    InterferenceDecisionIdentifierResponseBag,
    InterferenceDecisionByInterferenceResponseBag,
    InterferenceDecision
)


@pytest.fixture
def client():
    api_key = "test_api_key"
    mock_session = Mock(spec=aiohttp.ClientSession)
    return USPTOClient(api_key=api_key, session=mock_session), mock_session


@pytest.mark.asyncio
async def test_search_interference_decisions_post_success(client):
    """Test search_interference_decisions POST method with successful response"""
    client, mock_session = client
    
    mock_response_data = {
        "count": 2,
        "interferenceDecisionBag": [
            {
                "documentIdentifier": "DOC-001",
                "interferenceNumber": "106,001",
                "decisionType": "Final",
                "decisionDate": "2020-06-15",
                "patentNumber": "12345678"
            },
            {
                "documentIdentifier": "DOC-002",
                "interferenceNumber": "106,002",
                "decisionType": "Non-Final",
                "decisionDate": "2020-07-20",
                "patentNumber": "12345679"
            }
        ],
        "requestIdentifier": "test-request-id"
    }
    
    mock_response = Mock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value=mock_response_data)
    
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = mock_response
    mock_session.post.return_value = async_cm
    
    payload = {
        "q": "Final",
        "pagination": {"offset": 0, "limit": 25}
    }
    result = await client.search_interference_decisions(payload)
    
    assert result is not None
    assert isinstance(result, InterferenceDecisionResponseBag)
    assert result.count == 2
    assert len(result.interference_decision_bag) == 2
    assert result.request_identifier == "test-request-id"
    assert result.interference_decision_bag[0].document_identifier == "DOC-001"
    
    assert mock_session.post.call_count == 1
    args, kwargs = mock_session.post.call_args_list[0]
    assert "search" in args[0] or "search" in str(args[0])
    assert kwargs["json"] == payload
    assert kwargs["headers"]["X-API-KEY"] == "test_api_key"


@pytest.mark.asyncio
async def test_search_interference_decisions_get_success(client):
    """Test search_interference_decisions_get GET method with successful response"""
    client, mock_session = client
    
    mock_response_data = {
        "count": 1,
        "interferenceDecisionBag": [
            {
                "documentIdentifier": "DOC-001",
                "interferenceNumber": "106,001",
                "decisionType": "Final"
            }
        ],
        "requestIdentifier": "test-get-request-id"
    }
    
    mock_response = Mock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value=mock_response_data)
    
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = mock_response
    mock_session.get.return_value = async_cm
    
    result = await client.search_interference_decisions_get(q="Final")
    
    assert result is not None
    assert isinstance(result, InterferenceDecisionResponseBag)
    assert result.count == 1
    assert len(result.interference_decision_bag) == 1
    
    assert mock_session.get.call_count == 1
    args, kwargs = mock_session.get.call_args_list[0]
    assert "search" in args[0] or "search" in str(args[0])
    assert kwargs["params"]["q"] == "Final"
    assert kwargs["headers"]["X-API-KEY"] == "test_api_key"


@pytest.mark.asyncio
async def test_search_interference_decisions_get_all_params(client):
    """Test search_interference_decisions_get with all parameters"""
    client, mock_session = client
    
    mock_response_data = {
        "count": 5,
        "interferenceDecisionBag": [],
        "requestIdentifier": "test-all-params-id"
    }
    
    mock_response = Mock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value=mock_response_data)
    
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = mock_response
    mock_session.get.return_value = async_cm
    
    result = await client.search_interference_decisions_get(
        q="Final",
        sort="decisionDate desc",
        offset=10,
        limit=50,
        facets="decisionType",
        fields="documentIdentifier,patentNumber",
        filters="decisionType Final",
        range_filters="decisionDate 2021-01-01:2025-01-01"
    )
    
    assert result is not None
    assert result.count == 5
    
    args, kwargs = mock_session.get.call_args_list[0]
    params = kwargs["params"]
    assert params["q"] == "Final"
    assert params["sort"] == "decisionDate desc"
    assert params["offset"] == 10
    assert params["limit"] == 50
    assert params["facets"] == "decisionType"
    assert params["fields"] == "documentIdentifier,patentNumber"
    assert params["filters"] == "decisionType Final"
    assert params["rangeFilters"] == "decisionDate 2021-01-01:2025-01-01"


@pytest.mark.asyncio
async def test_search_interference_decisions_download_post_success(client):
    """Test search_interference_decisions_download POST method with successful response"""
    client, mock_session = client
    
    mock_response_data = {
        "count": 10,
        "interferenceDecisionBag": [],
        "requestIdentifier": "test-download-post-id"
    }
    
    mock_response = Mock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value=mock_response_data)
    
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = mock_response
    mock_session.post.return_value = async_cm
    
    payload = {
        "q": "Final",
        "pagination": {
            "offset": 0,
            "limit": 10
        }
    }
    result = await client.search_interference_decisions_download(payload)
    
    assert result is not None
    assert isinstance(result, InterferenceDecisionResponseBag)
    assert result.count == 10
    
    args, kwargs = mock_session.post.call_args_list[0]
    assert "search" in args[0] or "search" in str(args[0])
    assert "download" in args[0] or "download" in str(args[0])


@pytest.mark.asyncio
async def test_search_interference_decisions_download_get_success(client):
    """Test search_interference_decisions_download_get GET method with successful response"""
    client, mock_session = client
    
    mock_response_data = {
        "count": 5,
        "interferenceDecisionBag": [],
        "requestIdentifier": "test-download-get-id"
    }
    
    mock_response = Mock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value=mock_response_data)
    
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = mock_response
    mock_session.get.return_value = async_cm
    
    result = await client.search_interference_decisions_download_get(q="Final", format="json")
    
    assert result is not None
    assert result.count == 5
    
    args, kwargs = mock_session.get.call_args_list[0]
    assert kwargs["params"]["format"] == "json"


@pytest.mark.asyncio
async def test_search_interference_decisions_download_get_csv_format(client):
    """Test search_interference_decisions_download_get with CSV format"""
    client, mock_session = client
    
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
    
    result = await client.search_interference_decisions_download_get(q="Final", format="csv", limit=100)
    
    assert result is not None
    assert result.count == 10
    
    args, kwargs = mock_session.get.call_args_list[0]
    assert kwargs["params"]["format"] == "csv"
    assert kwargs["params"]["limit"] == 100


@pytest.mark.asyncio
async def test_get_interference_decision_success(client):
    """Test get_interference_decision with successful response"""
    client, mock_session = client
    
    mock_response_data = {
        "count": 1,
        "interferenceDecisionBag": [
            {
                "documentIdentifier": "DOC-001",
                "interferenceNumber": "106,001",
                "decisionType": "Final",
                "decisionDate": "2020-06-15",
                "patentNumber": "12345678"
            }
        ],
        "requestIdentifier": "test-get-decision-id"
    }
    
    mock_response = Mock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value=mock_response_data)
    
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = mock_response
    mock_session.get.return_value = async_cm
    
    document_identifier = "DOC-001"
    result = await client.get_interference_decision(document_identifier)
    
    assert result is not None
    assert isinstance(result, InterferenceDecisionIdentifierResponseBag)
    assert result.count == 1
    assert len(result.interference_decision_bag) == 1
    assert result.interference_decision_bag[0].document_identifier == document_identifier
    
    args, kwargs = mock_session.get.call_args_list[0]
    assert document_identifier in args[0] or document_identifier in str(args[0])


@pytest.mark.asyncio
async def test_get_interference_decisions_by_interference_success(client):
    """Test get_interference_decisions_by_interference with successful response"""
    client, mock_session = client
    
    mock_response_data = {
        "count": 2,
        "interferenceDecisionBag": [
            {
                "documentIdentifier": "DOC-001",
                "interferenceNumber": "106,001",
                "decisionType": "Non-Final"
            },
            {
                "documentIdentifier": "DOC-002",
                "interferenceNumber": "106,001",
                "decisionType": "Final"
            }
        ],
        "requestIdentifier": "test-get-by-interference-id"
    }
    
    mock_response = Mock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value=mock_response_data)
    
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = mock_response
    mock_session.get.return_value = async_cm
    
    interference_number = "106,001"
    result = await client.get_interference_decisions_by_interference(interference_number)
    
    assert result is not None
    assert isinstance(result, InterferenceDecisionByInterferenceResponseBag)
    assert result.count == 2
    assert len(result.interference_decision_bag) == 2
    assert result.interference_decision_bag[0].interference_number == interference_number
    
    args, kwargs = mock_session.get.call_args_list[0]
    assert interference_number in args[0] or interference_number in str(args[0])
    assert "decisions" in args[0] or "decisions" in str(args[0])


@pytest.mark.asyncio
async def test_search_interference_decisions_error_handling(client):
    """Test search_interference_decisions with error response"""
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
        await client.search_interference_decisions({"invalid": "payload"})
    
    assert exc_info.value.code == 400
    assert "Bad Request" in str(exc_info.value)


@pytest.mark.asyncio
async def test_get_interference_decision_error_handling(client):
    """Test get_interference_decision with error response"""
    client, mock_session = client
    
    mock_error_data = {
        "code": 404,
        "error": "Not Found",
        "errorDetails": "Interference decision not found",
        "requestIdentifier": "test-error-id"
    }
    
    mock_response = Mock()
    mock_response.status = 404
    mock_response.json = AsyncMock(return_value=mock_error_data)
    
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = mock_response
    mock_session.get.return_value = async_cm
    
    with pytest.raises(USPTOError) as exc_info:
        await client.get_interference_decision("invalid-document-id")
    
    assert exc_info.value.code == 404
    assert "Not Found" in str(exc_info.value)
