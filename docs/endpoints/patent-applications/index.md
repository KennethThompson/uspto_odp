# Patent Applications Endpoints

## Overview

The Patent Applications endpoints provide comprehensive access to patent application data from the USPTO. These endpoints allow you to search for applications, retrieve detailed information, access documents, and explore relationships between applications.

All endpoints in this category begin with `/api/v1/patent/applications`.

## Available Endpoints

| Endpoint | Methods | Description | Documentation |
|----------|---------|-------------|---------------|
| `/search` | GET, POST | Search for patent applications using query parameters or JSON payload | [Search](search.md) |
| `/search/download` | GET, POST | Download search results as a file | [Search/Download](search-download.md) |
| `/{appNumber}` | GET | Get complete patent file wrapper for an application | [Get Patent Wrapper](get-patent-wrapper.md) |
| `/{appNumber}/meta-data` | GET | Get metadata for a specific application | [Metadata](metadata.md) |
| `/{appNumber}/adjustment` | GET | Get patent term adjustment information | [Adjustment](adjustment.md) |
| `/{appNumber}/assignment` | GET | Get assignment records for an application | [Assignment](assignment.md) |
| `/{appNumber}/attorney` | GET | Get attorney/agent information | [Attorney](attorney.md) |
| `/{appNumber}/continuity` | GET | Get continuity data (parent/child relationships) | [Continuity](continuity.md) |
| `/{appNumber}/foreign-priority` | GET | Get foreign priority claims | [Foreign Priority](foreign-priority.md) |
| `/{appNumber}/transactions` | GET | Get transaction history | [Transactions](transactions.md) |
| `/{appNumber}/documents` | GET | Get list of documents for an application | [Documents](documents.md) |
| `/{appNumber}/associated-documents` | GET | Get associated documents | [Associated Documents](associated-documents.md) |

## Quick Start

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def main():
    client = USPTOClient(api_key="your-api-key-here")
    
    # Search for applications
    results = await client.search_patent_applications_get(
        q="applicationNumberText:14412875"
    )
    
    # Get application metadata
    metadata = await client.get_app_metadata("14412875")
    
    await client.session.close()

asyncio.run(main())
```

## Common Use Cases

### Searching Applications
Use the [Search](search.md) endpoint to find applications by:
- Application number
- Patent number
- Inventor name
- Filing date range
- Application type
- And many other criteria

### Retrieving Application Details
Once you have an application number, use the various detail endpoints:
- [Get Patent Wrapper](get-patent-wrapper.md) - Complete application information
- [Metadata](metadata.md) - Basic application metadata
- [Documents](documents.md) - Access application documents

### Exploring Relationships
- [Continuity](continuity.md) - Find related applications (continuations, divisions, etc.)
- [Foreign Priority](foreign-priority.md) - View foreign priority claims
- [Assignment](assignment.md) - Track ownership changes

## Related Documentation

- [Quick Start Guide](../../quickstart.md) - Get started quickly
- [Examples](../../examples.md) - More code examples
- [API Reference](../../api/client.md) - Complete API documentation
