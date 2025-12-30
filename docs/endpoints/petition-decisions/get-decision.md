# Get Petition Decision

## Overview

Retrieve a specific petition decision by its record identifier. Optionally include decision documents in the response.

## Endpoint Details

- **Method**: `GET`
- **URL**: `/api/v1/petition/decisions/{petitionDecisionRecordIdentifier}`
- **Authentication**: Required (API Key)

## Library Method

- `get_petition_decision(petition_decision_record_identifier: str, include_documents: bool = False) -> PetitionDecisionIdentifierResponseBag`

## Parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `petitionDecisionRecordIdentifier` | string | Yes | Petition decision record identifier (UUID format) | `6779f1be-0f3b-5775-b9d3-dcfdb83171c3` |
| `includeDocuments` | boolean | No | Include decision documents (query parameter) | `true` |

## Response Structure

Returns a `PetitionDecisionIdentifierResponseBag` object containing:
- `decision` - PetitionDecision object with decision details
- `documents` - List of documents (if include_documents=True)
- `request_identifier` - Unique request identifier

## Examples

### Basic Usage

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def get_decision():
    client = USPTOClient(api_key="your-api-key-here")
    
    decision = await client.get_petition_decision(
        "6779f1be-0f3b-5775-b9d3-dcfdb83171c3"
    )
    
    print(f"Decision Type: {decision.decision.decision_type_code_description_text}")
    print(f"Patent Number: {decision.decision.patent_number}")
    print(f"Decision Date: {decision.decision.decision_date}")
    
    await client.session.close()

asyncio.run(get_decision())
```

### Get Decision with Documents

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def get_decision_with_docs():
    client = USPTOClient(api_key="your-api-key-here")
    
    decision = await client.get_petition_decision(
        "6779f1be-0f3b-5775-b9d3-dcfdb83171c3",
        include_documents=True
    )
    
    print(f"Decision: {decision.decision.decision_type_code_description_text}")
    if hasattr(decision, 'documents') and decision.documents:
        print(f"Documents: {len(decision.documents)}")
    
    await client.session.close()

asyncio.run(get_decision_with_docs())
```

## Related Endpoints

- [Search](search.md) - Search for decisions
- [Search/Download](search-download.md) - Download search results
- [Petition Decisions Overview](index.md) - All petition decisions endpoints
