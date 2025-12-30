# Search Trial Documents

## Overview

Search for PTAB trial documents using either GET (query parameters) or POST (JSON payload) methods.

## Endpoint Details

- **Methods**: `GET`, `POST`
- **URL**: `/api/v1/patent/trials/documents/search`
- **Authentication**: Required (API Key)

## Library Methods

- `search_trial_documents_get()` - GET method
- `search_trial_documents()` - POST method

## Parameters

Similar to other search endpoints. See [Search Trial Proceedings](../trials-proceedings/search.md) for parameter details.

## Examples

### Basic Search

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def search_documents():
    client = USPTOClient(api_key="your-api-key-here")
    
    results = await client.search_trial_documents_get(q="trialNumber:IPR2020-00001")
    
    print(f"Found {results.total_num_found} documents")
    
    await client.session.close()

asyncio.run(search_documents())
```

## Related Endpoints

- [Search/Download](search-download.md) - Download search results
- [Get Document](get-document.md) - Get specific document
- [Get Documents by Trial](get-documents-by-trial.md) - Get all documents for a trial
