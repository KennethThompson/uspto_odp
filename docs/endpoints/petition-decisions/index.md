# Petition Decisions Endpoints

## Overview

The Petition Decisions endpoints provide access to USPTO petition decision records. These endpoints allow you to search for petition decisions, download results, and retrieve specific decision records.

All endpoints in this category begin with `/api/v1/petition/decisions`.

## Available Endpoints

| Endpoint | Methods | Description | Documentation |
|----------|---------|-------------|---------------|
| `/search` | GET, POST | Search for petition decisions using query parameters or JSON payload | [Search](search.md) |
| `/search/download` | GET, POST | Download search results as a file | [Search/Download](search-download.md) |
| `/{petitionDecisionRecordIdentifier}` | GET | Get a specific petition decision record | [Get Decision](get-decision.md) |

## Quick Start

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def main():
    client = USPTOClient(api_key="your-api-key-here")
    
    # Search for petition decisions
    results = await client.search_petition_decisions_get(
        q="patentNumber:12345678"
    )
    
    # Get specific decision
    decision = await client.get_petition_decision("decision-id")
    
    await client.session.close()

asyncio.run(main())
```

## Common Use Cases

### Searching Petition Decisions
Use the [Search](search.md) endpoint to find decisions by:
- Patent number
- Application number
- Decision type
- Decision date
- Technology center
- And other criteria

### Downloading Results
Use the [Search/Download](search-download.md) endpoint to:
- Download large result sets as files
- Export search results for analysis

### Retrieving Specific Decisions
Use the [Get Decision](get-decision.md) endpoint to:
- Get complete decision record details
- Access decision documents and metadata

## Related Documentation

- [Quick Start Guide](../../quickstart.md) - Get started quickly
- [Examples](../../examples.md) - More code examples
- [API Reference](../../api/client.md) - Complete API documentation
