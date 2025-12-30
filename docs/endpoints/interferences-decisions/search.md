# Search Interference Decisions

## Overview

Search for PTAB interference decision documents using either GET (query parameters) or POST (JSON payload) methods.

## Endpoint Details

- **Methods**: `GET`, `POST`
- **URL**: `/api/v1/patent/interferences/decisions/search`
- **Authentication**: Required (API Key)

## Library Methods

- `search_interference_decisions_get()` - GET method
- `search_interference_decisions()` - POST method

## Parameters

Similar to other search endpoints. See [Search Trial Proceedings](../trials-proceedings/search.md) for parameter details.

## Examples

### Basic Search

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def search_interferences():
    client = USPTOClient(api_key="your-api-key-here")
    
    results = await client.search_interference_decisions_get(q="interferenceNumber:106000")
    
    print(f"Found {results.total_num_found} decisions")
    
    await client.session.close()

asyncio.run(search_interferences())
```

## Related Endpoints

- [Search/Download](search-download.md) - Download search results
- [Get Decision](get-decision.md) - Get specific decision
- [Get Decisions by Interference](get-decisions-by-interference.md) - Get all decisions for an interference
