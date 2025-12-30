# Get Patent Wrapper

## Overview

Retrieve complete patent application file wrapper information for a specific application number. This includes all application metadata, events, inventors, and related information.

## Endpoint Details

- **Method**: `GET`
- **URL**: `/api/v1/patent/applications/{applicationNumberText}`
- **Authentication**: Required (API Key)

## Library Method

- `get_patent_wrapper(serial_number: str) -> PatentFileWrapper`

## Parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `applicationNumberText` | string | Yes | Application serial number (path parameter). Supports regular US applications and PCT applications | `14412875` or `PCTUS2004027676` |

### Application Number Formats

- **US Applications**: `14412875` or `US14412875` (US prefix is automatically stripped)
- **PCT Applications**: `PCTUS2004027676` or `PCTUS0427676` (supports various formats)

## Response Structure

Returns a `PatentFileWrapper` object containing:
- `application_number` - Application number
- `title` - Application title
- `inventors` - List of inventors
- `events` - Application events/history
- `metadata` - Application metadata
- `request_identifier` - Unique request identifier

## Examples

### Basic Usage

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def get_wrapper():
    client = USPTOClient(api_key="your-api-key-here")
    
    # Get patent wrapper
    wrapper = await client.get_patent_wrapper("14412875")
    
    print(f"Application: {wrapper.application_number}")
    print(f"Title: {wrapper.title}")
    print(f"Inventors: {[inv.name for inv in wrapper.inventors]}")
    
    await client.session.close()

asyncio.run(get_wrapper())
```

### PCT Application

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def get_pct_wrapper():
    client = USPTOClient(api_key="your-api-key-here")
    
    # Get PCT application wrapper
    wrapper = await client.get_patent_wrapper("PCTUS2004027676")
    
    print(f"PCT Application: {wrapper.application_number}")
    
    await client.session.close()

asyncio.run(get_pct_wrapper())
```

### Error Handling

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient, USPTOError

async def get_wrapper_with_error_handling():
    client = USPTOClient(api_key="your-api-key-here")
    
    try:
        wrapper = await client.get_patent_wrapper("invalid-number")
    except USPTOError as e:
        if e.code == 404:
            print("Application not found")
        else:
            print(f"Error {e.code}: {e.error}")
    finally:
        await client.session.close()

asyncio.run(get_wrapper_with_error_handling())
```

## Related Endpoints

- [Metadata](metadata.md) - Get application metadata only
- [Documents](documents.md) - Get application documents
- [Search](search.md) - Search for applications
