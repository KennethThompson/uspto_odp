# PTAB Trials - Decisions Endpoints

## Overview

The PTAB Trials Decisions endpoints provide access to Patent Trial and Appeal Board (PTAB) trial decision documents. These endpoints allow you to search for decisions, download results, retrieve specific decisions, and get all decisions for a trial.

All endpoints in this category begin with `/api/v1/patent/trials/decisions`.

## Available Endpoints

| Endpoint | Methods | Description | Documentation |
|----------|---------|-------------|---------------|
| `/search` | GET, POST | Search for trial decisions using query parameters or JSON payload | [Search](search.md) |
| `/search/download` | GET, POST | Download search results as a file | [Search/Download](search-download.md) |
| `/{documentIdentifier}` | GET | Get a specific trial decision document | [Get Decision](get-decision.md) |
| `/{trialNumber}/decisions` | GET | Get all decisions for a specific trial | [Get Decisions by Trial](get-decisions-by-trial.md) |

## Quick Start

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def main():
    client = USPTOClient(api_key="your-api-key-here")
    
    # Search for trial decisions
    results = await client.search_trial_decisions_get(
        q="trialNumber:IPR2020-00001"
    )
    
    # Get specific decision
    decision = await client.get_trial_decision("document-id")
    
    # Get all decisions for a trial
    decisions = await client.get_trial_decisions_by_trial("IPR2020-00001")
    
    await client.session.close()

asyncio.run(main())
```

## Common Use Cases

### Searching Trial Decisions
Use the [Search](search.md) endpoint to find decisions by:
- Trial number
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
- [Get Decisions by Trial](get-decisions-by-trial.md) - Get all decisions for a trial

## Related Documentation

- [PTAB Trials - Proceedings](../trials-proceedings/index.md) - Related proceedings endpoints
- [PTAB Trials - Documents](../trials-documents/index.md) - Related documents endpoints
- [Quick Start Guide](../../quickstart.md) - Get started quickly
- [Examples](../../examples.md) - More code examples
- [API Reference](../../api/client.md) - Complete API documentation
