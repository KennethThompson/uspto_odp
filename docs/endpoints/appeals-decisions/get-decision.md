# Get Appeal Decision

## Overview

Retrieve a specific appeal decision document by its document identifier.

## Endpoint Details

- **Method**: `GET`
- **URL**: `/api/v1/patent/appeals/decisions/{documentIdentifier}`
- **Authentication**: Required (API Key)

## Library Method

- `get_appeal_decision(document_identifier: str) -> AppealDecisionIdentifierResponseBag`

## Parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `documentIdentifier` | string | Yes | Document identifier (path parameter) | `document-id-123` |

## Examples

### Basic Usage

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def get_decision():
    client = USPTOClient(api_key="your-api-key-here")
    
    decision = await client.get_appeal_decision("document-id")
    
    print(f"Document Type: {decision.decision.document_type}")
    print(f"Document Name: {decision.decision.document_name}")
    
    await client.session.close()

asyncio.run(get_decision())
```

## Related Endpoints

- [Search](search.md) - Search for decisions
- [Get Decisions by Appeal](get-decisions-by-appeal.md) - Get all decisions for an appeal
