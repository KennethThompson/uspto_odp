"""
Unit tests for PTAB trials proceedings endpoints.
"""
import pytest
from unittest.mock import Mock, AsyncMock
import aiohttp
from uspto_odp.controller.uspto_odp_client import USPTOClient, USPTOError
from uspto_odp.models.patent_trials_proceedings import (
    TrialProceedingResponseBag,
    TrialProceedingIdentifierResponseBag,
    TrialProceeding
)


@pytest.fixture
def client():
    api_key = "test_api_key"
    mock_session = Mock(spec=aiohttp.ClientSession)
    return USPTOClient(api_key=api_key, session=mock_session), mock_session


@pytest.mark.asyncio
async def test_search_trial_proceedings_post_success(client):
    """Test search_trial_proceedings POST method with successful response"""
    client, mock_session = client
    
    mock_response_data = {
        "count": 2,
        "trialProceedingBag": [
            {
                "trialNumber": "IPR2020-00001",
                "trialType": "IPR",
                "proceedingStatus": "Instituted",
                "patentNumber": "12345678",
                "filingDate": "2020-01-15"
            },
            {
                "trialNumber": "IPR2020-00002",
                "trialType": "IPR",
                "proceedingStatus": "Terminated",
                "patentNumber": "12345679",
                "filingDate": "2020-01-20"
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
        "q": "IPR",
        "pagination": {"offset": 0, "limit": 25}
    }
    result = await client.search_trial_proceedings(payload)
    
    assert result is not None
    assert isinstance(result, TrialProceedingResponseBag)
    assert result.count == 2
    assert len(result.trial_proceeding_bag) == 2
    assert result.request_identifier == "test-request-id"
    assert result.trial_proceeding_bag[0].trial_number == "IPR2020-00001"
    
    assert mock_session.post.call_count == 1
    args, kwargs = mock_session.post.call_args_list[0]
    assert "search" in args[0] or "search" in str(args[0])
    assert kwargs["json"] == payload
    assert kwargs["headers"]["X-API-KEY"] == "test_api_key"


@pytest.mark.asyncio
async def test_search_trial_proceedings_get_success(client):
    """Test search_trial_proceedings_get GET method with successful response"""
    client, mock_session = client
    
    mock_response_data = {
        "count": 1,
        "trialProceedingBag": [
            {
                "trialNumber": "IPR2020-00001",
                "trialType": "IPR",
                "proceedingStatus": "Instituted"
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
    
    result = await client.search_trial_proceedings_get(q="IPR")
    
    assert result is not None
    assert isinstance(result, TrialProceedingResponseBag)
    assert result.count == 1
    assert len(result.trial_proceeding_bag) == 1
    
    assert mock_session.get.call_count == 1
    args, kwargs = mock_session.get.call_args_list[0]
    assert "search" in args[0] or "search" in str(args[0])
    assert kwargs["params"]["q"] == "IPR"
    assert kwargs["headers"]["X-API-KEY"] == "test_api_key"


@pytest.mark.asyncio
async def test_search_trial_proceedings_get_all_params(client):
    """Test search_trial_proceedings_get with all parameters"""
    client, mock_session = client
    
    mock_response_data = {
        "count": 5,
        "trialProceedingBag": [],
        "requestIdentifier": "test-all-params-id"
    }
    
    mock_response = Mock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value=mock_response_data)
    
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = mock_response
    mock_session.get.return_value = async_cm
    
    result = await client.search_trial_proceedings_get(
        q="IPR",
        sort="filingDate desc",
        offset=10,
        limit=50,
        facets="trialType,proceedingStatus",
        fields="trialNumber,patentNumber",
        filters="proceedingStatus Instituted",
        range_filters="filingDate 2021-01-01:2025-01-01"
    )
    
    assert result is not None
    assert result.count == 5
    
    args, kwargs = mock_session.get.call_args_list[0]
    params = kwargs["params"]
    assert params["q"] == "IPR"
    assert params["sort"] == "filingDate desc"
    assert params["offset"] == 10
    assert params["limit"] == 50
    assert params["facets"] == "trialType,proceedingStatus"
    assert params["fields"] == "trialNumber,patentNumber"
    assert params["filters"] == "proceedingStatus Instituted"
    assert params["rangeFilters"] == "filingDate 2021-01-01:2025-01-01"


@pytest.mark.asyncio
async def test_search_trial_proceedings_download_post_success(client):
    """Test search_trial_proceedings_download POST method with successful response"""
    client, mock_session = client
    
    mock_response_data = {
        "count": 10,
        "trialProceedingBag": [],
        "requestIdentifier": "test-download-post-id"
    }
    
    mock_response = Mock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value=mock_response_data)
    
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = mock_response
    mock_session.post.return_value = async_cm
    
    payload = {
        "q": "IPR",
        "pagination": {
            "offset": 0,
            "limit": 10
        }
    }
    result = await client.search_trial_proceedings_download(payload)
    
    assert result is not None
    assert isinstance(result, TrialProceedingResponseBag)
    assert result.count == 10
    
    args, kwargs = mock_session.post.call_args_list[0]
    assert "search" in args[0] or "search" in str(args[0])
    assert "download" in args[0] or "download" in str(args[0])


@pytest.mark.asyncio
async def test_search_trial_proceedings_download_get_success(client):
    """Test search_trial_proceedings_download_get GET method with successful response"""
    client, mock_session = client
    
    mock_response_data = {
        "count": 5,
        "trialProceedingBag": [],
        "requestIdentifier": "test-download-get-id"
    }
    
    mock_response = Mock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value=mock_response_data)
    
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = mock_response
    mock_session.get.return_value = async_cm
    
    result = await client.search_trial_proceedings_download_get(q="IPR", format="json")
    
    assert result is not None
    assert result.count == 5
    
    args, kwargs = mock_session.get.call_args_list[0]
    assert kwargs["params"]["format"] == "json"


@pytest.mark.asyncio
async def test_search_trial_proceedings_download_get_csv_format(client):
    """Test search_trial_proceedings_download_get with CSV format"""
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
    
    result = await client.search_trial_proceedings_download_get(q="IPR", format="csv", limit=100)
    
    assert result is not None
    assert result.count == 10
    
    args, kwargs = mock_session.get.call_args_list[0]
    assert kwargs["params"]["format"] == "csv"
    assert kwargs["params"]["limit"] == 100


@pytest.mark.asyncio
async def test_get_trial_proceeding_success(client):
    """Test get_trial_proceeding with successful response"""
    client, mock_session = client
    
    mock_response_data = {
        "count": 1,
        "trialProceedingBag": [
            {
                "trialNumber": "IPR2020-00001",
                "trialType": "IPR",
                "proceedingStatus": "Instituted",
                "patentNumber": "12345678",
                "filingDate": "2020-01-15",
                "institutionDate": "2020-06-01"
            }
        ],
        "requestIdentifier": "test-get-proceeding-id"
    }
    
    mock_response = Mock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value=mock_response_data)
    
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = mock_response
    mock_session.get.return_value = async_cm
    
    trial_number = "IPR2020-00001"
    result = await client.get_trial_proceeding(trial_number)
    
    assert result is not None
    assert isinstance(result, TrialProceedingIdentifierResponseBag)
    assert result.count == 1
    assert len(result.trial_proceeding_bag) == 1
    assert result.trial_proceeding_bag[0].trial_number == trial_number
    
    args, kwargs = mock_session.get.call_args_list[0]
    assert trial_number in args[0] or trial_number in str(args[0])


@pytest.mark.asyncio
async def test_search_trial_proceedings_error_handling(client):
    """Test search_trial_proceedings with error response"""
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
        await client.search_trial_proceedings({"invalid": "payload"})
    
    assert exc_info.value.code == 400
    assert "Bad Request" in str(exc_info.value)


@pytest.mark.asyncio
async def test_get_trial_proceeding_error_handling(client):
    """Test get_trial_proceeding with error response"""
    client, mock_session = client
    
    mock_error_data = {
        "code": 404,
        "error": "Not Found",
        "errorDetails": "Trial proceeding not found",
        "requestIdentifier": "test-error-id"
    }
    
    mock_response = Mock()
    mock_response.status = 404
    mock_response.json = AsyncMock(return_value=mock_error_data)
    
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = mock_response
    mock_session.get.return_value = async_cm
    
    with pytest.raises(USPTOError) as exc_info:
        await client.get_trial_proceeding("invalid-trial-number")
    
    assert exc_info.value.code == 404
    assert "Not Found" in str(exc_info.value)
