# Get Dataset Product

## Overview

Retrieve detailed information about a specific dataset product, including available files, metadata, and download information.

## Endpoint Details

- **Method**: `GET`
- **URL**: `/api/v1/datasets/products/{productIdentifier}`
- **Authentication**: Required (API Key)

## Library Method

- `get_dataset_product(product_identifier: str) -> DatasetProductResponseBag`

## Parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `productIdentifier` | string | Yes | Product identifier (path parameter) | `product-12345` |
| `fileDataFromDate` | string | No | Filter files from date (query parameter) | `2021-01-01` |
| `fileDataToDate` | string | No | Filter files to date (query parameter) | `2024-01-01` |
| `offset` | integer | No | Number of file records to skip | `0` |
| `limit` | integer | No | Number of file records to return | `25` |
| `includeFiles` | string | No | Include files in response (`true`/`false`) | `true` |
| `latest` | string | No | Return only latest file (`true`/`false`) | `false` |

## Response Structure

Returns a `DatasetProductResponseBag` object containing:
- `product` - DatasetProduct object with:
  - `product_identifier` - Product identifier
  - `product_name` - Product name
  - `product_description` - Description
  - `file_count` - Number of files
  - `total_size_bytes` - Total size
  - `files` - List of available files (if includeFiles=true)

## Examples

### Basic Usage

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def get_product():
    client = USPTOClient(api_key="your-api-key-here")
    
    product = await client.get_dataset_product("product-identifier")
    
    print(f"Product: {product.product.product_name}")
    print(f"Description: {product.product.product_description}")
    print(f"Files: {product.product.file_count}")
    
    await client.session.close()

asyncio.run(get_product())
```

### Get Product with Files

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def get_product_with_files():
    client = USPTOClient(api_key="your-api-key-here")
    
    # Note: includeFiles parameter would need to be added to the method
    # This is a conceptual example
    product = await client.get_dataset_product("product-identifier")
    
    if hasattr(product.product, 'files') and product.product.files:
        print(f"Available files:")
        for file in product.product.files:
            print(f"  {file.file_name} ({file.file_size} bytes)")
    
    await client.session.close()

asyncio.run(get_product_with_files())
```

## Related Endpoints

- [Search Products](search-products.md) - Search for products
- [Get File](get-file.md) - Download product files
- [Bulk Datasets Overview](index.md) - All bulk datasets endpoints
