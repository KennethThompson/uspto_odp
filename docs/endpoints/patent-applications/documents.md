# Get Patent Documents

## Overview

Retrieve a list of all documents associated with a patent application. This includes office actions, responses, amendments, and other documents.

## Endpoint Details

- **Method**: `GET`
- **URL**: `/api/v1/patent/applications/{applicationNumberText}/documents`
- **Authentication**: Required (API Key)

## Library Method

- `get_patent_documents(serial_number: str) -> PatentDocumentCollection`

## Parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `applicationNumberText` | string | Yes | Application serial number (path parameter) | `14412875` |

## Response Structure

Returns a `PatentDocumentCollection` object containing:
- `documents` - List of PatentDocument objects
- Each document includes:
  - `document_code` - Document code
  - `document_name` - Document name/description
  - `document_date` - Document date
  - `download_options` - Available download formats (PDF, MS_WORD, XML)

## Examples

### Basic Usage

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def get_documents():
    client = USPTOClient(api_key="your-api-key-here")
    
    documents = await client.get_patent_documents("14412875")
    
    print(f"Total documents: {len(documents.documents)}")
    for doc in documents.documents:
        print(f"{doc.document_code}: {doc.document_name}")
        print(f"  Date: {doc.document_date}")
        print(f"  Formats: {[opt.mime_type for opt in doc.download_options]}")
    
    await client.session.close()

asyncio.run(get_documents())
```

### Downloading a Document

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def download_document():
    client = USPTOClient(api_key="your-api-key-here")
    
    # Get documents
    documents = await client.get_patent_documents("14412875")
    
    # Download first document as PDF
    if documents.documents:
        doc = documents.documents[0]
        file_path = await client.download_document(
            doc,
            save_path="./downloads",
            mime_type="PDF"
        )
        print(f"Downloaded to: {file_path}")
    
    await client.session.close()

asyncio.run(download_document())
```

## Related Endpoints

- [Get Patent Wrapper](get-patent-wrapper.md) - Get complete application information
- [Associated Documents](associated-documents.md) - Get associated documents (PGPub/Grant)
