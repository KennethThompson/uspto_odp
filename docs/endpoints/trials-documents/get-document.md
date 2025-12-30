# Get Trial Document

## Overview

Retrieve a specific trial document by its document identifier.

## Endpoint Details

- **Method**: `GET`
- **URL**: `/api/v1/patent/trials/documents/{documentIdentifier}`
- **Authentication**: Required (API Key)

## Library Method

- `get_trial_document(document_identifier: str) -> TrialDocumentIdentifierResponseBag`

## Parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `documentIdentifier` | string | Yes | Document identifier (path parameter) | `document-id-123` |

## Examples

### Basic Usage

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def get_document():
    client = USPTOClient(api_key="your-api-key-here")
    
    document = await client.get_trial_document("document-id")
    
    print(f"Document Type: {document.document.document_type}")
    print(f"Document Name: {document.document.document_name}")
    
    await client.session.close()

asyncio.run(get_document())
```

## Related Endpoints

- [Search](search.md) - Search for documents
- [Get Documents by Trial](get-documents-by-trial.md) - Get all documents for a trial
