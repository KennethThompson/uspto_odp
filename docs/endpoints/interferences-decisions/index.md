# PTAB Interferences - Decisions Endpoints

## Overview

The PTAB Interferences Decisions endpoints provide access to Patent Trial and Appeal Board (PTAB) interference decision documents. These endpoints allow you to search for interference decisions, download results, retrieve specific decisions, and get all decisions for an interference.

All endpoints in this category begin with `/api/v1/patent/interferences/decisions`.

## Available Endpoints

| Endpoint | Methods | Description | Documentation |
|----------|---------|-------------|---------------|
| `/search` | GET, POST | Search for interference decisions using query parameters or JSON payload | [Search](search.md) |
| `/search/download` | GET, POST | Download search results as a file | [Search/Download](search-download.md) |
| `/{interferenceNumber}/decisions` | GET | Get all decisions for a specific interference | [Get Decisions by Interference](get-decisions-by-interference.md) |
| `/decisions/{documentIdentifier}` | GET | Get a specific interference decision document | [Get Decision](get-decision.md) |

## Quick Start

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def main():
    client = USPTOClient(api_key="your-api-key-here")
    
    # Search for interference decisions
    results = await client.search_interference_decisions_get(
        q="interferenceNumber:106000"
    )
    
    # Get specific decision
    decision = await client.get_interference_decision("document-id")
    
    # Get all decisions for an interference
    decisions = await client.get_interference_decisions_by_interference("106000")
    
    await client.session.close()

asyncio.run(main())
```

## Common Use Cases

### Searching Interference Decisions
Use the [Search](search.md) endpoint to find decisions by:
- Interference number
- Document identifier
- Decision type
- Decision date
- Patent number
- And other criteria

### Downloading Results
Use the [Search/Download](search-download.md) endpoint to:
- Download large result sets as files
- Export search results for analysis

### Retrieving Decisions
- [Get Decision](get-decision.md) - Get a specific decision document
- [Get Decisions by Interference](get-decisions-by-interference.md) - Get all decisions for an interference

## Related Documentation

- [Quick Start Guide](../../quickstart.md) - Get started quickly
- [Examples](../../examples.md) - More code examples
- [API Reference](../../api/client.md) - Complete API documentation
