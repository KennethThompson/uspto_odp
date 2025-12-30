# PTAB Trials - Proceedings Endpoints

## Overview

The PTAB Trials Proceedings endpoints provide access to Patent Trial and Appeal Board (PTAB) trial proceeding information. These endpoints allow you to search for trial proceedings, download results, and retrieve specific proceeding details.

All endpoints in this category begin with `/api/v1/patent/trials/proceedings`.

## Available Endpoints

| Endpoint | Methods | Description | Documentation |
|----------|---------|-------------|---------------|
| `/search` | GET, POST | Search for trial proceedings using query parameters or JSON payload | [Search](search.md) |
| `/search/download` | GET, POST | Download search results as a file | [Search/Download](search-download.md) |
| `/{trialNumber}` | GET | Get a specific trial proceeding | [Get Proceeding](get-proceeding.md) |

## Quick Start

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def main():
    client = USPTOClient(api_key="your-api-key-here")
    
    # Search for trial proceedings
    results = await client.search_trial_proceedings_get(
        q="trialNumber:IPR2020-00001"
    )
    
    # Get specific proceeding
    proceeding = await client.get_trial_proceeding("IPR2020-00001")
    
    await client.session.close()

asyncio.run(main())
```

## Common Use Cases

### Searching Trial Proceedings
Use the [Search](search.md) endpoint to find proceedings by:
- Trial number
- Patent number
- Trial type (IPR, PGR, CBM)
- Filing date
- Status
- And other criteria

### Downloading Results
Use the [Search/Download](search-download.md) endpoint to:
- Download large result sets as files
- Export search results for analysis

### Retrieving Specific Proceedings
Use the [Get Proceeding](get-proceeding.md) endpoint to:
- Get complete proceeding details
- Access proceeding metadata and status

## Related Documentation

- [PTAB Trials - Decisions](../trials-decisions/index.md) - Related decisions endpoints
- [PTAB Trials - Documents](../trials-documents/index.md) - Related documents endpoints
- [Quick Start Guide](../../quickstart.md) - Get started quickly
- [Examples](../../examples.md) - More code examples
- [API Reference](../../api/client.md) - Complete API documentation
