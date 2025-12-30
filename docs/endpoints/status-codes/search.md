# Search Status Codes

## Overview

Search for patent application status codes and their descriptions. This endpoint helps you understand what different status codes mean.

## Endpoint Details

- **Methods**: `GET`, `POST`
- **URL**: `/api/v1/patent/status-codes`
- **Authentication**: Required (API Key)

## Library Methods

- `search_status_codes_get()` - GET method with query parameters
- `search_status_codes()` - POST method with JSON payload

## Parameters

### GET Method Parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `q` | string | No | Search query string | `statusCode:101` or `applicationStatusDescriptionText:Preexam` |
| `offset` | integer | No | Position in dataset to start from (default: 0) | `0` |
| `limit` | integer | No | Number of results to return (default: 25) | `50` |

### POST Method Payload

```json
{
  "q": "statusCode:101",
  "offset": 0,
  "limit": 25
}
```

## Response Structure

Returns a `StatusCodeCollection` object containing:
- `status_codes` - List of StatusCode objects
- Each status code includes:
  - `status_code` - Status code number
  - `description` - Status code description
  - Additional metadata

## Examples

### Search by Status Code Number (GET)

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def search_by_code():
    client = USPTOClient(api_key="your-api-key-here")
    
    results = await client.search_status_codes_get(q="statusCode:101")
    
    for code in results.status_codes:
        print(f"Code {code.status_code}: {code.description}")
    
    await client.session.close()

asyncio.run(search_by_code())
```

### Search by Description (GET)

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def search_by_description():
    client = USPTOClient(api_key="your-api-key-here")
    
    results = await client.search_status_codes_get(
        q="applicationStatusDescriptionText:Preexam",
        limit=50
    )
    
    print(f"Found {len(results.status_codes)} status codes")
    for code in results.status_codes:
        print(f"{code.status_code}: {code.description}")
    
    await client.session.close()

asyncio.run(search_by_description())
```

### Search with POST Method

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def search_post():
    client = USPTOClient(api_key="your-api-key-here")
    
    payload = {
        "q": "statusCode:101",
        "limit": 25
    }
    
    results = await client.search_status_codes(payload)
    
    for code in results.status_codes:
        print(f"{code.status_code}: {code.description}")
    
    await client.session.close()

asyncio.run(search_post())
```

## Related Documentation

- [Status Codes Overview](index.md) - Status codes endpoints overview
- [Quick Start Guide](../../quickstart.md) - Getting started guide
