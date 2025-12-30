"""
Unit tests for petition decision endpoints.
"""
import pytest
from unittest.mock import Mock, AsyncMock
import aiohttp
from uspto_odp.controller.uspto_odp_client import USPTOClient, USPTOError
from uspto_odp.models.patent_petition_decision import (
    PetitionDecisionResponseBag,
    PetitionDecisionIdentifierResponseBag,
    PetitionDecision
)


@pytest.fixture
def client():
    api_key = "test_api_key"
    mock_session = Mock(spec=aiohttp.ClientSession)
    return USPTOClient(api_key=api_key, session=mock_session), mock_session


@pytest.mark.asyncio
async def test_search_petition_decisions_post_success(client):
    """Test search_petition_decisions POST method with successful response"""
    client, mock_session = client
    
    mock_response_data = {
        "count": 2,
        "petitionDecisionBag": [
            {
                "petitionDecisionRecordIdentifier": "6779f1be-0f3b-5775-b9d3-dcfdb83171c3",
                "patentNumber": "12345678",
                "applicationNumberText": "11512156",
                "firstApplicantName": "Test Applicant",
                "decisionTypeCodeDescriptionText": "Denied"
            },
            {
                "petitionDecisionRecordIdentifier": "6779f1be-0f3b-5775-b9d3-dcfdb83171c4",
                "patentNumber": "12345679",
                "applicationNumberText": "11512157",
                "firstApplicantName": "Another Applicant",
                "decisionTypeCodeDescriptionText": "Granted"
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
        "q": "Denied",
        "pagination": {"offset": 0, "limit": 25}
    }
    result = await client.search_petition_decisions(payload)
    
    assert result is not None
    assert isinstance(result, PetitionDecisionResponseBag)
    assert result.count == 2
    assert len(result.petition_decision_bag) == 2
    assert result.request_identifier == "test-request-id"
    assert result.petition_decision_bag[0].petition_decision_record_identifier == "6779f1be-0f3b-5775-b9d3-dcfdb83171c3"
    
    assert mock_session.post.call_count == 1
    args, kwargs = mock_session.post.call_args_list[0]
    assert "search" in args[0] or "search" in str(args[0])
    assert kwargs["json"] == payload
    assert kwargs["headers"]["X-API-KEY"] == "test_api_key"


@pytest.mark.asyncio
async def test_search_petition_decisions_get_success(client):
    """Test search_petition_decisions_get GET method with successful response"""
    client, mock_session = client
    
    mock_response_data = {
        "count": 1,
        "petitionDecisionBag": [
            {
                "petitionDecisionRecordIdentifier": "6779f1be-0f3b-5775-b9d3-dcfdb83171c3",
                "patentNumber": "12345678",
                "decisionTypeCodeDescriptionText": "Denied"
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
    
    result = await client.search_petition_decisions_get(q="decisionTypeCodeDescriptionText:Denied")
    
    assert result is not None
    assert isinstance(result, PetitionDecisionResponseBag)
    assert result.count == 1
    assert len(result.petition_decision_bag) == 1
    
    assert mock_session.get.call_count == 1
    args, kwargs = mock_session.get.call_args_list[0]
    assert "search" in args[0] or "search" in str(args[0])
    assert kwargs["params"]["q"] == "decisionTypeCodeDescriptionText:Denied"
    assert kwargs["headers"]["X-API-KEY"] == "test_api_key"


@pytest.mark.asyncio
async def test_search_petition_decisions_get_all_params(client):
    """Test search_petition_decisions_get with all parameters"""
    client, mock_session = client
    
    mock_response_data = {
        "count": 5,
        "petitionDecisionBag": [],
        "requestIdentifier": "test-all-params-id"
    }
    
    mock_response = Mock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value=mock_response_data)
    
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = mock_response
    mock_session.get.return_value = async_cm
    
    result = await client.search_petition_decisions_get(
        q="Denied",
        sort="petitionMailDate desc",
        offset=10,
        limit=50,
        facets="decisionTypeCode,businessEntityStatusCategory",
        fields="petitionDecisionRecordIdentifier,patentNumber",
        filters="businessEntityStatusCategory Small",
        range_filters="petitionMailDate 2021-01-01:2025-01-01"
    )
    
    assert result is not None
    assert result.count == 5
    
    args, kwargs = mock_session.get.call_args_list[0]
    params = kwargs["params"]
    assert params["q"] == "Denied"
    assert params["sort"] == "petitionMailDate desc"
    assert params["offset"] == 10
    assert params["limit"] == 50
    assert params["facets"] == "decisionTypeCode,businessEntityStatusCategory"
    assert params["fields"] == "petitionDecisionRecordIdentifier,patentNumber"
    assert params["filters"] == "businessEntityStatusCategory Small"
    assert params["rangeFilters"] == "petitionMailDate 2021-01-01:2025-01-01"


@pytest.mark.asyncio
async def test_search_petition_decisions_download_post_success(client):
    """Test search_petition_decisions_download POST method with successful response"""
    client, mock_session = client
    
    mock_response_data = {
        "count": 10,
        "petitionDecisionBag": [],
        "requestIdentifier": "test-download-post-id"
    }
    
    mock_response = Mock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value=mock_response_data)
    
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = mock_response
    mock_session.post.return_value = async_cm
    
    payload = {
        "q": "Denied",
        "pagination": {
            "offset": 0,
            "limit": 10
        }
    }
    result = await client.search_petition_decisions_download(payload)
    
    assert result is not None
    assert isinstance(result, PetitionDecisionResponseBag)
    assert result.count == 10
    
    args, kwargs = mock_session.post.call_args_list[0]
    assert "search" in args[0] or "search" in str(args[0])
    assert "download" in args[0] or "download" in str(args[0])


@pytest.mark.asyncio
async def test_search_petition_decisions_download_get_success(client):
    """Test search_petition_decisions_download_get GET method with successful response"""
    client, mock_session = client
    
    mock_response_data = {
        "count": 5,
        "petitionDecisionBag": [],
        "requestIdentifier": "test-download-get-id"
    }
    
    mock_response = Mock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value=mock_response_data)
    
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = mock_response
    mock_session.get.return_value = async_cm
    
    result = await client.search_petition_decisions_download_get(q="Denied", format="json")
    
    assert result is not None
    assert result.count == 5
    
    args, kwargs = mock_session.get.call_args_list[0]
    assert kwargs["params"]["format"] == "json"


@pytest.mark.asyncio
async def test_search_petition_decisions_download_get_csv_format(client):
    """Test search_petition_decisions_download_get with CSV format"""
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
    
    result = await client.search_petition_decisions_download_get(q="Denied", format="csv", limit=100)
    
    assert result is not None
    assert result.count == 10
    
    args, kwargs = mock_session.get.call_args_list[0]
    assert kwargs["params"]["format"] == "csv"
    assert kwargs["params"]["limit"] == 100


@pytest.mark.asyncio
async def test_get_petition_decision_success(client):
    """Test get_petition_decision with successful response"""
    client, mock_session = client
    
    mock_response_data = {
        "count": 1,
        "petitionDecisionBag": [
            {
                "petitionDecisionRecordIdentifier": "6779f1be-0f3b-5775-b9d3-dcfdb83171c3",
                "patentNumber": "12345678",
                "applicationNumberText": "11512156",
                "firstApplicantName": "Test Applicant",
                "decisionTypeCodeDescriptionText": "Denied",
                "petitionMailDate": "2023-01-01"
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
    
    identifier = "6779f1be-0f3b-5775-b9d3-dcfdb83171c3"
    result = await client.get_petition_decision(identifier)
    
    assert result is not None
    assert isinstance(result, PetitionDecisionIdentifierResponseBag)
    assert result.count == 1
    assert len(result.petition_decision_bag) == 1
    assert result.petition_decision_bag[0].petition_decision_record_identifier == identifier
    
    args, kwargs = mock_session.get.call_args_list[0]
    assert identifier in args[0] or identifier in str(args[0])
    assert kwargs["params"]["includeDocuments"] == "false"


@pytest.mark.asyncio
async def test_get_petition_decision_with_documents(client):
    """Test get_petition_decision with includeDocuments=true"""
    client, mock_session = client
    
    mock_response_data = {
        "count": 1,
        "petitionDecisionBag": [
            {
                "petitionDecisionRecordIdentifier": "6779f1be-0f3b-5775-b9d3-dcfdb83171c3",
                "documents": [{"documentId": "doc1", "documentType": "Decision"}]
            }
        ]
    }
    
    mock_response = Mock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value=mock_response_data)
    
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = mock_response
    mock_session.get.return_value = async_cm
    
    identifier = "6779f1be-0f3b-5775-b9d3-dcfdb83171c3"
    result = await client.get_petition_decision(identifier, include_documents=True)
    
    assert result is not None
    assert result.petition_decision_bag[0].documents is not None
    
    args, kwargs = mock_session.get.call_args_list[0]
    assert kwargs["params"]["includeDocuments"] == "true"


@pytest.mark.asyncio
async def test_search_petition_decisions_error_handling(client):
    """Test search_petition_decisions with error response"""
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
        await client.search_petition_decisions({"invalid": "payload"})
    
    assert exc_info.value.code == 400
    assert "Bad Request" in str(exc_info.value)


@pytest.mark.asyncio
async def test_get_petition_decision_error_handling(client):
    """Test get_petition_decision with error response"""
    client, mock_session = client
    
    mock_error_data = {
        "code": 404,
        "error": "Not Found",
        "errorDetails": "Petition decision not found",
        "requestIdentifier": "test-error-id"
    }
    
    mock_response = Mock()
    mock_response.status = 404
    mock_response.json = AsyncMock(return_value=mock_error_data)
    
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = mock_response
    mock_session.get.return_value = async_cm
    
    with pytest.raises(USPTOError) as exc_info:
        await client.get_petition_decision("invalid-identifier")
    
    assert exc_info.value.code == 404
    assert "Not Found" in str(exc_info.value)
