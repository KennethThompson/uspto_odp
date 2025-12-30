# Status Codes Endpoints

## Overview

The Status Codes endpoint provides access to patent application status codes and their descriptions. This is useful for understanding what different status codes mean and for querying status code information.

The endpoint is located at `/api/v1/patent/status-codes`.

## Available Endpoints

| Endpoint | Methods | Description | Documentation |
|----------|---------|-------------|---------------|
| `/api/v1/patent/status-codes` | GET, POST | Search for status codes using query parameters or JSON payload | [Search](search.md) |

## Quick Start

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def main():
    client = USPTOClient(api_key="your-api-key-here")
    
    # Search for status codes
    results = await client.search_status_codes_get(
        q="statusCode:101"
    )
    
    # Or use POST method
    payload = {
        "q": "statusCode:101",
        "limit": 25
    }
    results = await client.search_status_codes(payload)
    
    await client.session.close()

asyncio.run(main())
```

## Common Use Cases

### Understanding Status Codes
Use the [Search](search.md) endpoint to:
- Look up status code descriptions
- Search by status code number
- Search by status code description text
- Get comprehensive status code information

## Related Documentation

- [Quick Start Guide](../../quickstart.md) - Get started quickly
- [Examples](../../examples.md) - More code examples
- [API Reference](../../api/client.md) - Complete API documentation
