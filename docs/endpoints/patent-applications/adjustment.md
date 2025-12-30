# Get Patent Term Adjustment

## Overview

Retrieve patent term adjustment information for a patent application. This shows adjustments to the patent term based on USPTO delays.

## Endpoint Details

- **Method**: `GET`
- **URL**: `/api/v1/patent/applications/{applicationNumberText}/adjustment`
- **Authentication**: Required (API Key)

## Library Method

- `get_adjustment(serial_number: str) -> AdjustmentResponse`

## Parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `applicationNumberText` | string | Yes | Application serial number (path parameter) | `14412875` |

## Response Structure

Returns an `AdjustmentResponse` object containing:
- `application_number` - Application number
- `adjustment` - PatentTermAdjustment object with adjustment details
- `request_identifier` - Unique request identifier

## Examples

### Basic Usage

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def get_adjustment():
    client = USPTOClient(api_key="your-api-key-here")
    
    adjustment = await client.get_adjustment("14412875")
    
    print(f"Application: {adjustment.application_number}")
    # Access adjustment details from adjustment.adjustment
    
    await client.session.close()

asyncio.run(get_adjustment())
```

## Related Endpoints

- [Get Patent Wrapper](get-patent-wrapper.md) - Get complete application information
- [Metadata](metadata.md) - Get application metadata
