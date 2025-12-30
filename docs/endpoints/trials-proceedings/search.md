# Search Trial Proceedings

## Overview

Search for PTAB trial proceedings using either GET (query parameters) or POST (JSON payload) methods. Find trials by trial number, patent number, trial type (IPR, PGR, CBM), status, and more.

## Endpoint Details

- **Methods**: `GET`, `POST`
- **URL**: `/api/v1/patent/trials/proceedings/search`
- **Authentication**: Required (API Key)

## Library Methods

- `search_trial_proceedings_get()` - GET method with query parameters
- `search_trial_proceedings()` - POST method with JSON payload

## Parameters

### GET Method Parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `q` | string | No | Search query string | `trialType:IPR` or `trialNumber:IPR2020-00001` |
| `sort` | string | No | Field to sort by followed by order | `filingDate desc` |
| `offset` | integer | No | Position in dataset to start from (default: 0) | `0` |
| `limit` | integer | No | Number of results to return (default: 25) | `50` |
| `facets` | string | No | Comma-separated list of fields to facet | `trialType,proceedingStatus` |
| `fields` | string | No | Comma-separated list of fields to include | `trialNumber,patentNumber` |
| `filters` | string | No | Filter by field value | `proceedingStatus Instituted` |
| `rangeFilters` | string | No | Filter by range | `filingDate 2021-01-01:2025-01-01` |

## Response Structure

Returns a `TrialProceedingResponseBag` object containing:
- `proceedings` - List of TrialProceeding objects
- `total_num_found` - Total number of matching results

## Examples

### Basic Search

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def search_proceedings():
    client = USPTOClient(api_key="your-api-key-here")
    
    results = await client.search_trial_proceedings_get(q="trialType:IPR")
    
    print(f"Found {results.total_num_found} proceedings")
    for proceeding in results.proceedings[:5]:
        print(f"{proceeding.trial_number}: {proceeding.trial_type}")
    
    await client.session.close()

asyncio.run(search_proceedings())
```

### Advanced Search

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def advanced_search():
    client = USPTOClient(api_key="your-api-key-here")
    
    results = await client.search_trial_proceedings_get(
        q="IPR",
        filters="proceedingStatus Instituted",
        range_filters="filingDate 2021-01-01:2025-01-01",
        limit=100
    )
    
    print(f"Found {results.total_num_found} proceedings")
    
    await client.session.close()

asyncio.run(advanced_search())
```

## Related Endpoints

- [Search/Download](search-download.md) - Download search results
- [Get Proceeding](get-proceeding.md) - Get specific proceeding
- [Trials Proceedings Overview](index.md) - All trials proceedings endpoints
