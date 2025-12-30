"""
Integration tests for petition decision endpoints.
Requires USPTO_API_KEY environment variable to be set.
"""
import pytest
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOError


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_petition_decisions_get_basic(client):
    """
    Test search_petition_decisions_get with basic query.
    """
    await asyncio.sleep(2)  # Rate limiting
    
    result = await client.search_petition_decisions_get(limit=10)
    
    assert result is not None
    assert hasattr(result, 'count')
    assert hasattr(result, 'petition_decision_bag')
    assert isinstance(result.count, int)
    assert isinstance(result.petition_decision_bag, list)
    assert result.count >= 0
    
    print(f"✓ Retrieved {result.count} petition decisions")
    print(f"  Found {len(result.petition_decision_bag)} results")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_petition_decisions_get_with_query(client):
    """
    Test search_petition_decisions_get with query string.
    """
    await asyncio.sleep(2)  # Rate limiting
    
    result = await client.search_petition_decisions_get(
        q="decisionTypeCodeDescriptionText:Denied",
        limit=10
    )
    
    assert result is not None
    assert result.count >= 0
    assert isinstance(result.petition_decision_bag, list)
    
    print(f"✓ Searched for denied decisions")
    print(f"  Count: {result.count}")
    print(f"  Found {len(result.petition_decision_bag)} results")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_petition_decisions_get_with_filters(client):
    """
    Test search_petition_decisions_get with filters.
    """
    await asyncio.sleep(2)  # Rate limiting
    
    result = await client.search_petition_decisions_get(
        q="Denied",
        filters="businessEntityStatusCategory Small",
        limit=10
    )
    
    assert result is not None
    assert result.count >= 0
    
    await asyncio.sleep(2)  # Rate limiting
    
    print(f"✓ Searched with filters")
    print(f"  Count: {result.count}")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_petition_decisions_post_basic(client):
    """
    Test search_petition_decisions POST method with basic payload.
    """
    await asyncio.sleep(2)  # Rate limiting
    
    payload = {
        "q": "Denied",
        "pagination": {
            "offset": 0,
            "limit": 10
        }
    }
    
    result = await client.search_petition_decisions(payload)
    
    assert result is not None
    assert result.count >= 0
    assert isinstance(result.petition_decision_bag, list)
    
    await asyncio.sleep(2)  # Rate limiting
    
    print(f"✓ Searched via POST")
    print(f"  Count: {result.count}")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_petition_decisions_download_get_basic(client):
    """
    Test search_petition_decisions_download_get GET method with basic query.
    """
    await asyncio.sleep(2)  # Rate limiting
    
    result = await client.search_petition_decisions_download_get(
        q="Denied",
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
async def test_search_petition_decisions_download_post_basic(client):
    """
    Test search_petition_decisions_download POST method with basic payload.
    """
    await asyncio.sleep(2)  # Rate limiting
    
    payload = {
        "q": "Denied",
        "pagination": {
            "offset": 0,
            "limit": 10
        }
    }
    
    result = await client.search_petition_decisions_download(payload)
    
    assert result is not None
    assert result.count >= 0
    
    await asyncio.sleep(2)  # Rate limiting
    
    print(f"✓ Downloaded search results via POST")
    print(f"  Count: {result.count}")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_petition_decisions_download_csv_format(client):
    """
    Test search_petition_decisions_download_get with CSV format.
    """
    await asyncio.sleep(2)  # Rate limiting
    
    result = await client.search_petition_decisions_download_get(
        q="Denied",
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
async def test_get_petition_decision_basic(client):
    """
    Test get_petition_decision with a known identifier.
    Note: This test may fail if the identifier doesn't exist - that's expected.
    """
    await asyncio.sleep(2)  # Rate limiting
    
    # Use a known identifier format (UUID)
    # This may need to be updated with an actual identifier from search results
    identifier = "6779f1be-0f3b-5775-b9d3-dcfdb83171c3"
    
    try:
        result = await client.get_petition_decision(identifier)
        
        assert result is not None
        assert hasattr(result, 'count')
        assert hasattr(result, 'petition_decision_bag')
        assert result.count >= 0
        
        await asyncio.sleep(2)  # Rate limiting
        
        print(f"✓ Retrieved petition decision")
        print(f"  Identifier: {identifier}")
        print(f"  Count: {result.count}")
    except USPTOError as e:
        if e.code == 404 or str(e.code) == "404":
            print(f"⚠ Petition decision not found (expected if identifier is invalid)")
        else:
            raise


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_petition_decision_with_documents(client):
    """
    Test get_petition_decision with includeDocuments=true.
    """
    await asyncio.sleep(2)  # Rate limiting
    
    # First, get a valid identifier from search
    search_result = await client.search_petition_decisions_get(limit=1)
    
    await asyncio.sleep(2)  # Rate limiting
    
    if search_result.petition_decision_bag:
        identifier = search_result.petition_decision_bag[0].petition_decision_record_identifier
        
        result = await client.get_petition_decision(identifier, include_documents=True)
        
        assert result is not None
        assert result.count >= 0
        
        await asyncio.sleep(2)  # Rate limiting
        
        print(f"✓ Retrieved petition decision with documents")
        print(f"  Identifier: {identifier}")
    else:
        print("⚠ No petition decisions found to test with documents")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_petition_decision_not_found(client):
    """
    Test get_petition_decision with invalid identifier.
    """
    await asyncio.sleep(2)  # Rate limiting
    
    with pytest.raises(USPTOError) as exc_info:
        await client.get_petition_decision("invalid-identifier-12345")
    
    assert exc_info.value.code == 404 or str(exc_info.value.code) == "404"
    
    await asyncio.sleep(2)  # Rate limiting
    
    print("✓ Error handling works correctly for invalid identifier")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_petition_decisions_verify_structure(client):
    """
    Verify the structure of petition decision search results.
    """
    await asyncio.sleep(2)  # Rate limiting
    
    result = await client.search_petition_decisions_get(limit=5)
    
    assert result is not None
    assert isinstance(result.count, int)
    assert isinstance(result.petition_decision_bag, list)
    
    if len(result.petition_decision_bag) > 0:
        first_decision = result.petition_decision_bag[0]
        assert hasattr(first_decision, 'petition_decision_record_identifier')
        # Verify common fields exist
        if first_decision.petition_decision_record_identifier:
            assert isinstance(first_decision.petition_decision_record_identifier, str)
    
    await asyncio.sleep(2)  # Rate limiting
    
    print(f"✓ Verified petition decision response structure")
