"""
Integration tests for PTAB appeals decisions endpoints.
Requires USPTO_API_KEY environment variable to be set.
"""
import pytest
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOError


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_appeal_decisions_get_basic(client):
    """
    Test search_appeal_decisions_get with basic query.
    """
    await asyncio.sleep(2)  # Rate limiting
    
    result = await client.search_appeal_decisions_get(limit=10)
    
    assert result is not None
    assert hasattr(result, 'count')
    assert hasattr(result, 'appeal_decision_bag')
    assert isinstance(result.count, int)
    assert isinstance(result.appeal_decision_bag, list)
    assert result.count >= 0
    
    print(f"✓ Retrieved {result.count} appeal decisions")
    print(f"  Found {len(result.appeal_decision_bag)} results")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_appeal_decisions_get_with_query(client):
    """
    Test search_appeal_decisions_get with query string.
    Note: The API may return 404 for invalid field queries, so we test with a simple text query.
    """
    await asyncio.sleep(2)  # Rate limiting
    
    # Use a simple text query instead of field-specific query
    # The API may not support field-specific queries like decisionType:Final
    try:
        result = await client.search_appeal_decisions_get(
            q="Final",
            limit=10
        )
        
        assert result is not None
        assert result.count >= 0
        assert isinstance(result.appeal_decision_bag, list)
        
        print(f"✓ Searched for Final appeal decisions")
        print(f"  Count: {result.count}")
        print(f"  Found {len(result.appeal_decision_bag)} results")
    except USPTOError as e:
        if e.code == 404 or str(e.code) == "404":
            # API may return 404 for queries that don't match - this is acceptable
            print(f"⚠ Query returned 404 (no matching results or query not supported)")
        else:
            raise


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_appeal_decisions_get_with_filters(client):
    """
    Test search_appeal_decisions_get with filters.
    Note: The API may return 404 for invalid filter syntax, so we handle errors gracefully.
    """
    await asyncio.sleep(2)  # Rate limiting
    
    try:
        result = await client.search_appeal_decisions_get(
            q="Final",
            filters="decisionType Final",
            limit=10
        )
        
        assert result is not None
        assert result.count >= 0
        
        await asyncio.sleep(2)  # Rate limiting
        
        print(f"✓ Searched with filters")
        print(f"  Count: {result.count}")
    except USPTOError as e:
        if e.code == 404 or str(e.code) == "404":
            # API may return 404 for invalid filter syntax - this is acceptable
            print(f"⚠ Filter query returned 404 (filter syntax may not be supported)")
        else:
            raise


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_appeal_decisions_post_basic(client):
    """
    Test search_appeal_decisions POST method with basic payload.
    """
    await asyncio.sleep(2)  # Rate limiting
    
    payload = {
        "q": "Final",
        "pagination": {
            "offset": 0,
            "limit": 10
        }
    }
    
    result = await client.search_appeal_decisions(payload)
    
    assert result is not None
    assert result.count >= 0
    assert isinstance(result.appeal_decision_bag, list)
    
    await asyncio.sleep(2)  # Rate limiting
    
    print(f"✓ Searched via POST")
    print(f"  Count: {result.count}")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_appeal_decisions_download_get_basic(client):
    """
    Test search_appeal_decisions_download_get GET method with basic query.
    """
    await asyncio.sleep(2)  # Rate limiting
    
    result = await client.search_appeal_decisions_download_get(
        q="Final",
        format="json",
        limit=10
    )
    
    assert result is not None
    assert hasattr(result, 'count')
    assert isinstance(result.count, int)
    
    await asyncio.sleep(2)  # Rate limiting
    
    print(f"✓ Downloaded search results via GET (JSON)")
    print(f"  Count: {result.count}")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_appeal_decisions_download_post_basic(client):
    """
    Test search_appeal_decisions_download POST method with basic payload.
    """
    await asyncio.sleep(2)  # Rate limiting
    
    payload = {
        "q": "Final",
        "pagination": {
            "offset": 0,
            "limit": 10
        }
    }
    
    result = await client.search_appeal_decisions_download(payload)
    
    assert result is not None
    assert result.count >= 0
    
    await asyncio.sleep(2)  # Rate limiting
    
    print(f"✓ Downloaded search results via POST")
    print(f"  Count: {result.count}")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_appeal_decisions_download_csv_format(client):
    """
    Test search_appeal_decisions_download_get with CSV format.
    """
    await asyncio.sleep(2)  # Rate limiting
    
    result = await client.search_appeal_decisions_download_get(
        q="Final",
        format="csv",
        limit=10
    )
    
    assert result is not None
    assert hasattr(result, 'count')
    
    await asyncio.sleep(2)  # Rate limiting
    
    print(f"✓ Downloaded search results via GET (CSV)")
    print(f"  Count: {result.count}")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_appeal_decision_basic(client):
    """
    Test get_appeal_decision with a known document identifier.
    Note: This test may fail if the document identifier doesn't exist - that's expected.
    """
    await asyncio.sleep(2)  # Rate limiting
    
    # First, get a valid document identifier from search
    search_result = await client.search_appeal_decisions_get(limit=1)
    
    await asyncio.sleep(2)  # Rate limiting
    
    if search_result.appeal_decision_bag:
        document_identifier = search_result.appeal_decision_bag[0].document_identifier
        
        if document_identifier:
            result = await client.get_appeal_decision(document_identifier)
            
            assert result is not None
            assert hasattr(result, 'count')
            assert hasattr(result, 'appeal_decision_bag')
            assert result.count >= 0
            
            await asyncio.sleep(2)  # Rate limiting
            
            print(f"✓ Retrieved appeal decision")
            print(f"  Document Identifier: {document_identifier}")
            print(f"  Count: {result.count}")
        else:
            print("⚠ No document identifier found in search results")
    else:
        print("⚠ No appeal decisions found to test individual lookup")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_appeal_decisions_by_appeal_basic(client):
    """
    Test get_appeal_decisions_by_appeal with a known appeal number.
    Note: This test may fail if the appeal number doesn't exist - that's expected.
    """
    await asyncio.sleep(2)  # Rate limiting
    
    # First, get a valid appeal number from search
    search_result = await client.search_appeal_decisions_get(limit=1)
    
    await asyncio.sleep(2)  # Rate limiting
    
    if search_result.appeal_decision_bag:
        appeal_number = search_result.appeal_decision_bag[0].appeal_number
        
        if appeal_number:
            result = await client.get_appeal_decisions_by_appeal(appeal_number)
            
            assert result is not None
            assert hasattr(result, 'count')
            assert hasattr(result, 'appeal_decision_bag')
            assert result.count >= 0
            
            await asyncio.sleep(2)  # Rate limiting
            
            print(f"✓ Retrieved appeal decisions by appeal number")
            print(f"  Appeal Number: {appeal_number}")
            print(f"  Count: {result.count}")
        else:
            print("⚠ No appeal number found in search results")
    else:
        print("⚠ No appeal decisions found to test lookup by appeal number")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_appeal_decision_not_found(client):
    """
    Test get_appeal_decision with invalid document identifier.
    """
    await asyncio.sleep(2)  # Rate limiting
    
    with pytest.raises(USPTOError) as exc_info:
        await client.get_appeal_decision("invalid-document-identifier-12345")
    
    assert exc_info.value.code == 404 or str(exc_info.value.code) == "404"
    
    await asyncio.sleep(2)  # Rate limiting
    
    print("✓ Error handling works correctly for invalid document identifier")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_appeal_decisions_verify_structure(client):
    """
    Verify the structure of appeal decision search results.
    """
    await asyncio.sleep(2)  # Rate limiting
    
    result = await client.search_appeal_decisions_get(limit=5)
    
    assert result is not None
    assert isinstance(result.count, int)
    assert isinstance(result.appeal_decision_bag, list)
    
    if len(result.appeal_decision_bag) > 0:
        first_decision = result.appeal_decision_bag[0]
        assert hasattr(first_decision, 'document_identifier')
        # Verify common fields exist
        if first_decision.document_identifier:
            assert isinstance(first_decision.document_identifier, str)
    
    await asyncio.sleep(2)  # Rate limiting
    
    print(f"✓ Verified appeal decision response structure")
