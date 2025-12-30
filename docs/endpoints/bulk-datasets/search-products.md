# Search Dataset Products

## Overview

Search for bulk dataset products available from the USPTO. This endpoint helps you find available datasets by name, type, category, or other criteria.

## Endpoint Details

- **Method**: `GET`
- **URL**: `/api/v1/datasets/products/search`
- **Authentication**: Required (API Key)

## Library Method

- `search_dataset_products_get()`

## Parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `q` | string | No | Search query string | `productType:Patent` |
| `sort` | string | No | Field to sort by followed by order | `releaseDate desc` |
| `offset` | integer | No | Position in dataset to start from (default: 0) | `0` |
| `limit` | integer | No | Number of results to return (default: 25) | `50` |
| `facets` | string | No | Comma-separated list of fields to facet | `productType,productCategory` |
| `fields` | string | No | Comma-separated list of fields to include | `productIdentifier,productName` |
| `filters` | string | No | Filter by field value | `productType Patent` |
| `rangeFilters` | string | No | Filter by range | `releaseDate 2021-01-01:2025-01-01` |

## Response Structure

Returns a `DatasetProductSearchResponseBag` object containing:
- `products` - List of DatasetProduct objects
- `total_num_found` - Total number of matching products
- Each product includes identifier, name, description, type, file count, etc.

## Examples

### Basic Search

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def search_products():
    client = USPTOClient(api_key="your-api-key-here")
    
    results = await client.search_dataset_products_get(q="Patent")
    
    print(f"Found {results.total_num_found} products")
    for product in results.products:
        print(f"{product.product_identifier}: {product.product_name}")
    
    await client.session.close()

asyncio.run(search_products())
```

### Advanced Search with Filters

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def search_with_filters():
    client = USPTOClient(api_key="your-api-key-here")
    
    results = await client.search_dataset_products_get(
        q="Patent",
        filters="productType Patent",
        range_filters="releaseDate 2021-01-01:2025-01-01",
        limit=50
    )
    
    print(f"Found {results.total_num_found} products")
    
    await client.session.close()

asyncio.run(search_with_filters())
```

## Related Endpoints

- [Get Product](get-product.md) - Get detailed product information
- [Get File](get-file.md) - Download product files
- [Bulk Datasets Overview](index.md) - All bulk datasets endpoints
