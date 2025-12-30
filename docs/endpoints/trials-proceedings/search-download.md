# Search/Download Trial Proceedings

## Overview

Download trial proceeding search results as a file. Supports JSON and CSV formats.

## Endpoint Details

- **Methods**: `GET`, `POST`
- **URL**: `/api/v1/patent/trials/proceedings/search/download`
- **Authentication**: Required (API Key)

## Library Methods

- `search_trial_proceedings_download_get()` - GET method
- `search_trial_proceedings_download()` - POST method

## Parameters

Same as [Search](search.md) endpoint, plus `format` parameter (`json` or `csv`).

## Examples

### Download as JSON

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def download_json():
    client = USPTOClient(api_key="your-api-key-here")
    
    results = await client.search_trial_proceedings_download_get(
        q="trialType:IPR",
        format="json",
        limit=100
    )
    
    print(f"Downloaded {len(results.proceedings)} proceedings")
    
    await client.session.close()

asyncio.run(download_json())
```

## Related Endpoints

- [Search](search.md) - Search without download
- [Get Proceeding](get-proceeding.md) - Get specific proceeding
