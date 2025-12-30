# Search Appeal Decisions

## Overview

Search for PTAB appeal decision documents using either GET (query parameters) or POST (JSON payload) methods.

## Endpoint Details

- **Methods**: `GET`, `POST`
- **URL**: `/api/v1/patent/appeals/decisions/search`
- **Authentication**: Required (API Key)

## Library Methods

- `search_appeal_decisions_get()` - GET method
- `search_appeal_decisions()` - POST method

## Parameters

Similar to other search endpoints. See [Search Trial Proceedings](../trials-proceedings/search.md) for parameter details.

## Examples

### Basic Search

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def search_appeals():
    client = USPTOClient(api_key="your-api-key-here")
    
    results = await client.search_appeal_decisions_get(q="appealNumber:2020-00001")
    
    print(f"Found {results.total_num_found} decisions")
    
    await client.session.close()

asyncio.run(search_appeals())
```

## Related Endpoints

- [Search/Download](search-download.md) - Download search results
- [Get Decision](get-decision.md) - Get specific decision
- [Get Decisions by Appeal](get-decisions-by-appeal.md) - Get all decisions for an appeal
