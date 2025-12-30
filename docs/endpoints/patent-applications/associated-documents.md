# Get Associated Documents

## Overview

Retrieve associated documents metadata for a patent application. This includes PGPub (Pre-Grant Publication) and Grant document metadata.

## Endpoint Details

- **Method**: `GET`
- **URL**: `/api/v1/patent/applications/{applicationNumberText}/associated-documents`
- **Authentication**: Required (API Key)

## Library Method

- `get_associated_documents(serial_number: str) -> AssociatedDocumentsResponse`

## Parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `applicationNumberText` | string | Yes | Application serial number (path parameter) | `14412875` |

## Response Structure

Returns an `AssociatedDocumentsResponse` object containing:
- `application_number` - Application number
- `associated_documents` - ApplicationAssociatedDocuments object with:
  - `pgpub_files` - Pre-Grant Publication file metadata
  - `grant_files` - Grant file metadata
- `request_identifier` - Unique request identifier

## Examples

### Basic Usage

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def get_associated_documents():
    client = USPTOClient(api_key="your-api-key-here")
    
    docs = await client.get_associated_documents("14412875")
    
    print(f"Application: {docs.application_number}")
    
    # Access PGPub files
    if docs.associated_documents.pgpub_files:
        print("PGPub files:")
        for file in docs.associated_documents.pgpub_files:
            print(f"  {file.file_name}")
    
    # Access Grant files
    if docs.associated_documents.grant_files:
        print("Grant files:")
        for file in docs.associated_documents.grant_files:
            print(f"  {file.file_name}")
    
    await client.session.close()

asyncio.run(get_associated_documents())
```

## Related Endpoints

- [Documents](documents.md) - Get all application documents
- [Get Patent Wrapper](get-patent-wrapper.md) - Get complete application information
