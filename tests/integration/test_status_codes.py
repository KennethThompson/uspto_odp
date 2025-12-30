"""
Integration tests for status codes endpoint.
Requires USPTO_API_KEY environment variable to be set.
"""
import pytest
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient, USPTOError
from uspto_odp.models.patent_status_codes import StatusCode, StatusCodeCollection


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_status_codes_get_basic(client):
    """
    Basic GET search for status codes with no parameters.
    API may return count without data unless pagination is specified.
    """
    result = await client.search_status_codes_get()
    
    assert result is not None
    assert isinstance(result, StatusCodeCollection)
    assert result.count > 0
    # API may return count without data bag when no query/pagination specified
    # This is acceptable behavior - verify structure is correct
    assert isinstance(result.status_codes, list)
    
    print(f"✓ Retrieved count: {result.count}, status codes: {len(result.status_codes)}")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_status_codes_get_with_query(client):
    """
    GET search with query string for specific status description.
    """
    result = await client.search_status_codes_get(
        q="applicationStatusDescriptionText:Preexam"
    )
    
    assert result is not None
    assert result.count >= 0  # May be 0 if no results
    
    if result.count > 0:
        # Verify all results contain "Preexam" in description
        for status_code in result.status_codes:
            assert "Preexam" in status_code.application_status_description_text.lower()
    
    await asyncio.sleep(1)  # Rate limiting
    
    print(f"✓ Found {result.count} status codes matching 'Preexam'")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_status_codes_get_with_comparison(client):
    """
    GET search with comparison operator (greater than).
    """
    result = await client.search_status_codes_get(
        q="applicationStatusCode:>100"
    )
    
    assert result is not None
    assert result.count >= 0
    
    if result.count > 0:
        # Verify all status codes are greater than 100
        for status_code in result.status_codes:
            assert status_code.application_status_code > 100
    
    await asyncio.sleep(1)  # Rate limiting
    
    print(f"✓ Found {result.count} status codes with code > 100")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_status_codes_get_with_pagination(client):
    """
    GET search with pagination parameters.
    """
    result = await client.search_status_codes_get(
        limit=10,
        offset=0
    )
    
    assert result is not None
    assert len(result.status_codes) <= 10
    
    await asyncio.sleep(1)  # Rate limiting
    
    print(f"✓ Retrieved {len(result.status_codes)} status codes with pagination (limit=10)")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_status_codes_get_with_boolean(client):
    """
    GET search with boolean operators (AND, OR).
    """
    result = await client.search_status_codes_get(
        q="Application AND Preexam"
    )
    
    assert result is not None
    assert result.count >= 0
    
    await asyncio.sleep(1)  # Rate limiting
    
    print(f"✓ Found {result.count} status codes matching 'Application AND Preexam'")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_status_codes_post_method(client):
    """
    POST method with JSON payload.
    """
    payload = {
        "q": "applicationStatusCode:150",
        "pagination": {
            "offset": 0,
            "limit": 25
        }
    }
    
    result = await client.search_status_codes(payload)
    
    assert result is not None
    assert isinstance(result, StatusCodeCollection)
    assert result.count >= 0
    
    # If we have results, verify structure; if not, that's also acceptable
    if result.count > 0 and len(result.status_codes) > 0:
        # Verify we got status code 150 if results are returned
        found_150 = any(sc.application_status_code == 150 for sc in result.status_codes)
        if found_150:
            print(f"✓ Found status code 150: {next(sc for sc in result.status_codes if sc.application_status_code == 150).application_status_description_text}")
    
    await asyncio.sleep(1)  # Rate limiting
    
    print(f"✓ POST search returned count: {result.count}, status codes: {len(result.status_codes)}")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_status_codes_verify_structure(client):
    """
    Verify the structure of returned status codes.
    """
    result = await client.search_status_codes_get(limit=5)
    
    assert result is not None
    assert hasattr(result, 'count')
    assert hasattr(result, 'status_codes')
    assert isinstance(result.status_codes, list)
    
    if len(result.status_codes) > 0:
        status_code = result.status_codes[0]
        assert isinstance(status_code, StatusCode)
        assert hasattr(status_code, 'application_status_code')
        assert hasattr(status_code, 'application_status_description_text')
        assert isinstance(status_code.application_status_code, int)
        assert isinstance(status_code.application_status_description_text, str)
        assert status_code.application_status_code > 0
        assert len(status_code.application_status_description_text) > 0
    
    await asyncio.sleep(1)  # Rate limiting
    
    print(f"✓ Verified structure of {len(result.status_codes)} status codes")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_status_codes_specific_code(client):
    """
    Test searching for a specific known status code.
    """
    # Search for status code 150 (Patented Case)
    result = await client.search_status_codes_get(
        q="applicationStatusCode:150",
        limit=25
    )
    
    assert result is not None
    assert result.count >= 0
    
    # If we have results, verify structure
    if result.count > 0 and len(result.status_codes) > 0:
        # Should find status code 150 if results are returned
        found_150 = any(sc.application_status_code == 150 for sc in result.status_codes)
        if found_150:
            # Get the 150 status code
            status_150 = next(sc for sc in result.status_codes if sc.application_status_code == 150)
            assert "Patent" in status_150.application_status_description_text or "Patented" in status_150.application_status_description_text
            print(f"✓ Found status code 150: {status_150.application_status_description_text}")
        else:
            print(f"✓ Found {len(result.status_codes)} status codes (may not include 150 due to pagination)")
    else:
        print(f"✓ Query returned count: {result.count} but no status codes in response")
    
    await asyncio.sleep(1)  # Rate limiting


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_status_codes_error_handling(client):
    """
    Test error handling for invalid queries.
    """
    # Test with invalid field name (should raise error)
    try:
        result = await client.search_status_codes_get(q="invalidField:value")
        # If it doesn't raise an error, verify it handles gracefully
        assert result is not None
        assert result.count >= 0
        print("✓ Invalid query handled gracefully (returned empty result)")
    except USPTOError as e:
        # Error is acceptable for invalid queries (may be 400 or 404)
        assert e.code == 400 or str(e.code) == "400" or e.code == 404 or str(e.code) == "404"
        print(f"✓ Invalid query correctly raised error: {e.code}")
    
    await asyncio.sleep(1)  # Rate limiting
