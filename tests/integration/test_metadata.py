"""
Integration tests for get_app_metadata and get_app_metadata_from_patent_number.
Requires USPTO_API_KEY environment variable to be set.
"""
import pytest
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOError
from uspto_odp.models.patent_metadata import ApplicationMetadataResponse


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_app_metadata_direct(client, known_application_numbers):
    """
    Test get_app_metadata method that calls the /meta-data endpoint directly.
    """
    application_number = known_application_numbers["utility"]
    result = await client.get_app_metadata(application_number)
    
    assert result is not None
    assert isinstance(result, ApplicationMetadataResponse)
    assert result.application_number == application_number
    assert result.metadata is not None
    assert result.metadata.invention_title is not None
    
    print(f"✓ Retrieved metadata directly for application {application_number}")
    print(f"  Title: {result.metadata.invention_title}")
    print(f"  Status Code: {result.metadata.application_status_code}")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_app_metadata_not_found(client):
    """
    Test get_app_metadata with non-existent application number.
    """
    invalid_app = "99999999"  # Likely invalid
    
    with pytest.raises(USPTOError) as exc_info:
        await client.get_app_metadata(invalid_app)
    
    assert exc_info.value.code == 404 or str(exc_info.value.code) == "404"
    print("✓ Correctly raised USPTOError for invalid application number")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_app_metadata_from_patent_number_with_prefix(client, known_patent_numbers):
    """
    Test get_app_metadata_from_patent_number with US prefix format.
    """
    patent_number = known_patent_numbers["with_prefix"]
    result = await client.get_app_metadata_from_patent_number(patent_number)
    
    assert result is not None
    assert isinstance(result, ApplicationMetadataResponse)
    assert result.application_number is not None
    assert result.metadata is not None
    
    print(f"✓ Retrieved metadata for patent {patent_number}")
    print(f"  Application Number: {result.application_number}")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_app_metadata_from_patent_number_with_commas(client, known_patent_numbers):
    """
    Test get_app_metadata_from_patent_number with comma-separated format.
    """
    patent_number = known_patent_numbers["with_commas"]
    result = await client.get_app_metadata_from_patent_number(patent_number)
    
    assert result is not None
    assert isinstance(result, ApplicationMetadataResponse)
    assert result.application_number is not None
    
    await asyncio.sleep(1)  # Rate limiting
    
    print(f"✓ Retrieved metadata for patent {patent_number} (with commas)")
    print(f"  Application Number: {result.application_number}")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_app_metadata_from_patent_number_plain_format(client, known_patent_numbers):
    """
    Test get_app_metadata_from_patent_number with plain numeric format.
    """
    patent_number = known_patent_numbers["plain"]
    result = await client.get_app_metadata_from_patent_number(patent_number)
    
    assert result is not None
    assert isinstance(result, ApplicationMetadataResponse)
    assert result.application_number is not None
    
    await asyncio.sleep(1)  # Rate limiting
    
    print(f"✓ Retrieved metadata for patent {patent_number} (plain format)")
    print(f"  Application Number: {result.application_number}")


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
    app_numbers = [r.application_number for r in results if r]
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
    assert isinstance(result, ApplicationMetadataResponse)
    assert result.application_number is not None
    assert result.metadata is not None
    
    # Verify common metadata fields exist
    assert result.metadata.application_status_code is not None
    assert result.metadata.invention_title is not None
    
    print(f"✓ Verified metadata structure for patent {patent_number}")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_app_metadata_consistency(client, known_patent_numbers, known_application_numbers):
    """
    Verify that get_app_metadata and get_app_metadata_from_patent_number return consistent data
    when given the same application.
    """
    # First get application number from patent number
    patent_number = known_patent_numbers["plain"]
    result_from_patent = await client.get_app_metadata_from_patent_number(patent_number)
    
    await asyncio.sleep(1)  # Rate limiting
    
    if result_from_patent:
        app_number = result_from_patent.application_number
        
        # Now get metadata directly using application number
        result_direct = await client.get_app_metadata(app_number)
        
        # Both should return the same application number
        assert result_direct.application_number == result_from_patent.application_number
        assert result_direct.metadata.invention_title == result_from_patent.metadata.invention_title
        
        print("✓ Verified consistency between direct and patent-number methods")
        print(f"  Application: {app_number}")
        print(f"  Title: {result_direct.metadata.invention_title}")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_app_metadata_from_patent_number_not_found(client):
    """
    Test behavior when patent number is not found.
    The API returns a 404 error for invalid patent numbers.
    """
    invalid_patent = "99999999"  # Likely invalid
    
    # The API returns 404 for invalid patent numbers, which raises USPTOError
    with pytest.raises(USPTOError) as exc_info:
        await client.get_app_metadata_from_patent_number(invalid_patent)
    
    # Error code may be string or int depending on API response
    assert exc_info.value.code == 404 or str(exc_info.value.code) == "404"
    assert "404" in str(exc_info.value) or "Not Found" in str(exc_info.value)
    print("✓ Correctly raised USPTOError for invalid patent number")
