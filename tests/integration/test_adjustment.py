"""
Integration tests for adjustment endpoint.
Requires USPTO_API_KEY environment variable to be set.
"""
import pytest
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOError


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_adjustment_basic(client, known_application_numbers):
    """
    Test get_adjustment with a valid application number.
    """
    serial_number = known_application_numbers["utility"]
    result = await client.get_adjustment(serial_number)
    
    assert result is not None
    assert hasattr(result, 'adjustments')
    assert isinstance(result.adjustments, list)
    assert result.count >= 0
    
    print(f"✓ Retrieved adjustment data for application {serial_number}")
    print(f"  Count: {result.count}")
    print(f"  Found {len(result.adjustments)} adjustment records")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_adjustment_verify_structure(client, known_application_numbers):
    """
    Verify AdjustmentResponse structure and fields.
    """
    serial_number = known_application_numbers["utility"]
    result = await client.get_adjustment(serial_number)
    
    assert result is not None
    assert hasattr(result, 'count')
    assert hasattr(result, 'adjustments')
    assert isinstance(result.count, int)
    assert isinstance(result.adjustments, list)
    
    # If there are adjustments, verify their structure
    if len(result.adjustments) > 0:
        app_adjustment = result.adjustments[0]
        assert hasattr(app_adjustment, 'application_number')
        assert hasattr(app_adjustment, 'patent_term_adjustment')
        
        # Verify application number matches
        assert app_adjustment.application_number == serial_number
        
        # If patent_term_adjustment exists, verify its structure
        if app_adjustment.patent_term_adjustment:
            pta = app_adjustment.patent_term_adjustment
            # Check that common fields exist (may be None)
            assert hasattr(pta, 'pta_days')
            assert hasattr(pta, 'total_adjustment_days')
            assert hasattr(pta, 'adjustment_reason_codes')
            assert hasattr(pta, 'adjustment_reason_descriptions')
    
    await asyncio.sleep(1)  # Rate limiting
    
    print(f"✓ Verified adjustment structure for application {serial_number}")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_adjustment_multiple_applications(client, known_application_numbers):
    """
    Test get_adjustment with multiple known application numbers.
    """
    applications = [
        known_application_numbers["utility"],
        known_application_numbers["utility_2"]
    ]
    
    results = []
    for app_num in applications:
        result = await client.get_adjustment(app_num)
        results.append(result)
        await asyncio.sleep(1)  # Rate limiting
    
    # Verify all requests succeeded
    for i, result in enumerate(results):
        assert result is not None
        assert result.count >= 0
        print(f"✓ Application {applications[i]}: count={result.count}, "
              f"adjustments={len(result.adjustments)}")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_adjustment_not_found(client):
    """
    Test behavior when application number is not found.
    """
    invalid_app = "99999999"  # Likely invalid
    
    with pytest.raises(USPTOError) as exc_info:
        await client.get_adjustment(invalid_app)
    
    # Error code may be string or int depending on API response
    assert exc_info.value.code == 404 or str(exc_info.value.code) == "404"
    assert "404" in str(exc_info.value) or "Not Found" in str(exc_info.value)
    print("✓ Correctly raised USPTOError for invalid application number")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_adjustment_verify_data_types(client, known_application_numbers):
    """
    Verify that returned data has correct types.
    """
    serial_number = known_application_numbers["utility"]
    result = await client.get_adjustment(serial_number)
    
    assert isinstance(result.count, int)
    assert isinstance(result.adjustments, list)
    
    if len(result.adjustments) > 0:
        app_adjustment = result.adjustments[0]
        assert isinstance(app_adjustment.application_number, str)
        
        if app_adjustment.patent_term_adjustment:
            pta = app_adjustment.patent_term_adjustment
            # Verify optional fields are correct types when present
            if pta.pta_days is not None:
                assert isinstance(pta.pta_days, int)
            if pta.total_adjustment_days is not None:
                assert isinstance(pta.total_adjustment_days, int)
            if pta.adjustment_reason_codes is not None:
                assert isinstance(pta.adjustment_reason_codes, list)
    
    await asyncio.sleep(1)  # Rate limiting
    
    print(f"✓ Verified data types for application {serial_number}")
