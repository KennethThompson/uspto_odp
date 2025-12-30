# Get Decisions by Appeal

## Overview

Retrieve all decision documents for a specific appeal.

## Endpoint Details

- **Method**: `GET`
- **URL**: `/api/v1/patent/appeals/{appealNumber}/decisions`
- **Authentication**: Required (API Key)

## Library Method

- `get_appeal_decisions_by_appeal(appeal_number: str) -> AppealDecisionByAppealResponseBag`

## Parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `appealNumber` | string | Yes | Appeal number identifier (path parameter) | `2020-00001` |

## Examples

### Basic Usage

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def get_decisions_by_appeal():
    client = USPTOClient(api_key="your-api-key-here")
    
    decisions = await client.get_appeal_decisions_by_appeal("2020-00001")
    
    print(f"Found {len(decisions.decisions)} decisions")
    for decision in decisions.decisions:
        print(f"{decision.document_type}: {decision.document_name}")
    
    await client.session.close()

asyncio.run(get_decisions_by_appeal())
```

## Related Endpoints

- [Get Decision](get-decision.md) - Get specific decision
- [Search](search.md) - Search for decisions
- [Appeals Decisions Overview](index.md) - All appeals decisions endpoints
