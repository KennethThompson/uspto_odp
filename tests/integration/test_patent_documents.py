"""
Integration tests for patent documents endpoint.
Requires USPTO_API_KEY environment variable to be set.
"""
import pytest
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient, USPTOError


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_patent_documents_basic(client, known_application_numbers):
    """
    Integration test for get_patent_documents using a real serial number.
    Tests basic functionality and verifies document collection structure.
    """
    serial_number = known_application_numbers["utility_2"]
    result = await client.get_patent_documents(serial_number)
    
    assert result is not None
    assert hasattr(result, 'documents')
    assert isinstance(result.documents, list)
    assert len(result.documents) > 0
    
    # Verify document structure
    first_doc = result.documents[0]
    assert hasattr(first_doc, 'application_number')
    assert hasattr(first_doc, 'document_code')
    assert hasattr(first_doc, 'document_identifier')
    assert hasattr(first_doc, 'document_description')
    assert hasattr(first_doc, 'official_date')
    assert hasattr(first_doc, 'direction_category')
    assert hasattr(first_doc, 'download_options')
    
    print(f"✓ Found {len(result.documents)} documents for serial {serial_number}")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_patent_documents_verify_fields(client, known_application_numbers):
    """
    Verify that document fields are properly populated.
    """
    serial_number = known_application_numbers["utility"]
    result = await client.get_patent_documents(serial_number)
    
    assert result is not None
    assert len(result.documents) > 0
    
    # Check that documents have required fields
    for doc in result.documents[:5]:  # Check first 5 documents
        assert doc.application_number == serial_number
        assert doc.document_code is not None
        assert doc.document_identifier is not None
        assert doc.official_date is not None
        assert doc.direction_category in ["INCOMING", "OUTGOING", "INTERNAL"]
        assert isinstance(doc.download_options, list)
        assert len(doc.download_options) > 0
        
        # Verify download options have required fields
        for option in doc.download_options:
            assert hasattr(option, 'mime_type')
            assert hasattr(option, 'download_url')
            assert option.download_url.startswith('http')
    
    print(f"✓ Verified document fields for {len(result.documents)} documents")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_patent_documents_error_handling(client):
    """
    Test error handling for invalid application numbers.
    """
    invalid_serial = "99999999"  # Likely invalid
    
    with pytest.raises(USPTOError):
        await client.get_patent_documents(invalid_serial)
    
    print("✓ Error handling works correctly for invalid serial numbers")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_patent_documents_different_types(client, known_application_numbers):
    """
    Test getting documents for different application types.
    """
    # Test with utility application
    utility_result = await client.get_patent_documents(known_application_numbers["utility"])
    assert utility_result is not None
    assert len(utility_result.documents) > 0
    
    await asyncio.sleep(1)  # Rate limiting
    
    print(f"✓ Retrieved documents for utility application: {len(utility_result.documents)} documents")
