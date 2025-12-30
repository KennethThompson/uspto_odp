# Get Foreign Priority Claims

## Overview

Retrieve foreign priority claims for a patent application. This shows priority claims to foreign applications.

## Endpoint Details

- **Method**: `GET`
- **URL**: `/api/v1/patent/applications/{applicationNumberText}/foreign-priority`
- **Authentication**: Required (API Key)

## Library Method

- `get_foreign_priority(serial_number: str) -> ForeignPriorityCollection`

## Parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `applicationNumberText` | string | Yes | Application serial number (path parameter) | `14412875` |

## Response Structure

Returns a `ForeignPriorityCollection` object containing:
- `foreign_priorities` - List of foreign priority claims
- Each priority includes country, application number, filing date, and other details

## Examples

### Basic Usage

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def get_foreign_priority():
    client = USPTOClient(api_key="your-api-key-here")
    
    priorities = await client.get_foreign_priority("14412875")
    
    print(f"Foreign priorities: {len(priorities.foreign_priorities)}")
    for priority in priorities.foreign_priorities:
        print(f"Country: {priority.country}")
        print(f"Application: {priority.application_number}")
        print(f"Filing Date: {priority.filing_date}")
    
    await client.session.close()

asyncio.run(get_foreign_priority())
```

## Related Endpoints

- [Get Patent Wrapper](get-patent-wrapper.md) - Get complete application information
- [Metadata](metadata.md) - Get application metadata
