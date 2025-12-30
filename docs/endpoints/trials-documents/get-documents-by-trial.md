# Get Documents by Trial

## Overview

Retrieve all documents for a specific trial proceeding.

## Endpoint Details

- **Method**: `GET`
- **URL**: `/api/v1/patent/trials/{trialNumber}/documents`
- **Authentication**: Required (API Key)

## Library Method

- `get_trial_documents_by_trial(trial_number: str) -> TrialDocumentByTrialResponseBag`

## Parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `trialNumber` | string | Yes | Trial number identifier (path parameter) | `IPR2020-00001` |

## Examples

### Basic Usage

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def get_documents_by_trial():
    client = USPTOClient(api_key="your-api-key-here")
    
    documents = await client.get_trial_documents_by_trial("IPR2020-00001")
    
    print(f"Found {len(documents.documents)} documents")
    for doc in documents.documents:
        print(f"{doc.document_type}: {doc.document_name}")
    
    await client.session.close()

asyncio.run(get_documents_by_trial())
```

## Related Endpoints

- [Get Trial Proceeding](../trials-proceedings/get-proceeding.md) - Get trial proceeding details
- [Get Document](get-document.md) - Get specific document
- [Trials Documents Overview](index.md) - All trials documents endpoints
