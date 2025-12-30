# Search/Download Interference Decisions

## Overview

Download interference decision search results as a file. Supports JSON and CSV formats.

## Endpoint Details

- **Methods**: `GET`, `POST`
- **URL**: `/api/v1/patent/interferences/decisions/search/download`
- **Authentication**: Required (API Key)

## Library Methods

- `search_interference_decisions_download_get()` - GET method
- `search_interference_decisions_download()` - POST method

## Parameters

Same as [Search](search.md) endpoint, plus `format` parameter (`json` or `csv`).

## Examples

### Download as JSON

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def download_json():
    client = USPTOClient(api_key="your-api-key-here")
    
    results = await client.search_interference_decisions_download_get(
        q="interferenceNumber:106000",
        format="json"
    )
    
    print(f"Downloaded {len(results.decisions)} decisions")
    
    await client.session.close()

asyncio.run(download_json())
```

## Related Endpoints

- [Search](search.md) - Search without download
- [Get Decision](get-decision.md) - Get specific decision
