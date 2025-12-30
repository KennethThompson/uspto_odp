# Get Trial Proceeding

## Overview

Retrieve a specific trial proceeding by its trial number.

## Endpoint Details

- **Method**: `GET`
- **URL**: `/api/v1/patent/trials/proceedings/{trialNumber}`
- **Authentication**: Required (API Key)

## Library Method

- `get_trial_proceeding(trial_number: str) -> TrialProceedingIdentifierResponseBag`

## Parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `trialNumber` | string | Yes | Trial number identifier (path parameter) | `IPR2020-00001` |

## Response Structure

Returns a `TrialProceedingIdentifierResponseBag` object containing:
- `proceeding` - TrialProceeding object with proceeding details
- `request_identifier` - Unique request identifier

## Examples

### Basic Usage

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def get_proceeding():
    client = USPTOClient(api_key="your-api-key-here")
    
    proceeding = await client.get_trial_proceeding("IPR2020-00001")
    
    print(f"Trial Number: {proceeding.proceeding.trial_number}")
    print(f"Trial Type: {proceeding.proceeding.trial_type}")
    print(f"Status: {proceeding.proceeding.proceeding_status}")
    
    await client.session.close()

asyncio.run(get_proceeding())
```

## Related Endpoints

- [Search](search.md) - Search for proceedings
- [Get Decisions by Trial](../trials-decisions/get-decisions-by-trial.md) - Get decisions for this trial
- [Get Documents by Trial](../trials-documents/get-documents-by-trial.md) - Get documents for this trial
