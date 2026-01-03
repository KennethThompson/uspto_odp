# Get Dataset Product

## Overview

Retrieve detailed information about a specific dataset product, including available files, metadata, and download information. This endpoint supports various filtering and pagination options to control the files returned with the product.

## Endpoint Details

- **Method**: `GET`
- **URL**: `/api/v1/datasets/products/{productIdentifier}`
- **Authentication**: Required (API Key)

## Library Method

```python
get_dataset_product(
    product_identifier: str,
    file_data_from_date: Optional[str] = None,
    file_data_to_date: Optional[str] = None,
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    include_files: Optional[str] = None,
    latest: Optional[str] = None
) -> DatasetProductResponseBag
```

## Parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `product_identifier` | string | Yes | Product identifier (path parameter) | `"product-12345"` |
| `file_data_from_date` | string | No | Filter product files by date from. Format: 'yyyy-MM-dd' | `"2023-01-01"` |
| `file_data_to_date` | string | No | Filter product files by date to. Format: 'yyyy-MM-dd' | `"2023-12-31"` |
| `offset` | integer | No | Number of product file records to skip. Default: 0 | `0` |
| `limit` | integer | No | Number of product file records to collect | `25` |
| `include_files` | string | No | Set to 'true' to include files, 'false' to omit | `"true"` |
| `latest` | string | No | Set to 'true' to return only the latest product file | `"true"` |

## Optional Parameters Discussion

### Date Range Filtering
Use `file_data_from_date` and `file_data_to_date` to filter the product files by their data date range. This is useful when you only need files from a specific time period.

```python
# Get only files from 2023
product = await client.get_dataset_product(
    "product-id",
    file_data_from_date="2023-01-01",
    file_data_to_date="2023-12-31"
)
```

### Pagination
Use `offset` and `limit` to paginate through large numbers of product files. This is helpful when a product contains many files and you want to retrieve them in batches.

```python
# Get files 20-30
product = await client.get_dataset_product(
    "product-id",
    offset=20,
    limit=10
)
```

### File Inclusion Control
Use `include_files` to control whether the file list is included in the response. Set to `"false"` to get product metadata without the file details, which can reduce response size and improve performance.

```python
# Get product info without file list
product = await client.get_dataset_product(
    "product-id",
    include_files="false"
)
```

### Latest File Only
Use `latest="true"` to retrieve only the most recent file for the product. This is useful when you only need the current version of a regularly updated dataset.

```python
# Get only the latest file
product = await client.get_dataset_product(
    "product-id",
    latest="true"
)
```

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

    # Get basic product information
    product = await client.get_dataset_product("product-identifier")

    print(f"Product: {product.dataset_product_bag[0].product_name}")
    print(f"Description: {product.dataset_product_bag[0].product_description}")
    print(f"File Count: {product.dataset_product_bag[0].file_count}")

    await client.session.close()

asyncio.run(get_product())
```

### Get Product with Files Included

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def get_product_with_files():
    client = USPTOClient(api_key="your-api-key-here")

    # Include file details in the response
    product = await client.get_dataset_product(
        "product-identifier",
        include_files="true"
    )

    dataset = product.dataset_product_bag[0]
    print(f"Product: {dataset.product_name}")

    if hasattr(dataset, 'files') and dataset.files:
        print(f"\nAvailable files ({len(dataset.files)}):")
        for file in dataset.files:
            print(f"  - {file.file_name} ({file.file_size} bytes)")
            print(f"    Date: {file.file_date}")

    await client.session.close()

asyncio.run(get_product_with_files())
```

### Get Latest File Only

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def get_latest_file():
    client = USPTOClient(api_key="your-api-key-here")

    # Get only the latest file for this product
    product = await client.get_dataset_product(
        "product-identifier",
        latest="true",
        include_files="true"
    )

    dataset = product.dataset_product_bag[0]
    if hasattr(dataset, 'files') and dataset.files:
        latest_file = dataset.files[0]
        print(f"Latest file: {latest_file.file_name}")
        print(f"Date: {latest_file.file_date}")
        print(f"Size: {latest_file.file_size} bytes")

    await client.session.close()

asyncio.run(get_latest_file())
```

### Filter by Date Range with Pagination

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def get_filtered_product():
    client = USPTOClient(api_key="your-api-key-here")

    # Get product files from 2023, paginated
    product = await client.get_dataset_product(
        "product-identifier",
        file_data_from_date="2023-01-01",
        file_data_to_date="2023-12-31",
        offset=0,
        limit=10,
        include_files="true"
    )

    dataset = product.dataset_product_bag[0]
    print(f"Product: {dataset.product_name}")
    print(f"Total files in product: {dataset.file_count}")

    if hasattr(dataset, 'files') and dataset.files:
        print(f"\nShowing {len(dataset.files)} files from 2023:")
        for file in dataset.files:
            print(f"  - {file.file_name} ({file.file_date})")

    await client.session.close()

asyncio.run(get_filtered_product())
```

### Get Product Metadata Only (No Files)

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def get_metadata_only():
    client = USPTOClient(api_key="your-api-key-here")

    # Get product metadata without file details for faster response
    product = await client.get_dataset_product(
        "product-identifier",
        include_files="false"
    )

    dataset = product.dataset_product_bag[0]
    print(f"Product: {dataset.product_name}")
    print(f"Description: {dataset.product_description}")
    print(f"Total files: {dataset.file_count}")
    print(f"Total size: {dataset.total_size} bytes")
    # No file details will be included when include_files="false"

    await client.session.close()

asyncio.run(get_metadata_only())
```

## Related Endpoints

- [Search Products](search-products.md) - Search for products
- [Get File](get-file.md) - Download product files
- [Bulk Datasets Overview](index.md) - All bulk datasets endpoints
