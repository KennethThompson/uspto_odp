# Search Petition Decisions

## Overview

Search for petition decisions using either GET (query parameters) or POST (JSON payload) methods. This endpoint allows you to find petition decisions by various criteria including patent number, decision type, date, and more.

## Endpoint Details

- **Methods**: `GET`, `POST`
- **URL**: `/api/v1/petition/decisions/search`
- **Authentication**: Required (API Key)

## Library Methods

- `search_petition_decisions_get()` - GET method with query parameters
- `search_petition_decisions()` - POST method with JSON payload

## Parameters

### GET Method Parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `q` | string | No | Search query string | `decisionTypeCodeDescriptionText:Denied` |
| `sort` | string | No | Field to sort by followed by order | `petitionMailDate desc` |
| `offset` | integer | No | Position in dataset to start from (default: 0) | `0` |
| `limit` | integer | No | Number of results to return (default: 25) | `50` |
| `facets` | string | No | Comma-separated list of fields to facet | `decisionTypeCode,businessEntityStatusCategory` |
| `fields` | string | No | Comma-separated list of fields to include | `petitionDecisionRecordIdentifier,patentNumber` |
| `filters` | string | No | Filter by field value | `businessEntityStatusCategory Small` |
| `rangeFilters` | string | No | Filter by range | `petitionMailDate 2021-01-01:2025-01-01` |

### POST Method Payload

Same structure as GET parameters, provided as JSON object.

## Response Structure

Returns a `PetitionDecisionResponseBag` object containing:
- `decisions` - List of PetitionDecision objects
- `total_num_found` - Total number of matching results
- `facets` - Facet counts (if facets parameter provided)

## Examples

### Basic Search (GET)

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def search_decisions():
    client = USPTOClient(api_key="your-api-key-here")
    
    results = await client.search_petition_decisions_get(
        q="decisionTypeCodeDescriptionText:Denied"
    )
    
    print(f"Found {results.total_num_found} decisions")
    for decision in results.decisions[:5]:
        print(f"{decision.patent_number}: {decision.decision_type_code_description_text}")
    
    await client.session.close()

asyncio.run(search_decisions())
```

### Advanced Search with Filters

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def advanced_search():
    client = USPTOClient(api_key="your-api-key-here")
    
    results = await client.search_petition_decisions_get(
        q="patentNumber:12345678",
        filters="businessEntityStatusCategory Small",
        range_filters="petitionMailDate 2021-01-01:2025-01-01",
        limit=100
    )
    
    print(f"Found {results.total_num_found} decisions")
    
    await client.session.close()

asyncio.run(advanced_search())
```

### Search with POST Method

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def search_post():
    client = USPTOClient(api_key="your-api-key-here")
    
    payload = {
        "q": "decisionTypeCodeDescriptionText:Denied",
        "limit": 50,
        "filters": {
            "businessEntityStatusCategory": ["Small"]
        }
    }
    
    results = await client.search_petition_decisions(payload)
    
    print(f"Found {results.total_num_found} decisions")
    
    await client.session.close()

asyncio.run(search_post())
```

## Related Endpoints

- [Search/Download](search-download.md) - Download search results
- [Get Decision](get-decision.md) - Get specific decision
- [Petition Decisions Overview](index.md) - All petition decisions endpoints
