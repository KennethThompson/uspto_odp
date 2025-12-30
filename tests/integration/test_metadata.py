"""
Integration tests for get_app_metadata_from_patent_number.
Requires USPTO_API_KEY environment variable to be set.
"""
import pytest
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient, USPTOError


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_app_metadata_from_patent_number_with_prefix(client, known_patent_numbers):
    """
    Test get_app_metadata_from_patent_number with US prefix format.
    """
    patent_number = known_patent_numbers["with_prefix"]
    result = await client.get_app_metadata_from_patent_number(patent_number)
    
    assert result is not None
    assert "applicationNumberText" in result
    assert "applicationMetaData" in result
    
    print(f"✓ Retrieved metadata for patent {patent_number}")
    print(f"  Application Number: {result['applicationNumberText']}")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_app_metadata_from_patent_number_with_commas(client, known_patent_numbers):
    """
    Test get_app_metadata_from_patent_number with comma-separated format.
    """
    patent_number = known_patent_numbers["with_commas"]
    result = await client.get_app_metadata_from_patent_number(patent_number)
    
    assert result is not None
    assert "applicationNumberText" in result
    
    await asyncio.sleep(1)  # Rate limiting
    
    print(f"✓ Retrieved metadata for patent {patent_number} (with commas)")
    print(f"  Application Number: {result['applicationNumberText']}")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_app_metadata_from_patent_number_plain_format(client, known_patent_numbers):
    """
    Test get_app_metadata_from_patent_number with plain numeric format.
    """
    patent_number = known_patent_numbers["plain"]
    result = await client.get_app_metadata_from_patent_number(patent_number)
    
    assert result is not None
    assert "applicationNumberText" in result
    
    await asyncio.sleep(1)  # Rate limiting
    
    print(f"✓ Retrieved metadata for patent {patent_number} (plain format)")
    print(f"  Application Number: {result['applicationNumberText']}")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_app_metadata_from_patent_number_verify_consistency(client, known_patent_numbers):
    """
    Verify that different formats return the same result.
    """
    formats = [
        known_patent_numbers["with_prefix"],
        known_patent_numbers["with_commas"],
        known_patent_numbers["plain"]
    ]
    
    results = []
    for patent_num in formats:
        result = await client.get_app_metadata_from_patent_number(patent_num)
        results.append(result)
        await asyncio.sleep(1)  # Rate limiting
    
    # All formats should return the same application number
    app_numbers = [r["applicationNumberText"] for r in results if r]
    if len(app_numbers) > 1:
        assert len(set(app_numbers)) == 1, "All formats should return the same application number"
    
    print(f"✓ Verified consistency across {len(formats)} different formats")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_app_metadata_from_patent_number_verify_structure(client, known_patent_numbers):
    """
    Verify the structure of returned metadata.
    """
    patent_number = known_patent_numbers["with_prefix"]
    result = await client.get_app_metadata_from_patent_number(patent_number)
    
    assert result is not None
    assert "applicationNumberText" in result
    assert "applicationMetaData" in result
    
    metadata = result["applicationMetaData"]
    assert isinstance(metadata, dict)
    
    # Verify common metadata fields exist
    if "patentNumber" in metadata:
        assert metadata["patentNumber"] is not None
    
    print(f"✓ Verified metadata structure for patent {patent_number}")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_app_metadata_from_patent_number_not_found(client):
    """
    Test behavior when patent number is not found.
    Note: This may return empty results rather than None, depending on API behavior.
    """
    invalid_patent = "99999999"  # Likely invalid
    
    result = await client.get_app_metadata_from_patent_number(invalid_patent)
    
    # API may return None or empty result - both are acceptable
    # The implementation returns None if count is 0
    assert result is None or (isinstance(result, dict) and result.get('count', 0) == 0)
    
    print("✓ Correctly handled invalid patent number")
