# Get Decisions by Trial

## Overview

Retrieve all decision documents for a specific trial proceeding.

## Endpoint Details

- **Method**: `GET`
- **URL**: `/api/v1/patent/trials/{trialNumber}/decisions`
- **Authentication**: Required (API Key)

## Library Method

- `get_trial_decisions_by_trial(trial_number: str) -> TrialDecisionByTrialResponseBag`

## Parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `trialNumber` | string | Yes | Trial number identifier (path parameter) | `IPR2020-00001` |

## Examples

### Basic Usage

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def get_decisions_by_trial():
    client = USPTOClient(api_key="your-api-key-here")
    
    decisions = await client.get_trial_decisions_by_trial("IPR2020-00001")
    
    print(f"Found {len(decisions.decisions)} decisions")
    for decision in decisions.decisions:
        print(f"{decision.document_type}: {decision.document_name}")
    
    await client.session.close()

asyncio.run(get_decisions_by_trial())
```

## Related Endpoints

- [Get Trial Proceeding](../trials-proceedings/get-proceeding.md) - Get trial proceeding details
- [Get Decision](get-decision.md) - Get specific decision
- [Trials Decisions Overview](index.md) - All trials decisions endpoints
