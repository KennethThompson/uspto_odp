# Search Trial Decisions

## Overview

Search for PTAB trial decision documents using either GET (query parameters) or POST (JSON payload) methods.

## Endpoint Details

- **Methods**: `GET`, `POST`
- **URL**: `/api/v1/patent/trials/decisions/search`
- **Authentication**: Required (API Key)

## Library Methods

- `search_trial_decisions_get()` - GET method
- `search_trial_decisions()` - POST method

## Parameters

Similar to other search endpoints. See [Search Trial Proceedings](../trials-proceedings/search.md) for parameter details.

## Examples

### Basic Search

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def search_decisions():
    client = USPTOClient(api_key="your-api-key-here")
    
    results = await client.search_trial_decisions_get(q="trialNumber:IPR2020-00001")
    
    print(f"Found {results.total_num_found} decisions")
    
    await client.session.close()

asyncio.run(search_decisions())
```

## Related Endpoints

- [Search/Download](search-download.md) - Download search results
- [Get Decision](get-decision.md) - Get specific decision
- [Get Decisions by Trial](get-decisions-by-trial.md) - Get all decisions for a trial
