"""
Unit tests for associated-documents endpoint.
"""
import pytest
from unittest.mock import Mock, AsyncMock
import aiohttp
from uspto_odp.controller.uspto_odp_client import USPTOClient, USPTOError
from uspto_odp.models.patent_associated_documents import (
    AssociatedDocumentsResponse, ApplicationAssociatedDocuments,
    PGPubFileMetaData, GrantFileMetaData
)


@pytest.fixture
def client():
    api_key = "test_api_key"
    mock_session = Mock(spec=aiohttp.ClientSession)
    return USPTOClient(api_key=api_key, session=mock_session), mock_session


@pytest.mark.asyncio
async def test_get_associated_documents_success_both(client):
    """Test get_associated_documents method with both PGPub and Grant metadata"""
    client, mock_session = client
    
    # Create mock response data
    mock_response_data = {
        "count": 1,
        "patentFileWrapperDataBag": [{
            "applicationNumberText": "14412875",
            "pgpubDocumentMetaData": {
                "productIdentifier": "PGPUB-001",
                "zipFileName": "pgpub_14412875.zip",
                "fileCreateDateTime": "2023-01-15T10:30:00Z",
                "xmlFileName": "pgpub_14412875.xml",
                "fileLocationURI": "https://example.com/pgpub/14412875"
            },
            "grantDocumentMetaData": {
                "productIdentifier": "GRANT-001",
                "zipFileName": "grant_14412875.zip",
                "fileCreateDateTime": "2023-06-15T10:30:00Z",
                "xmlFileName": "grant_14412875.xml",
                "fileLocationURI": "https://example.com/grant/14412875"
            },
            "requestIdentifier": "test-request-id-123"
        }],
        "requestIdentifier": "test-top-level-request-id"
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
    result = await client.get_associated_documents("14412875")
    
    # Assertions
    assert result is not None
    assert isinstance(result, AssociatedDocumentsResponse)
    assert result.count == 1
    assert len(result.associated_documents) == 1
    
    doc_data = result.associated_documents[0]
    assert doc_data.application_number == "14412875"
    assert doc_data.pgpub_document_meta_data is not None
    assert doc_data.grant_document_meta_data is not None
    assert doc_data.request_identifier == "test-request-id-123"
    
    pgpub = doc_data.pgpub_document_meta_data
    assert pgpub.product_identifier == "PGPUB-001"
    assert pgpub.zip_file_name == "pgpub_14412875.zip"
    assert pgpub.xml_file_name == "pgpub_14412875.xml"
    assert pgpub.file_location_uri == "https://example.com/pgpub/14412875"
    
    grant = doc_data.grant_document_meta_data
    assert grant.product_identifier == "GRANT-001"
    assert grant.zip_file_name == "grant_14412875.zip"
    assert grant.xml_file_name == "grant_14412875.xml"
    assert grant.file_location_uri == "https://example.com/grant/14412875"
    
    # Verify GET was called with correct URL
    assert mock_session.get.call_count == 1
    args, kwargs = mock_session.get.call_args_list[0]
    assert "14412875" in args[0] or "14412875" in str(args[0])
    assert "associated-documents" in args[0] or "associated-documents" in str(args[0])
    assert kwargs["headers"]["X-API-KEY"] == "test_api_key"


@pytest.mark.asyncio
async def test_get_associated_documents_only_pgpub(client):
    """Test get_associated_documents with only PGPub metadata"""
    client, mock_session = client
    
    mock_response_data = {
        "count": 1,
        "patentFileWrapperDataBag": [{
            "applicationNumberText": "14412875",
            "pgpubDocumentMetaData": {
                "productIdentifier": "PGPUB-001",
                "zipFileName": "pgpub_14412875.zip",
                "fileCreateDateTime": "2023-01-15T10:30:00Z",
                "xmlFileName": "pgpub_14412875.xml",
                "fileLocationURI": "https://example.com/pgpub/14412875"
            },
            "grantDocumentMetaData": None
        }]
    }
    
    mock_response = Mock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value=mock_response_data)
    
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = mock_response
    mock_session.get.return_value = async_cm
    
    result = await client.get_associated_documents("14412875")
    
    assert result is not None
    assert len(result.associated_documents) == 1
    doc_data = result.associated_documents[0]
    assert doc_data.pgpub_document_meta_data is not None
    assert doc_data.grant_document_meta_data is None


@pytest.mark.asyncio
async def test_get_associated_documents_only_grant(client):
    """Test get_associated_documents with only Grant metadata"""
    client, mock_session = client
    
    mock_response_data = {
        "count": 1,
        "patentFileWrapperDataBag": [{
            "applicationNumberText": "14412875",
            "pgpubDocumentMetaData": None,
            "grantDocumentMetaData": {
                "productIdentifier": "GRANT-001",
                "zipFileName": "grant_14412875.zip",
                "fileCreateDateTime": "2023-06-15T10:30:00Z",
                "xmlFileName": "grant_14412875.xml",
                "fileLocationURI": "https://example.com/grant/14412875"
            }
        }]
    }
    
    mock_response = Mock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value=mock_response_data)
    
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = mock_response
    mock_session.get.return_value = async_cm
    
    result = await client.get_associated_documents("14412875")
    
    assert result is not None
    assert len(result.associated_documents) == 1
    doc_data = result.associated_documents[0]
    assert doc_data.pgpub_document_meta_data is None
    assert doc_data.grant_document_meta_data is not None


@pytest.mark.asyncio
async def test_get_associated_documents_empty_response(client):
    """Test get_associated_documents with empty response"""
    client, mock_session = client
    
    mock_response_data = {
        "count": 0,
        "patentFileWrapperDataBag": []
    }
    
    mock_response = Mock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value=mock_response_data)
    
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = mock_response
    mock_session.get.return_value = async_cm
    
    result = await client.get_associated_documents("14412875")
    
    assert result is not None
    assert result.count == 0
    assert len(result.associated_documents) == 0


@pytest.mark.asyncio
async def test_get_associated_documents_not_found(client):
    """Test get_associated_documents with non-existent application number"""
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
        await client.get_associated_documents("99999999")
    
    assert exc_info.value.code == 404
    assert "Not Found" in str(exc_info.value)


@pytest.mark.asyncio
async def test_get_associated_documents_bad_request(client):
    """Test get_associated_documents with bad request"""
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
        await client.get_associated_documents("invalid")
    
    assert exc_info.value.code == 400
    assert "Bad Request" in str(exc_info.value)
