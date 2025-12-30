# Search/Download Patent Applications

## Overview

Download patent application search results as a file. This endpoint is optimized for bulk downloads and supports both JSON and CSV formats.

## Endpoint Details

- **Methods**: `GET`, `POST`
- **URL**: `/api/v1/patent/applications/search/download`
- **Authentication**: Required (API Key)

## Library Methods

- `search_patent_applications_download_get()` - GET method with query parameters
- `search_patent_applications_download()` - POST method with JSON payload

## Parameters

### GET Method Parameters

All parameters from the [Search](search.md) endpoint, plus:

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `format` | string | No | Download format: `json` or `csv` (default: `json`) | `csv` |

### POST Method Payload

Same as [Search](search.md) POST payload, with optional `format` field.

## Response Structure

Returns a `PatentDataResponse` object containing:
- `data` - The downloaded data (format depends on `format` parameter)
- `request_identifier` - Unique request identifier

## Examples

### Download as JSON (GET)

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def download_json():
    client = USPTOClient(api_key="your-api-key-here")
    
    # Download search results as JSON
    results = await client.search_patent_applications_download_get(
        q="applicationMetaData.filingDate:[2020 TO 2024]",
        format="json",
        limit=100
    )
    
    print(f"Downloaded {len(results.data)} records")
    
    await client.session.close()

asyncio.run(download_json())
```

### Download as CSV (GET)

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def download_csv():
    client = USPTOClient(api_key="your-api-key-here")
    
    # Download search results as CSV
    results = await client.search_patent_applications_download_get(
        q="applicationMetaData.applicationTypeCode:UTL",
        format="csv",
        limit=1000
    )
    
    # Save CSV data
    with open("patents.csv", "wb") as f:
        f.write(results.data)
    
    await client.session.close()

asyncio.run(download_csv())
```

### Download with POST Method

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def download_post():
    client = USPTOClient(api_key="your-api-key-here")
    
    payload = {
        "q": "applicationMetaData.patentNumber:12345678",
        "limit": 500,
        "format": "json"
    }
    
    results = await client.search_patent_applications_download(payload)
    
    print(f"Downloaded data: {len(results.data)} records")
    
    await client.session.close()

asyncio.run(download_post())
```

## Related Endpoints

- [Search](search.md) - Search without download
- [Get Patent Wrapper](get-patent-wrapper.md) - Get detailed application information
