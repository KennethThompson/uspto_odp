# Search/Download Petition Decisions

## Overview

Download petition decision search results as a file. This endpoint is optimized for bulk downloads and supports both JSON and CSV formats.

## Endpoint Details

- **Methods**: `GET`, `POST`
- **URL**: `/api/v1/petition/decisions/search/download`
- **Authentication**: Required (API Key)

## Library Methods

- `search_petition_decisions_download_get()` - GET method
- `search_petition_decisions_download()` - POST method

## Parameters

Same as [Search](search.md) endpoint, plus:

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `format` | string | No | Download format: `json` or `csv` (default: `json`) | `csv` |

## Response Structure

Returns a `PetitionDecisionResponseBag` object with downloaded data.

## Examples

### Download as JSON

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def download_json():
    client = USPTOClient(api_key="your-api-key-here")
    
    results = await client.search_petition_decisions_download_get(
        q="decisionTypeCodeDescriptionText:Denied",
        format="json",
        limit=100
    )
    
    print(f"Downloaded {len(results.decisions)} decisions")
    
    await client.session.close()

asyncio.run(download_json())
```

### Download as CSV

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def download_csv():
    client = USPTOClient(api_key="your-api-key-here")
    
    results = await client.search_petition_decisions_download_get(
        q="Denied",
        format="csv",
        limit=1000
    )
    
    # Process CSV data
    print("CSV data downloaded")
    
    await client.session.close()

asyncio.run(download_csv())
```

## Related Endpoints

- [Search](search.md) - Search without download
- [Get Decision](get-decision.md) - Get specific decision
