"""
Integration tests for transactions endpoint.
Requires USPTO_API_KEY environment variable to be set.
"""
import pytest
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient, USPTOError


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_patent_transactions_basic(client, known_application_numbers):
    """
    Test get_patent_transactions with a valid application number.
    """
    serial_number = known_application_numbers["utility"]
    result = await client.get_patent_transactions(serial_number)
    
    assert result is not None
    assert hasattr(result, 'transactions')
    assert isinstance(result.transactions, list)
    
    print(f"✓ Retrieved transaction data for application {serial_number}")
    print(f"  Found {len(result.transactions)} transactions")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_patent_transactions_verify_structure(client, known_application_numbers):
    """
    Verify TransactionCollection structure and fields.
    """
    serial_number = known_application_numbers["utility"]
    result = await client.get_patent_transactions(serial_number)
    
    assert result is not None
    
    # If there are transactions, verify their structure
    if len(result.transactions) > 0:
        app_transaction = result.transactions[0]
        # Verify ApplicationTransactions has expected attributes
        assert hasattr(app_transaction, 'application_number')
        assert hasattr(app_transaction, 'events')
        # If there are events, verify their structure
        if len(app_transaction.events) > 0:
            event = app_transaction.events[0]
            assert hasattr(event, 'event_date')
            assert hasattr(event, 'event_code')
    
    await asyncio.sleep(1)  # Rate limiting
    
    print(f"✓ Verified transaction structure for application {serial_number}")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_patent_transactions_error_handling(client):
    """
    Test error handling for invalid application numbers.
    """
    invalid_serial = "99999999"  # Likely invalid
    
    with pytest.raises(USPTOError):
        await client.get_patent_transactions(invalid_serial)
    
    print("✓ Error handling works correctly for invalid serial numbers")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_patent_transactions_multiple_applications(client, known_application_numbers):
    """
    Test getting transactions for multiple applications.
    """
    applications = [
        known_application_numbers["utility"],
        known_application_numbers["utility_2"]
    ]
    
    for app_num in applications:
        result = await client.get_patent_transactions(app_num)
        assert result is not None
        await asyncio.sleep(1)  # Rate limiting
    
    print(f"✓ Retrieved transaction data for {len(applications)} applications")
