# Search Patent Applications

## Overview

Search for patent applications using either GET (query parameters) or POST (JSON payload) methods. This endpoint supports complex queries with boolean operators, wildcards, filtering, sorting, and faceting.

## Endpoint Details

- **Methods**: `GET`, `POST`
- **URL**: `/api/v1/patent/applications/search`
- **Authentication**: Required (API Key)

## Library Methods

- `search_patent_applications_get()` - GET method with query parameters
- `search_patent_applications()` - POST method with JSON payload

## Parameters

### GET Method Parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `q` | string | No | Search query string. Accepts boolean operators (AND, OR, NOT), wildcards (*), and exact phrases ("") | `applicationNumberText:14412875` |
| `sort` | string | No | Field to sort by followed by order (asc/desc) | `applicationMetaData.filingDate desc` |
| `offset` | integer | No | Position in dataset to start from (default: 0) | `0` |
| `limit` | integer | No | Number of results to return (default: 25) | `50` |
| `facets` | string | No | Comma-separated list of fields to facet | `applicationMetaData.applicationTypeCode,applicationMetaData.docketNumber` |
| `fields` | string | No | Comma-separated list of fields to include in response | `applicationNumberText,applicationMetaData.patentNumber` |
| `filters` | string | No | Filter by field value. Format: `fieldName value1,value2` | `applicationMetaData.applicationTypeCode UTL,DES` |
| `rangeFilters` | string | No | Filter by range. Format: `fieldName min:max` | `applicationMetaData.grantDate 2010-01-01:2011-01-01` |

### POST Method Payload

The POST method accepts a JSON payload with the same parameters as query parameters, plus additional options:

```json
{
  "q": "applicationNumberText:14412875",
  "sort": "applicationMetaData.filingDate desc",
  "offset": 0,
  "limit": 25,
  "facets": ["applicationMetaData.applicationTypeCode"],
  "fields": ["applicationNumberText", "applicationMetaData.patentNumber"],
  "filters": {
    "applicationMetaData.applicationTypeCode": ["UTL", "DES"]
  },
  "rangeFilters": {
    "applicationMetaData.filingDate": {
      "min": "2020-01-01",
      "max": "2024-01-01"
    }
  }
}
```

## Response Structure

The response is a dictionary containing:

- `totalNumFound` - Total number of matching results
- `patentFileWrapperDataBag` - Array of patent application records
- `facets` - Facet counts (if facets parameter provided)
- `requestIdentifier` - Unique request identifier

## Examples

### Basic Search (GET)

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def basic_search():
    client = USPTOClient(api_key="your-api-key-here")
    
    # Search by application number
    results = await client.search_patent_applications_get(
        q="applicationNumberText:14412875"
    )
    
    print(f"Found {results.get('totalNumFound', 0)} results")
    
    await client.session.close()

asyncio.run(basic_search())
```

### Advanced Search with Filters (GET)

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def advanced_search():
    client = USPTOClient(api_key="your-api-key-here")
    
    # Complex search with multiple filters
    results = await client.search_patent_applications_get(
        q="applicationMetaData.inventorBag.inventorNameText:Smith",
        sort="applicationMetaData.filingDate desc",
        filters="applicationMetaData.applicationTypeCode UTL",
        range_filters="applicationMetaData.filingDate 2020-01-01:2024-01-01",
        limit=100,
        offset=0
    )
    
    print(f"Found {results.get('totalNumFound', 0)} results")
    for app in results.get('patentFileWrapperDataBag', [])[:5]:
        print(f"- {app.get('applicationNumberText')}")
    
    await client.session.close()

asyncio.run(advanced_search())
```

### Search with POST Method

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def post_search():
    client = USPTOClient(api_key="your-api-key-here")
    
    # POST method with JSON payload
    payload = {
        "q": "applicationMetaData.patentNumber:12345678",
        "sort": "applicationMetaData.filingDate desc",
        "offset": 0,
        "limit": 25,
        "facets": ["applicationMetaData.applicationTypeCode"],
        "fields": ["applicationNumberText", "applicationMetaData.patentNumber"]
    }
    
    results = await client.search_patent_applications(payload)
    
    print(f"Found {results.get('totalNumFound', 0)} results")
    
    await client.session.close()

asyncio.run(post_search())
```

### Search with Faceting

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def faceted_search():
    client = USPTOClient(api_key="your-api-key-here")
    
    # Search with faceting to get counts by application type
    results = await client.search_patent_applications_get(
        q="applicationMetaData.filingDate:[2020 TO 2024]",
        facets="applicationMetaData.applicationTypeCode",
        limit=0  # Set to 0 to only get facets
    )
    
    # Access facet counts
    facets = results.get('facets', {})
    for field, counts in facets.items():
        print(f"{field}:")
        for value, count in counts.items():
            print(f"  {value}: {count}")
    
    await client.session.close()

asyncio.run(faceted_search())
```

### Error Handling

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient, USPTOError

async def search_with_error_handling():
    client = USPTOClient(api_key="your-api-key-here")
    
    try:
        results = await client.search_patent_applications_get(
            q="invalid:query"
        )
    except USPTOError as e:
        if e.code == 400:
            print(f"Bad request: {e.error_details}")
        elif e.code == 403:
            print("Access forbidden - check your API key")
        else:
            print(f"Error {e.code}: {e.error}")
    finally:
        await client.session.close()

asyncio.run(search_with_error_handling())
```

## Query Syntax

The `q` parameter supports:

- **Field Search**: `fieldName:value` - Search specific field
- **Boolean Operators**: `term1 AND term2`, `term1 OR term2`, `NOT term`
- **Wildcards**: `term*` - Match any characters after term
- **Exact Phrases**: `"exact phrase"` - Match exact phrase
- **Range Queries**: `field:[min TO max]` - Range search

## Related Endpoints

- [Search/Download](search-download.md) - Download search results as file
- [Get Patent Wrapper](get-patent-wrapper.md) - Get detailed application information
- [Metadata](metadata.md) - Get application metadata

## See Also

- [Patent Applications Overview](index.md) - All patent application endpoints
- [Quick Start Guide](../../quickstart.md) - Getting started guide
- [Examples](../../examples.md) - More examples
