# Get Patent Assignments

## Overview

Retrieve assignment records for a patent application. This shows ownership transfers and assignments.

## Endpoint Details

- **Method**: `GET`
- **URL**: `/api/v1/patent/applications/{applicationNumberText}/assignment`
- **Authentication**: Required (API Key)

## Library Method

- `get_patent_assignments(serial_number: str) -> AssignmentCollection`

## Parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `applicationNumberText` | string | Yes | Application serial number (path parameter) | `14412875` |

## Response Structure

Returns an `AssignmentCollection` object containing:
- `assignments` - List of assignment records
- Each assignment includes assignor, assignee, assignment date, and other details

## Examples

### Basic Usage

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def get_assignments():
    client = USPTOClient(api_key="your-api-key-here")
    
    assignments = await client.get_patent_assignments("14412875")
    
    print(f"Total assignments: {len(assignments.assignments)}")
    for assignment in assignments.assignments:
        print(f"Assignee: {assignment.assignee_name}")
        print(f"Date: {assignment.assignment_date}")
    
    await client.session.close()

asyncio.run(get_assignments())
```

## Related Endpoints

- [Get Patent Wrapper](get-patent-wrapper.md) - Get complete application information
- [Transactions](transactions.md) - Get transaction history
