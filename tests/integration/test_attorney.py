"""
Integration tests for attorney endpoint.
Requires USPTO_API_KEY environment variable to be set.
"""
import pytest
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOError


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_attorney_basic(client, known_application_numbers):
    """
    Test get_attorney with a valid application number.
    """
    serial_number = known_application_numbers["utility"]
    result = await client.get_attorney(serial_number)
    
    assert result is not None
    assert hasattr(result, 'attorneys')
    assert isinstance(result.attorneys, list)
    assert result.count >= 0
    
    print(f"✓ Retrieved attorney data for application {serial_number}")
    print(f"  Count: {result.count}")
    print(f"  Found {len(result.attorneys)} attorney records")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_attorney_verify_structure(client, known_application_numbers):
    """
    Verify AttorneyResponse structure and fields.
    """
    serial_number = known_application_numbers["utility"]
    result = await client.get_attorney(serial_number)
    
    assert result is not None
    assert hasattr(result, 'count')
    assert hasattr(result, 'attorneys')
    assert isinstance(result.count, int)
    assert isinstance(result.attorneys, list)
    
    # If there are attorneys, verify their structure
    if len(result.attorneys) > 0:
        app_attorney = result.attorneys[0]
        assert hasattr(app_attorney, 'application_number')
        assert hasattr(app_attorney, 'record_attorney')
        
        # Verify application number matches
        assert app_attorney.application_number == serial_number
        
        # If record_attorney exists, verify its structure
        if app_attorney.record_attorney:
            assert hasattr(app_attorney.record_attorney, 'attorney_name')
            # Other fields may be None, so just check they exist
            assert hasattr(app_attorney.record_attorney, 'registration_number')
            assert hasattr(app_attorney.record_attorney, 'address')
    
    await asyncio.sleep(1)  # Rate limiting
    
    print(f"✓ Verified attorney structure for application {serial_number}")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_attorney_multiple_applications(client, known_application_numbers):
    """
    Test get_attorney with multiple known application numbers.
    """
    applications = [
        known_application_numbers["utility"],
        known_application_numbers["utility_2"]
    ]
    
    results = []
    for app_num in applications:
        result = await client.get_attorney(app_num)
        results.append(result)
        await asyncio.sleep(1)  # Rate limiting
    
    # Verify all requests succeeded
    for i, result in enumerate(results):
        assert result is not None
        assert result.count >= 0
        print(f"✓ Application {applications[i]}: count={result.count}, "
              f"attorneys={len(result.attorneys)}")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_attorney_not_found(client):
    """
    Test behavior when application number is not found.
    """
    invalid_app = "99999999"  # Likely invalid
    
    with pytest.raises(USPTOError) as exc_info:
        await client.get_attorney(invalid_app)
    
    # Error code may be string or int depending on API response
    assert exc_info.value.code == 404 or str(exc_info.value.code) == "404"
    assert "404" in str(exc_info.value) or "Not Found" in str(exc_info.value)
    print("✓ Correctly raised USPTOError for invalid application number")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_attorney_verify_data_types(client, known_application_numbers):
    """
    Verify that returned data has correct types.
    """
    serial_number = known_application_numbers["utility"]
    result = await client.get_attorney(serial_number)
    
    assert isinstance(result.count, int)
    assert isinstance(result.attorneys, list)
    
    if len(result.attorneys) > 0:
        app_attorney = result.attorneys[0]
        assert isinstance(app_attorney.application_number, str)
        
        if app_attorney.record_attorney:
            # Verify optional fields are correct types when present
            if app_attorney.record_attorney.attorney_name is not None:
                assert isinstance(app_attorney.record_attorney.attorney_name, str)
            if app_attorney.record_attorney.registration_number is not None:
                assert isinstance(app_attorney.record_attorney.registration_number, str)
            if app_attorney.record_attorney.address is not None:
                assert hasattr(app_attorney.record_attorney.address, 'city_name')
    
    await asyncio.sleep(1)  # Rate limiting
    
    print(f"✓ Verified data types for application {serial_number}")
