# Bulk Datasets Endpoints

## Overview

The Bulk Datasets endpoints provide access to USPTO bulk data products. These endpoints allow you to search for available datasets, get product information, and download dataset files.

All endpoints in this category begin with `/api/v1/datasets/products`.

## Available Endpoints

| Endpoint | Methods | Description | Documentation |
|----------|---------|-------------|---------------|
| `/search` | GET | Search for bulk dataset products | [Search Products](search-products.md) |
| `/{productIdentifier}` | GET | Get detailed information about a specific product | [Get Product](get-product.md) |
| `/files/{productIdentifier}/{fileName}` | GET | Download a specific file from a product | [Get File](get-file.md) |

## Quick Start

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def main():
    client = USPTOClient(api_key="your-api-key-here")
    
    # Search for products
    results = await client.search_dataset_products_get(q="Patent")
    
    # Get product details
    product = await client.get_dataset_product("product-identifier")
    
    # Download a file
    file_data = await client.get_dataset_file("product-identifier", "filename.zip")
    
    await client.session.close()

asyncio.run(main())
```

## Common Use Cases

### Finding Available Datasets
Use the [Search Products](search-products.md) endpoint to:
- Search for datasets by name or description
- Filter by product type or category
- Find datasets updated within a date range

### Getting Product Information
Use the [Get Product](get-product.md) endpoint to:
- View product metadata
- See available files
- Get download URLs
- Check file sizes and counts

### Downloading Files
Use the [Get File](get-file.md) endpoint to:
- Download specific dataset files
- Access bulk data products programmatically

## Related Documentation

- [Quick Start Guide](../../quickstart.md) - Get started quickly
- [Examples](../../examples.md) - More code examples
- [API Reference](../../api/client.md) - Complete API documentation
