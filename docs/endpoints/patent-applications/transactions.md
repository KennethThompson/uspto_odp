# Get Patent Transactions

## Overview

Retrieve transaction history for a patent application. This shows all transactions and events related to the application.

## Endpoint Details

- **Method**: `GET`
- **URL**: `/api/v1/patent/applications/{applicationNumberText}/transactions`
- **Authentication**: Required (API Key)

## Library Method

- `get_patent_transactions(serial_number: str) -> TransactionCollection`

## Parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `applicationNumberText` | string | Yes | Application serial number (path parameter) | `14412875` |

## Response Structure

Returns a `TransactionCollection` object containing:
- `transactions` - List of transaction records
- Each transaction includes date, type, description, and other details

## Examples

### Basic Usage

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def get_transactions():
    client = USPTOClient(api_key="your-api-key-here")
    
    transactions = await client.get_patent_transactions("14412875")
    
    print(f"Total transactions: {len(transactions.transactions)}")
    for transaction in transactions.transactions[:10]:  # Show first 10
        print(f"Date: {transaction.date}")
        print(f"Type: {transaction.type}")
        print(f"Description: {transaction.description}")
        print("---")
    
    await client.session.close()

asyncio.run(get_transactions())
```

## Related Endpoints

- [Get Patent Wrapper](get-patent-wrapper.md) - Get complete application information
- [Assignment](assignment.md) - Get assignment records
