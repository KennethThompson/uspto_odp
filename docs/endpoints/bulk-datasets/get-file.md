# Get Dataset File

## Overview

Download a specific file from a dataset product. This endpoint returns file content or redirects to the download location.

## Endpoint Details

- **Method**: `GET`
- **URL**: `/api/v1/datasets/products/files/{productIdentifier}/{fileName}`
- **Authentication**: Required (API Key)

## Library Method

- `get_dataset_file(product_identifier: str, file_name: str) -> DatasetFileResponseBag`

## Parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `productIdentifier` | string | Yes | Product identifier (path parameter) | `product-12345` |
| `fileName` | string | Yes | File name (path parameter) | `data.zip` |

## Response Structure

Returns a `DatasetFileResponseBag` object containing:
- `file_content` - File content (may be binary)
- `file_name` - File name
- `content_type` - MIME type
- `request_identifier` - Unique request identifier

## Examples

### Download File

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def download_file():
    client = USPTOClient(api_key="your-api-key-here")
    
    file_data = await client.get_dataset_file("product-identifier", "data.zip")
    
    # Save file
    if file_data.file_content:
        with open("downloaded_file.zip", "wb") as f:
            f.write(file_data.file_content)
        print(f"Downloaded {file_data.file_name}")
    
    await client.session.close()

asyncio.run(download_file())
```

### Error Handling

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient, USPTOError

async def download_with_error_handling():
    client = USPTOClient(api_key="your-api-key-here")
    
    try:
        file_data = await client.get_dataset_file("product-id", "file.zip")
        # Process file
    except USPTOError as e:
        if e.code == 404:
            print("File not found")
        else:
            print(f"Error {e.code}: {e.error}")
    finally:
        await client.session.close()

asyncio.run(download_with_error_handling())
```

## Related Endpoints

- [Get Product](get-product.md) - Get product information and file list
- [Search Products](search-products.md) - Search for products
- [Bulk Datasets Overview](index.md) - All bulk datasets endpoints
