# Get Application Metadata

## Overview

Retrieve metadata for a specific patent application. This endpoint provides essential application information including filing date, patent number, application type, and more.

## Endpoint Details

- **Method**: `GET`
- **URL**: `/api/v1/patent/applications/{applicationNumberText}/meta-data`
- **Authentication**: Required (API Key)

## Library Methods

- `get_app_metadata(application_number: str) -> ApplicationMetadataResponse` - Direct endpoint
- `get_app_metadata_from_patent_number(patent_number: str) -> Optional[ApplicationMetadataResponse]` - Convenience method (searches by patent number first)

## Parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `applicationNumberText` | string | Yes | Application serial number (path parameter) | `14412875` or `14/412,875` |

## Response Structure

Returns an `ApplicationMetadataResponse` object containing:
- `application_number` - Application number
- `metadata` - ApplicationMetadata object with:
  - `filing_date` - Filing date
  - `patent_number` - Patent number (if granted)
  - `application_type` - Application type code
  - `status` - Application status
  - And more metadata fields
- `request_identifier` - Unique request identifier

## Examples

### Basic Usage

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def get_metadata():
    client = USPTOClient(api_key="your-api-key-here")
    
    # Get metadata by application number
    metadata = await client.get_app_metadata("14412875")
    
    print(f"Application: {metadata.application_number}")
    print(f"Filing Date: {metadata.metadata.filing_date}")
    print(f"Patent Number: {metadata.metadata.patent_number}")
    
    await client.session.close()

asyncio.run(get_metadata())
```

### Using Patent Number (Convenience Method)

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def get_metadata_from_patent():
    client = USPTOClient(api_key="your-api-key-here")
    
    # Get metadata using patent number (searches for app number first)
    metadata = await client.get_app_metadata_from_patent_number("9022434")
    
    if metadata:
        print(f"Application: {metadata.application_number}")
        print(f"Filing Date: {metadata.metadata.filing_date}")
    else:
        print("Patent number not found")
    
    await client.session.close()

asyncio.run(get_metadata_from_patent())
```

### Error Handling

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient, USPTOError

async def get_metadata_with_error_handling():
    client = USPTOClient(api_key="your-api-key-here")
    
    try:
        metadata = await client.get_app_metadata("invalid-number")
    except USPTOError as e:
        if e.code == 404:
            print("Application not found")
        else:
            print(f"Error {e.code}: {e.error}")
    finally:
        await client.session.close()

asyncio.run(get_metadata_with_error_handling())
```

## Related Endpoints

- [Get Patent Wrapper](get-patent-wrapper.md) - Get complete application information
- [Search](search.md) - Search for applications
- [Documents](documents.md) - Get application documents
