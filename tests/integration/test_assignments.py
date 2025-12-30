"""
Integration tests for assignments endpoint.
Requires USPTO_API_KEY environment variable to be set.
"""
import pytest
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient, USPTOError


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_patent_assignments_basic(client, known_application_numbers):
    """
    Test get_patent_assignments with a valid application number.
    """
    serial_number = known_application_numbers["utility"]
    result = await client.get_patent_assignments(serial_number)
    
    assert result is not None
    assert hasattr(result, 'assignments')
    assert isinstance(result.assignments, list)
    
    print(f"✓ Retrieved assignment data for application {serial_number}")
    print(f"  Found {len(result.assignments)} assignments")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_patent_assignments_verify_structure(client, known_application_numbers):
    """
    Verify AssignmentCollection structure and fields.
    """
    serial_number = known_application_numbers["utility"]
    result = await client.get_patent_assignments(serial_number)
    
    assert result is not None
    
    # If there are assignments, verify their structure
    if len(result.assignments) > 0:
        app_assignment = result.assignments[0]
        # Verify ApplicationAssignment has expected attributes
        assert hasattr(app_assignment, 'application_number')
        assert hasattr(app_assignment, 'assignments')
        # If there are individual assignments, verify their structure
        if len(app_assignment.assignments) > 0:
            assignment = app_assignment.assignments[0]
            assert hasattr(assignment, 'recorded_date')
            assert hasattr(assignment, 'assignees')
    
    await asyncio.sleep(1)  # Rate limiting
    
    print(f"✓ Verified assignment structure for application {serial_number}")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_patent_assignments_error_handling(client):
    """
    Test error handling for invalid application numbers.
    """
    invalid_serial = "99999999"  # Likely invalid
    
    with pytest.raises(USPTOError):
        await client.get_patent_assignments(invalid_serial)
    
    print("✓ Error handling works correctly for invalid serial numbers")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_patent_assignments_multiple_applications(client, known_application_numbers):
    """
    Test getting assignments for multiple applications.
    """
    applications = [
        known_application_numbers["utility"],
        known_application_numbers["utility_2"]
    ]
    
    for app_num in applications:
        result = await client.get_patent_assignments(app_num)
        assert result is not None
        await asyncio.sleep(1)  # Rate limiting
    
    print(f"✓ Retrieved assignment data for {len(applications)} applications")
