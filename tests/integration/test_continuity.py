"""
Integration tests for continuity endpoint.
Requires USPTO_API_KEY environment variable to be set.
"""
import pytest
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient, USPTOError


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_continuity_basic(client, known_application_numbers):
    """
    Test get_continuity with a valid application number.
    """
    serial_number = known_application_numbers["utility"]
    result = await client.get_continuity(serial_number)
    
    assert result is not None
    assert hasattr(result, 'continuities')
    assert isinstance(result.continuities, list)
    
    print(f"✓ Retrieved continuity data for application {serial_number}")
    print(f"  Found {len(result.continuities)} continuity relationships")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_continuity_verify_structure(client, known_application_numbers):
    """
    Verify ContinuityCollection structure and fields.
    """
    serial_number = known_application_numbers["utility"]
    result = await client.get_continuity(serial_number)
    
    assert result is not None
    
    # If there are continuities, verify their structure
    if len(result.continuities) > 0:
        continuity = result.continuities[0]
        # Verify continuity has expected attributes
        assert hasattr(continuity, 'application_number') or hasattr(continuity, 'child_application_number')
    
    await asyncio.sleep(1)  # Rate limiting
    
    print(f"✓ Verified continuity structure for application {serial_number}")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_continuity_error_handling(client):
    """
    Test error handling for invalid application numbers.
    """
    invalid_serial = "99999999"  # Likely invalid
    
    with pytest.raises(USPTOError):
        await client.get_continuity(invalid_serial)
    
    print("✓ Error handling works correctly for invalid serial numbers")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_continuity_multiple_applications(client, known_application_numbers):
    """
    Test getting continuity for multiple applications.
    """
    applications = [
        known_application_numbers["utility"],
        known_application_numbers["utility_2"]
    ]
    
    for app_num in applications:
        result = await client.get_continuity(app_num)
        assert result is not None
        await asyncio.sleep(1)  # Rate limiting
    
    print(f"✓ Retrieved continuity data for {len(applications)} applications")
