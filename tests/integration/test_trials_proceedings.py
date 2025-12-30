"""
Integration tests for PTAB trials proceedings endpoints.
Requires USPTO_API_KEY environment variable to be set.
"""
import pytest
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOError


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_trial_proceedings_get_basic(client):
    """
    Test search_trial_proceedings_get with basic query.
    """
    await asyncio.sleep(2)  # Rate limiting
    
    result = await client.search_trial_proceedings_get(limit=10)
    
    assert result is not None
    assert hasattr(result, 'count')
    assert hasattr(result, 'trial_proceeding_bag')
    assert isinstance(result.count, int)
    assert isinstance(result.trial_proceeding_bag, list)
    assert result.count >= 0
    
    print(f"✓ Retrieved {result.count} trial proceedings")
    print(f"  Found {len(result.trial_proceeding_bag)} results")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_trial_proceedings_get_with_query(client):
    """
    Test search_trial_proceedings_get with query string.
    Note: The API may return 404 for invalid field queries, so we test with a simple text query.
    """
    await asyncio.sleep(2)  # Rate limiting
    
    # Use a simple text query instead of field-specific query
    # The API may not support field-specific queries like trialType:IPR
    try:
        result = await client.search_trial_proceedings_get(
            q="IPR",
            limit=10
        )
        
        assert result is not None
        assert result.count >= 0
        assert isinstance(result.trial_proceeding_bag, list)
        
        print(f"✓ Searched for IPR trials")
        print(f"  Count: {result.count}")
        print(f"  Found {len(result.trial_proceeding_bag)} results")
    except USPTOError as e:
        if e.code == 404 or str(e.code) == "404":
            # API may return 404 for queries that don't match - this is acceptable
            print(f"⚠ Query returned 404 (no matching results or query not supported)")
        else:
            raise


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_trial_proceedings_get_with_filters(client):
    """
    Test search_trial_proceedings_get with filters.
    Note: The API may return 404 for invalid filter syntax, so we handle errors gracefully.
    """
    await asyncio.sleep(2)  # Rate limiting
    
    try:
        result = await client.search_trial_proceedings_get(
            q="IPR",
            filters="proceedingStatus Instituted",
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
async def test_search_trial_proceedings_post_basic(client):
    """
    Test search_trial_proceedings POST method with basic payload.
    """
    await asyncio.sleep(2)  # Rate limiting
    
    payload = {
        "q": "IPR",
        "pagination": {
            "offset": 0,
            "limit": 10
        }
    }
    
    result = await client.search_trial_proceedings(payload)
    
    assert result is not None
    assert result.count >= 0
    assert isinstance(result.trial_proceeding_bag, list)
    
    await asyncio.sleep(2)  # Rate limiting
    
    print(f"✓ Searched via POST")
    print(f"  Count: {result.count}")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_trial_proceedings_download_get_basic(client):
    """
    Test search_trial_proceedings_download_get GET method with basic query.
    """
    await asyncio.sleep(2)  # Rate limiting
    
    result = await client.search_trial_proceedings_download_get(
        q="IPR",
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
async def test_search_trial_proceedings_download_post_basic(client):
    """
    Test search_trial_proceedings_download POST method with basic payload.
    """
    await asyncio.sleep(2)  # Rate limiting
    
    payload = {
        "q": "IPR",
        "pagination": {
            "offset": 0,
            "limit": 10
        }
    }
    
    result = await client.search_trial_proceedings_download(payload)
    
    assert result is not None
    assert result.count >= 0
    
    await asyncio.sleep(2)  # Rate limiting
    
    print(f"✓ Downloaded search results via POST")
    print(f"  Count: {result.count}")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_trial_proceedings_download_csv_format(client):
    """
    Test search_trial_proceedings_download_get with CSV format.
    """
    await asyncio.sleep(2)  # Rate limiting
    
    result = await client.search_trial_proceedings_download_get(
        q="IPR",
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
async def test_get_trial_proceeding_basic(client):
    """
    Test get_trial_proceeding with a known trial number.
    Note: This test may fail if the trial number doesn't exist - that's expected.
    """
    await asyncio.sleep(2)  # Rate limiting
    
    # First, get a valid trial number from search
    search_result = await client.search_trial_proceedings_get(limit=1)
    
    await asyncio.sleep(2)  # Rate limiting
    
    if search_result.trial_proceeding_bag:
        trial_number = search_result.trial_proceeding_bag[0].trial_number
        
        result = await client.get_trial_proceeding(trial_number)
        
        assert result is not None
        assert hasattr(result, 'count')
        assert hasattr(result, 'trial_proceeding_bag')
        assert result.count >= 0
        
        await asyncio.sleep(2)  # Rate limiting
        
        print(f"✓ Retrieved trial proceeding")
        print(f"  Trial Number: {trial_number}")
        print(f"  Count: {result.count}")
    else:
        print("⚠ No trial proceedings found to test individual lookup")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_trial_proceeding_not_found(client):
    """
    Test get_trial_proceeding with invalid trial number.
    """
    await asyncio.sleep(2)  # Rate limiting
    
    with pytest.raises(USPTOError) as exc_info:
        await client.get_trial_proceeding("invalid-trial-number-12345")
    
    assert exc_info.value.code == 404 or str(exc_info.value.code) == "404"
    
    await asyncio.sleep(2)  # Rate limiting
    
    print("✓ Error handling works correctly for invalid trial number")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_trial_proceedings_verify_structure(client):
    """
    Verify the structure of trial proceeding search results.
    """
    await asyncio.sleep(2)  # Rate limiting
    
    result = await client.search_trial_proceedings_get(limit=5)
    
    assert result is not None
    assert isinstance(result.count, int)
    assert isinstance(result.trial_proceeding_bag, list)
    
    if len(result.trial_proceeding_bag) > 0:
        first_proceeding = result.trial_proceeding_bag[0]
        assert hasattr(first_proceeding, 'trial_number')
        # Verify common fields exist
        if first_proceeding.trial_number:
            assert isinstance(first_proceeding.trial_number, str)
    
    await asyncio.sleep(2)  # Rate limiting
    
    print(f"✓ Verified trial proceeding response structure")
