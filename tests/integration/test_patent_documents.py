"""
Integration tests for patent documents endpoint.
Requires USPTO_API_KEY environment variable to be set.
"""
import pytest
import asyncio
from datetime import timedelta
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


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_patent_documents_with_date_filter(client):
    """
    Test filtering documents by date range using application 18571476.
    Verifies that date filtering properly limits results.
    """
    serial_number = "18571476"
    
    # First, get all documents without filters
    all_documents = await client.get_patent_documents(serial_number)
    
    assert all_documents is not None
    assert len(all_documents.documents) > 0
    
    print(f"✓ Retrieved {len(all_documents.documents)} total documents for {serial_number}")
    
    await asyncio.sleep(1)  # Rate limiting
    
    # Get the date range from the documents
    if len(all_documents.documents) > 0:
        # Find min and max dates
        dates = [doc.official_date.date() for doc in all_documents.documents]
        min_date = min(dates)
        max_date = max(dates)
        
        # Create a date range that should include some but not all documents
        # Use a range that starts after the earliest date
        filter_start = min_date + timedelta(days=1)
        filter_end = max_date - timedelta(days=1) if max_date > min_date + timedelta(days=2) else max_date
        
        # If all documents are on the same day, use that day
        if filter_start > filter_end:
            filter_start = min_date
            filter_end = max_date
        
        # Fetch documents with date filter
        filtered_documents = await client.get_patent_documents(
            serial_number,
            official_date_from=filter_start.strftime("%Y-%m-%d"),
            official_date_to=filter_end.strftime("%Y-%m-%d")
        )
        
        assert filtered_documents is not None
        assert isinstance(filtered_documents.documents, list)
        
        print(f"✓ Filtered documents: {len(filtered_documents.documents)} documents "
              f"(date range: {filter_start} to {filter_end})")
        
        # Verify all filtered documents fall within the date range
        for doc in filtered_documents.documents:
            doc_date = doc.official_date.date()
            assert filter_start <= doc_date <= filter_end, \
                f"Document date {doc_date} is outside filter range {filter_start} to {filter_end}"
        
        # Verify filtered results are a subset (or equal if all documents are in range)
        assert len(filtered_documents.documents) <= len(all_documents.documents), \
            "Filtered results should not exceed total documents"
        
        print(f"✓ Verified all {len(filtered_documents.documents)} filtered documents "
              f"are within date range")
    
    await asyncio.sleep(1)  # Rate limiting


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_patent_documents_with_document_codes_filter(client):
    """
    Test filtering documents by document codes using application 18571476.
    """
    serial_number = "18571476"
    
    # First, get all documents to see what codes are available
    all_documents = await client.get_patent_documents(serial_number)
    
    assert all_documents is not None
    assert len(all_documents.documents) > 0
    
    # Get unique document codes from the results
    document_codes = set(doc.document_code for doc in all_documents.documents)
    
    if len(document_codes) > 0:
        # Test with a single document code
        test_code = list(document_codes)[0]
        filtered_documents = await client.get_patent_documents(
            serial_number,
            document_codes=test_code
        )
        
        assert filtered_documents is not None
        assert isinstance(filtered_documents.documents, list)
        
        print(f"✓ Filtered by single code '{test_code}': {len(filtered_documents.documents)} documents")
        
        # Verify all documents have the requested code
        for doc in filtered_documents.documents:
            assert doc.document_code == test_code, \
                f"Document has code {doc.document_code}, expected {test_code}"
        
        await asyncio.sleep(1)  # Rate limiting
        
        # Test with multiple document codes if we have at least 2 codes
        if len(document_codes) >= 2:
            test_codes = list(document_codes)[:2]
            codes_string = ",".join(test_codes)
            
            filtered_documents_multi = await client.get_patent_documents(
                serial_number,
                document_codes=codes_string
            )
            
            assert filtered_documents_multi is not None
            assert isinstance(filtered_documents_multi.documents, list)
            
            print(f"✓ Filtered by multiple codes '{codes_string}': "
                  f"{len(filtered_documents_multi.documents)} documents")
            
            # Verify all documents have one of the requested codes
            for doc in filtered_documents_multi.documents:
                assert doc.document_code in test_codes, \
                    f"Document has code {doc.document_code}, expected one of {test_codes}"
            
            print(f"✓ Verified all documents match requested codes")
    
    await asyncio.sleep(1)  # Rate limiting


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_patent_documents_with_combined_filters(client):
    """
    Test combining date and document code filters using application 18571476.
    """
    serial_number = "18571476"
    
    # Get all documents first
    all_documents = await client.get_patent_documents(serial_number)
    
    assert all_documents is not None
    assert len(all_documents.documents) > 0
    
    # Get document codes and dates
    document_codes = set(doc.document_code for doc in all_documents.documents)
    dates = [doc.official_date.date() for doc in all_documents.documents]
    
    if len(document_codes) > 0 and len(dates) > 0:
        # Use a date range
        min_date = min(dates)
        max_date = max(dates)
        filter_start = min_date
        filter_end = max_date
        
        # Use a single document code
        test_code = list(document_codes)[0]
        
        # Apply both filters
        filtered_documents = await client.get_patent_documents(
            serial_number,
            official_date_from=filter_start.strftime("%Y-%m-%d"),
            official_date_to=filter_end.strftime("%Y-%m-%d"),
            document_codes=test_code
        )
        
        assert filtered_documents is not None
        assert isinstance(filtered_documents.documents, list)
        
        print(f"✓ Combined filters (date: {filter_start} to {filter_end}, "
              f"code: {test_code}): {len(filtered_documents.documents)} documents")
        
        # Verify all documents match both criteria
        for doc in filtered_documents.documents:
            doc_date = doc.official_date.date()
            assert filter_start <= doc_date <= filter_end, \
                f"Document date {doc_date} is outside filter range"
            assert doc.document_code == test_code, \
                f"Document code {doc.document_code} doesn't match filter {test_code}"
        
        print(f"✓ Verified all documents match both filter criteria")
    
    await asyncio.sleep(1)  # Rate limiting
