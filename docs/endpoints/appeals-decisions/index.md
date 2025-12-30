# PTAB Appeals - Decisions Endpoints

## Overview

The PTAB Appeals Decisions endpoints provide access to Patent Trial and Appeal Board (PTAB) appeal decision documents. These endpoints allow you to search for appeal decisions, download results, retrieve specific decisions, and get all decisions for an appeal.

All endpoints in this category begin with `/api/v1/patent/appeals/decisions`.

## Available Endpoints

| Endpoint | Methods | Description | Documentation |
|----------|---------|-------------|---------------|
| `/search` | GET, POST | Search for appeal decisions using query parameters or JSON payload | [Search](search.md) |
| `/search/download` | GET, POST | Download search results as a file | [Search/Download](search-download.md) |
| `/{documentIdentifier}` | GET | Get a specific appeal decision document | [Get Decision](get-decision.md) |
| `/{appealNumber}/decisions` | GET | Get all decisions for a specific appeal | [Get Decisions by Appeal](get-decisions-by-appeal.md) |

## Quick Start

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def main():
    client = USPTOClient(api_key="your-api-key-here")
    
    # Search for appeal decisions
    results = await client.search_appeal_decisions_get(
        q="appealNumber:2020-00001"
    )
    
    # Get specific decision
    decision = await client.get_appeal_decision("document-id")
    
    # Get all decisions for an appeal
    decisions = await client.get_appeal_decisions_by_appeal("2020-00001")
    
    await client.session.close()

asyncio.run(main())
```

## Common Use Cases

### Searching Appeal Decisions
Use the [Search](search.md) endpoint to find decisions by:
- Appeal number
- Document identifier
- Decision type
- Decision date
- Application number
- And other criteria

### Downloading Results
Use the [Search/Download](search-download.md) endpoint to:
- Download large result sets as files
- Export search results for analysis

### Retrieving Decisions
- [Get Decision](get-decision.md) - Get a specific decision document
- [Get Decisions by Appeal](get-decisions-by-appeal.md) - Get all decisions for an appeal

## Related Documentation

- [Quick Start Guide](../../quickstart.md) - Get started quickly
- [Examples](../../examples.md) - More code examples
- [API Reference](../../api/client.md) - Complete API documentation
