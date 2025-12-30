"""
Integration tests for associated-documents endpoint.
Requires USPTO_API_KEY environment variable to be set.
"""
import pytest
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOError


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_associated_documents_basic(client, known_application_numbers):
    """
    Test get_associated_documents with a valid application number.
    """
    serial_number = known_application_numbers["utility"]
    result = await client.get_associated_documents(serial_number)
    
    assert result is not None
    assert hasattr(result, 'associated_documents')
    assert isinstance(result.associated_documents, list)
    assert result.count >= 0
    
    print(f"✓ Retrieved associated documents data for application {serial_number}")
    print(f"  Count: {result.count}")
    print(f"  Found {len(result.associated_documents)} associated document records")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_associated_documents_verify_structure(client, known_application_numbers):
    """
    Verify AssociatedDocumentsResponse structure and fields.
    """
    serial_number = known_application_numbers["utility"]
    result = await client.get_associated_documents(serial_number)
    
    assert result is not None
    assert hasattr(result, 'count')
    assert hasattr(result, 'associated_documents')
    assert isinstance(result.count, int)
    assert isinstance(result.associated_documents, list)
    
    # If there are associated documents, verify their structure
    if len(result.associated_documents) > 0:
        app_docs = result.associated_documents[0]
        assert hasattr(app_docs, 'application_number')
        assert hasattr(app_docs, 'pgpub_document_meta_data')
        assert hasattr(app_docs, 'grant_document_meta_data')
        
        # Verify application number matches
        assert app_docs.application_number == serial_number
        
        # If pgpub metadata exists, verify its structure
        if app_docs.pgpub_document_meta_data:
            pgpub = app_docs.pgpub_document_meta_data
            assert hasattr(pgpub, 'product_identifier')
            assert hasattr(pgpub, 'zip_file_name')
            assert hasattr(pgpub, 'file_location_uri')
        
        # If grant metadata exists, verify its structure
        if app_docs.grant_document_meta_data:
            grant = app_docs.grant_document_meta_data
            assert hasattr(grant, 'product_identifier')
            assert hasattr(grant, 'zip_file_name')
            assert hasattr(grant, 'file_location_uri')
    
    await asyncio.sleep(1)  # Rate limiting
    
    print(f"✓ Verified associated documents structure for application {serial_number}")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_associated_documents_multiple_applications(client, known_application_numbers):
    """
    Test get_associated_documents with multiple known application numbers.
    """
    applications = [
        known_application_numbers["utility"],
        known_application_numbers["utility_2"]
    ]
    
    results = []
    for app_num in applications:
        result = await client.get_associated_documents(app_num)
        results.append(result)
        await asyncio.sleep(1)  # Rate limiting
    
    # Verify all requests succeeded
    for i, result in enumerate(results):
        assert result is not None
        assert result.count >= 0
        print(f"✓ Application {applications[i]}: count={result.count}, "
              f"associated_documents={len(result.associated_documents)}")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_associated_documents_not_found(client):
    """
    Test behavior when application number is not found.
    """
    invalid_app = "99999999"  # Likely invalid
    
    with pytest.raises(USPTOError) as exc_info:
        await client.get_associated_documents(invalid_app)
    
    # Error code may be string or int depending on API response
    assert exc_info.value.code == 404 or str(exc_info.value.code) == "404"
    assert "404" in str(exc_info.value) or "Not Found" in str(exc_info.value)
    print("✓ Correctly raised USPTOError for invalid application number")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_associated_documents_verify_data_types(client, known_application_numbers):
    """
    Verify that returned data has correct types.
    """
    serial_number = known_application_numbers["utility"]
    result = await client.get_associated_documents(serial_number)
    
    assert isinstance(result.count, int)
    assert isinstance(result.associated_documents, list)
    
    if len(result.associated_documents) > 0:
        app_docs = result.associated_documents[0]
        assert isinstance(app_docs.application_number, str)
        
        if app_docs.pgpub_document_meta_data:
            pgpub = app_docs.pgpub_document_meta_data
            # Verify optional fields are correct types when present
            if pgpub.product_identifier is not None:
                assert isinstance(pgpub.product_identifier, str)
            if pgpub.zip_file_name is not None:
                assert isinstance(pgpub.zip_file_name, str)
            if pgpub.file_location_uri is not None:
                assert isinstance(pgpub.file_location_uri, str)
        
        if app_docs.grant_document_meta_data:
            grant = app_docs.grant_document_meta_data
            # Verify optional fields are correct types when present
            if grant.product_identifier is not None:
                assert isinstance(grant.product_identifier, str)
            if grant.zip_file_name is not None:
                assert isinstance(grant.zip_file_name, str)
            if grant.file_location_uri is not None:
                assert isinstance(grant.file_location_uri, str)
    
    await asyncio.sleep(1)  # Rate limiting
    
    print(f"✓ Verified data types for application {serial_number}")
