# Get Continuity Information

## Overview

Retrieve continuity data showing parent/child relationships between patent applications (continuations, divisions, continuations-in-part, etc.).

## Endpoint Details

- **Method**: `GET`
- **URL**: `/api/v1/patent/applications/{applicationNumberText}/continuity`
- **Authentication**: Required (API Key)

## Library Method

- `get_continuity(serial_number: str) -> ContinuityCollection`

## Parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `applicationNumberText` | string | Yes | Application serial number (path parameter) | `14412875` |

## Response Structure

Returns a `ContinuityCollection` object containing:
- `parent_continuities` - List of parent applications
- `child_continuities` - List of child applications
- Each continuity includes relationship type and application number

## Examples

### Basic Usage

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def get_continuity():
    client = USPTOClient(api_key="your-api-key-here")
    
    continuity = await client.get_continuity("14412875")
    
    print(f"Parent applications: {len(continuity.parent_continuities)}")
    for parent in continuity.parent_continuities:
        print(f"  {parent.application_number} - {parent.relationship_type}")
    
    print(f"Child applications: {len(continuity.child_continuities)}")
    for child in continuity.child_continuities:
        print(f"  {child.application_number} - {child.relationship_type}")
    
    await client.session.close()

asyncio.run(get_continuity())
```

## Related Endpoints

- [Get Patent Wrapper](get-patent-wrapper.md) - Get complete application information
- [Search](search.md) - Search for related applications
