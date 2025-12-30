"""
Integration tests for patent wrapper endpoint.
Requires USPTO_API_KEY environment variable to be set.
"""
import pytest
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient, USPTOError


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_patent_wrapper_regular_application(client, known_application_numbers):
    """
    Test get_patent_wrapper with a regular application number.
    """
    serial_number = known_application_numbers["utility"]
    result = await client.get_patent_wrapper(serial_number)
    
    assert result is not None
    assert result.application_number == serial_number
    assert result.metadata is not None
    assert result.metadata.invention_title is not None
    assert result.metadata.filing_date is not None
    
    print(f"✓ Retrieved wrapper for application {serial_number}")
    print(f"  Title: {result.metadata.invention_title}")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_patent_wrapper_with_us_prefix(client, known_application_numbers):
    """
    Test that US prefix is properly stripped from application numbers.
    """
    serial_with_prefix = f"US{known_application_numbers['utility']}"
    result = await client.get_patent_wrapper(serial_with_prefix)
    
    assert result is not None
    assert result.application_number == known_application_numbers["utility"]
    
    await asyncio.sleep(1)  # Rate limiting
    
    print(f"✓ US prefix properly stripped: {serial_with_prefix} -> {result.application_number}")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_patent_wrapper_verify_fields(client, known_application_numbers):
    """
    Verify that all PatentFileWrapper fields are properly populated.
    """
    serial_number = known_application_numbers["utility"]
    result = await client.get_patent_wrapper(serial_number)
    
    assert result is not None
    assert result.application_number is not None
    assert result.metadata is not None
    
    # Verify metadata fields
    metadata = result.metadata
    assert metadata.filing_date is not None
    assert metadata.application_type_code is not None
    assert metadata.application_status_code is not None
    
    # Verify events exist (may be empty list)
    assert hasattr(result, 'events')
    assert isinstance(result.events, list)
    
    print(f"✓ Verified all wrapper fields for application {serial_number}")
    print(f"  Events: {len(result.events)}")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_patent_wrapper_pct_application(client, known_application_numbers):
    """
    Test get_patent_wrapper with PCT application number.
    """
    if "pct" not in known_application_numbers:
        pytest.skip("PCT application number not available in test data")
    
    pct_number = known_application_numbers["pct"]
    result = await client.get_patent_wrapper(pct_number)
    
    assert result is not None
    assert result.application_number is not None
    
    await asyncio.sleep(1)  # Rate limiting
    
    print(f"✓ Retrieved wrapper for PCT application {pct_number}")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_patent_wrapper_error_handling(client):
    """
    Test error handling for invalid application numbers.
    """
    invalid_serial = "99999999"  # Likely invalid
    
    with pytest.raises(USPTOError):
        await client.get_patent_wrapper(invalid_serial)
    
    print("✓ Error handling works correctly for invalid application numbers")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_patent_wrapper_multiple_applications(client, known_application_numbers):
    """
    Test getting wrappers for multiple different applications.
    """
    applications = [
        known_application_numbers["utility"],
        known_application_numbers["utility_2"]
    ]
    
    results = []
    for app_num in applications:
        result = await client.get_patent_wrapper(app_num)
        results.append(result)
        await asyncio.sleep(1)  # Rate limiting
    
    assert len(results) == 2
    assert results[0].application_number != results[1].application_number
    
    print(f"✓ Retrieved wrappers for {len(results)} different applications")
