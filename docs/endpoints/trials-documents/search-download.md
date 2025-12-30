# Search/Download Trial Documents

## Overview

Download trial document search results as a file. Supports JSON and CSV formats.

## Endpoint Details

- **Methods**: `GET`, `POST`
- **URL**: `/api/v1/patent/trials/documents/search/download`
- **Authentication**: Required (API Key)

## Library Methods

- `search_trial_documents_download_get()` - GET method
- `search_trial_documents_download()` - POST method

## Parameters

Same as [Search](search.md) endpoint, plus `format` parameter (`json` or `csv`).

## Examples

### Download as JSON

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def download_json():
    client = USPTOClient(api_key="your-api-key-here")
    
    results = await client.search_trial_documents_download_get(
        q="trialNumber:IPR2020-00001",
        format="json"
    )
    
    print(f"Downloaded {len(results.documents)} documents")
    
    await client.session.close()

asyncio.run(download_json())
```

## Related Endpoints

- [Search](search.md) - Search without download
- [Get Document](get-document.md) - Get specific document
