"""
Integration tests for foreign priority endpoint.
Requires USPTO_API_KEY environment variable to be set.
"""
import pytest
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient, USPTOError


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_foreign_priority_basic(client, known_application_numbers):
    """
    Test get_foreign_priority with a valid application number.
    """
    serial_number = known_application_numbers["utility"]
    result = await client.get_foreign_priority(serial_number)
    
    assert result is not None
    assert hasattr(result, 'priorities')
    assert isinstance(result.priorities, list)
    
    print(f"✓ Retrieved foreign priority data for application {serial_number}")
    print(f"  Found {len(result.priorities)} foreign priority entries")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_foreign_priority_verify_structure(client, known_application_numbers):
    """
    Verify ForeignPriorityCollection structure and fields.
    """
    serial_number = known_application_numbers["utility"]
    result = await client.get_foreign_priority(serial_number)
    
    assert result is not None
    
    # If there are foreign priorities, verify their structure
    if len(result.priorities) > 0:
        priority_data = result.priorities[0]
        # Verify ForeignPriorityData has expected attributes
        assert hasattr(priority_data, 'application_number')
        assert hasattr(priority_data, 'foreign_priorities')
        # If there are individual foreign priorities, verify their structure
        if len(priority_data.foreign_priorities) > 0:
            priority = priority_data.foreign_priorities[0]
            assert hasattr(priority, 'office_name')
            assert hasattr(priority, 'filing_date')
            assert hasattr(priority, 'application_number')
    
    await asyncio.sleep(1)  # Rate limiting
    
    print(f"✓ Verified foreign priority structure for application {serial_number}")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_foreign_priority_error_handling(client):
    """
    Test error handling for invalid application numbers.
    """
    invalid_serial = "99999999"  # Likely invalid
    
    with pytest.raises(USPTOError):
        await client.get_foreign_priority(invalid_serial)
    
    print("✓ Error handling works correctly for invalid serial numbers")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_foreign_priority_multiple_applications(client, known_application_numbers):
    """
    Test getting foreign priority for multiple applications.
    """
    applications = [
        known_application_numbers["utility"],
        known_application_numbers["utility_2"]
    ]
    
    for app_num in applications:
        result = await client.get_foreign_priority(app_num)
        assert result is not None
        await asyncio.sleep(1)  # Rate limiting
    
    print(f"✓ Retrieved foreign priority data for {len(applications)} applications")
