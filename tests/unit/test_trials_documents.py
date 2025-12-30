"""
Unit tests for PTAB trials documents endpoints.
"""
import pytest
from unittest.mock import Mock, AsyncMock
import aiohttp
from uspto_odp.controller.uspto_odp_client import USPTOClient, USPTOError
from uspto_odp.models.patent_trials_documents import (
    TrialDocumentResponseBag,
    TrialDocumentIdentifierResponseBag,
    TrialDocumentByTrialResponseBag,
    TrialDocument
)


@pytest.fixture
def client():
    api_key = "test_api_key"
    mock_session = Mock(spec=aiohttp.ClientSession)
    return USPTOClient(api_key=api_key, session=mock_session), mock_session


@pytest.mark.asyncio
async def test_search_trial_documents_post_success(client):
    """Test search_trial_documents POST method with successful response"""
    client, mock_session = client
    
    mock_response_data = {
        "count": 2,
        "trialDocumentBag": [
            {
                "documentIdentifier": "DOC-001",
                "trialNumber": "IPR2020-00001",
                "trialType": "IPR",
                "documentType": "Petition",
                "documentTitle": "Petition for Inter Partes Review",
                "filingDate": "2020-01-15",
                "documentDate": "2020-01-15"
            },
            {
                "documentIdentifier": "DOC-002",
                "trialNumber": "IPR2020-00002",
                "trialType": "IPR",
                "documentType": "Decision",
                "documentTitle": "Decision on Institution",
                "filingDate": "2020-02-20",
                "documentDate": "2020-02-20"
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
    result = await client.search_trial_documents(payload)
    
    assert result is not None
    assert isinstance(result, TrialDocumentResponseBag)
    assert result.count == 2
    assert len(result.trial_document_bag) == 2
    assert result.request_identifier == "test-request-id"
    assert result.trial_document_bag[0].document_identifier == "DOC-001"
    
    assert mock_session.post.call_count == 1
    args, kwargs = mock_session.post.call_args_list[0]
    assert "search" in args[0] or "search" in str(args[0])
    assert kwargs["json"] == payload
    assert kwargs["headers"]["X-API-KEY"] == "test_api_key"


@pytest.mark.asyncio
async def test_search_trial_documents_get_success(client):
    """Test search_trial_documents_get GET method with successful response"""
    client, mock_session = client
    
    mock_response_data = {
        "count": 1,
        "trialDocumentBag": [
            {
                "documentIdentifier": "DOC-001",
                "trialNumber": "IPR2020-00001",
                "trialType": "IPR",
                "documentType": "Petition"
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
    
    result = await client.search_trial_documents_get(q="IPR")
    
    assert result is not None
    assert isinstance(result, TrialDocumentResponseBag)
    assert result.count == 1
    assert len(result.trial_document_bag) == 1
    
    assert mock_session.get.call_count == 1
    args, kwargs = mock_session.get.call_args_list[0]
    assert "search" in args[0] or "search" in str(args[0])
    assert kwargs["params"]["q"] == "IPR"
    assert kwargs["headers"]["X-API-KEY"] == "test_api_key"


@pytest.mark.asyncio
async def test_search_trial_documents_get_all_params(client):
    """Test search_trial_documents_get with all parameters"""
    client, mock_session = client
    
    mock_response_data = {
        "count": 5,
        "trialDocumentBag": [],
        "requestIdentifier": "test-all-params-id"
    }
    
    mock_response = Mock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value=mock_response_data)
    
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = mock_response
    mock_session.get.return_value = async_cm
    
    result = await client.search_trial_documents_get(
        q="IPR",
        sort="documentDate desc",
        offset=10,
        limit=50,
        facets="trialType,documentType",
        fields="documentIdentifier,patentNumber",
        filters="documentType Petition",
        range_filters="documentDate 2021-01-01:2025-01-01"
    )
    
    assert result is not None
    assert result.count == 5
    
    args, kwargs = mock_session.get.call_args_list[0]
    params = kwargs["params"]
    assert params["q"] == "IPR"
    assert params["sort"] == "documentDate desc"
    assert params["offset"] == 10
    assert params["limit"] == 50
    assert params["facets"] == "trialType,documentType"
    assert params["fields"] == "documentIdentifier,patentNumber"
    assert params["filters"] == "documentType Petition"
    assert params["rangeFilters"] == "documentDate 2021-01-01:2025-01-01"


@pytest.mark.asyncio
async def test_search_trial_documents_download_post_success(client):
    """Test search_trial_documents_download POST method with successful response"""
    client, mock_session = client
    
    mock_response_data = {
        "count": 10,
        "trialDocumentBag": [],
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
    result = await client.search_trial_documents_download(payload)
    
    assert result is not None
    assert isinstance(result, TrialDocumentResponseBag)
    assert result.count == 10
    
    args, kwargs = mock_session.post.call_args_list[0]
    assert "search" in args[0] or "search" in str(args[0])
    assert "download" in args[0] or "download" in str(args[0])


@pytest.mark.asyncio
async def test_search_trial_documents_download_get_success(client):
    """Test search_trial_documents_download_get GET method with successful response"""
    client, mock_session = client
    
    mock_response_data = {
        "count": 5,
        "trialDocumentBag": [],
        "requestIdentifier": "test-download-get-id"
    }
    
    mock_response = Mock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value=mock_response_data)
    
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = mock_response
    mock_session.get.return_value = async_cm
    
    result = await client.search_trial_documents_download_get(q="IPR", format="json")
    
    assert result is not None
    assert result.count == 5
    
    args, kwargs = mock_session.get.call_args_list[0]
    assert kwargs["params"]["format"] == "json"


@pytest.mark.asyncio
async def test_search_trial_documents_download_get_csv_format(client):
    """Test search_trial_documents_download_get with CSV format"""
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
    
    result = await client.search_trial_documents_download_get(q="IPR", format="csv", limit=100)
    
    assert result is not None
    assert result.count == 10
    
    args, kwargs = mock_session.get.call_args_list[0]
    assert kwargs["params"]["format"] == "csv"
    assert kwargs["params"]["limit"] == 100


@pytest.mark.asyncio
async def test_get_trial_document_success(client):
    """Test get_trial_document with successful response"""
    client, mock_session = client
    
    mock_response_data = {
        "count": 1,
        "trialDocumentBag": [
            {
                "documentIdentifier": "DOC-001",
                "trialNumber": "IPR2020-00001",
                "trialType": "IPR",
                "documentType": "Petition",
                "documentTitle": "Petition for Inter Partes Review",
                "filingDate": "2020-01-15",
                "documentDate": "2020-01-15"
            }
        ],
        "requestIdentifier": "test-get-document-id"
    }
    
    mock_response = Mock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value=mock_response_data)
    
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = mock_response
    mock_session.get.return_value = async_cm
    
    document_identifier = "DOC-001"
    result = await client.get_trial_document(document_identifier)
    
    assert result is not None
    assert isinstance(result, TrialDocumentIdentifierResponseBag)
    assert result.count == 1
    assert len(result.trial_document_bag) == 1
    assert result.trial_document_bag[0].document_identifier == document_identifier
    
    args, kwargs = mock_session.get.call_args_list[0]
    assert document_identifier in args[0] or document_identifier in str(args[0])


@pytest.mark.asyncio
async def test_get_trial_documents_by_trial_success(client):
    """Test get_trial_documents_by_trial with successful response"""
    client, mock_session = client
    
    mock_response_data = {
        "count": 2,
        "trialDocumentBag": [
            {
                "documentIdentifier": "DOC-001",
                "trialNumber": "IPR2020-00001",
                "documentType": "Petition"
            },
            {
                "documentIdentifier": "DOC-002",
                "trialNumber": "IPR2020-00001",
                "documentType": "Decision"
            }
        ],
        "requestIdentifier": "test-get-by-trial-id"
    }
    
    mock_response = Mock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value=mock_response_data)
    
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = mock_response
    mock_session.get.return_value = async_cm
    
    trial_number = "IPR2020-00001"
    result = await client.get_trial_documents_by_trial(trial_number)
    
    assert result is not None
    assert isinstance(result, TrialDocumentByTrialResponseBag)
    assert result.count == 2
    assert len(result.trial_document_bag) == 2
    assert result.trial_document_bag[0].trial_number == trial_number
    
    args, kwargs = mock_session.get.call_args_list[0]
    assert trial_number in args[0] or trial_number in str(args[0])
    assert "documents" in args[0] or "documents" in str(args[0])


@pytest.mark.asyncio
async def test_search_trial_documents_error_handling(client):
    """Test search_trial_documents with error response"""
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
        await client.search_trial_documents({"invalid": "payload"})
    
    assert exc_info.value.code == 400
    assert "Bad Request" in str(exc_info.value)


@pytest.mark.asyncio
async def test_get_trial_document_error_handling(client):
    """Test get_trial_document with error response"""
    client, mock_session = client
    
    mock_error_data = {
        "code": 404,
        "error": "Not Found",
        "errorDetails": "Trial document not found",
        "requestIdentifier": "test-error-id"
    }
    
    mock_response = Mock()
    mock_response.status = 404
    mock_response.json = AsyncMock(return_value=mock_error_data)
    
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = mock_response
    mock_session.get.return_value = async_cm
    
    with pytest.raises(USPTOError) as exc_info:
        await client.get_trial_document("invalid-document-id")
    
    assert exc_info.value.code == 404
    assert "Not Found" in str(exc_info.value)
