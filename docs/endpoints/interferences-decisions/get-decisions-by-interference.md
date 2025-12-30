# Get Decisions by Interference

## Overview

Retrieve all decision documents for a specific interference.

## Endpoint Details

- **Method**: `GET`
- **URL**: `/api/v1/patent/interferences/{interferenceNumber}/decisions`
- **Authentication**: Required (API Key)

## Library Method

- `get_interference_decisions_by_interference(interference_number: str) -> InterferenceDecisionByInterferenceResponseBag`

## Parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `interferenceNumber` | string | Yes | Interference number identifier (path parameter) | `106000` or `106,001` |

## Examples

### Basic Usage

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def get_decisions_by_interference():
    client = USPTOClient(api_key="your-api-key-here")
    
    decisions = await client.get_interference_decisions_by_interference("106000")
    
    print(f"Found {len(decisions.decisions)} decisions")
    for decision in decisions.decisions:
        print(f"{decision.document_type}: {decision.document_name}")
    
    await client.session.close()

asyncio.run(get_decisions_by_interference())
```

## Related Endpoints

- [Get Decision](get-decision.md) - Get specific decision
- [Search](search.md) - Search for decisions
- [Interferences Decisions Overview](index.md) - All interferences decisions endpoints
