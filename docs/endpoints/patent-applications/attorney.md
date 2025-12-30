# Get Attorney Information

## Overview

Retrieve attorney/agent information for a patent application.

## Endpoint Details

- **Method**: `GET`
- **URL**: `/api/v1/patent/applications/{applicationNumberText}/attorney`
- **Authentication**: Required (API Key)

## Library Method

- `get_attorney(serial_number: str) -> AttorneyResponse`

## Parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `applicationNumberText` | string | Yes | Application serial number (path parameter) | `14412875` |

## Response Structure

Returns an `AttorneyResponse` object containing:
- `application_number` - Application number
- `attorney` - Attorney/agent information
- `request_identifier` - Unique request identifier

## Examples

### Basic Usage

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def get_attorney():
    client = USPTOClient(api_key="your-api-key-here")
    
    attorney = await client.get_attorney("14412875")
    
    print(f"Application: {attorney.application_number}")
    # Access attorney details from attorney.attorney
    
    await client.session.close()

asyncio.run(get_attorney())
```

## Related Endpoints

- [Get Patent Wrapper](get-patent-wrapper.md) - Get complete application information
- [Metadata](metadata.md) - Get application metadata
