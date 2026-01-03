# Get Patent Documents

## Overview

Retrieve a list of all documents associated with a patent application. This includes office actions, responses, amendments, and other documents. You can filter documents by date range and document codes to narrow down results.

## Endpoint Details

- **Method**: `GET`
- **URL**: `/api/v1/patent/applications/{applicationNumberText}/documents`
- **Authentication**: Required (API Key)

## Library Method

- `get_patent_documents(serial_number: str, official_date_from: Optional[str] = None, official_date_to: Optional[str] = None, document_codes: Optional[str] = None) -> PatentDocumentCollection`

## Parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `applicationNumberText` | string | Yes | Application serial number (path parameter) | `14412875` |
| `officialDateFrom` | string | No | Filter documents by official date from. Format: `yyyy-MM-dd` | `2023-01-01` |
| `officialDateTo` | string | No | Filter documents by official date to. Format: `yyyy-MM-dd` | `2023-12-31` |
| `documentCodes` | string | No | Filter by document codes. Single code or comma-separated codes | `WFEE` or `SRFW,SRNT` |

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
        print(f"{doc.document_code}: {doc.document_description}")
        print(f"  Date: {doc.official_date}")
        print(f"  Formats: {[opt.mime_type for opt in doc.download_options]}")
    
    await client.session.close()

asyncio.run(get_documents())
```

### Filtering by Date Range

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def filter_by_date():
    client = USPTOClient(api_key="your-api-key-here")
    
    # Get documents within a specific date range
    documents = await client.get_patent_documents(
        "18571476",
        official_date_from="2023-01-01",
        official_date_to="2023-12-31"
    )
    
    print(f"Found {len(documents.documents)} documents in date range")
    for doc in documents.documents:
        print(f"{doc.document_code}: {doc.document_description} - {doc.official_date.date()}")
    
    await client.session.close()

asyncio.run(filter_by_date())
```

### Filtering by Document Codes

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def filter_by_codes():
    client = USPTOClient(api_key="your-api-key-here")
    
    # Get documents with specific document codes
    # Single code
    documents = await client.get_patent_documents(
        "18571476",
        document_codes="WFEE"
    )
    
    print(f"Found {len(documents.documents)} documents with code WFEE")
    
    # Multiple codes (comma-separated)
    documents = await client.get_patent_documents(
        "18571476",
        document_codes="SRFW,SRNT"
    )
    
    print(f"Found {len(documents.documents)} documents with codes SRFW or SRNT")
    
    await client.session.close()

asyncio.run(filter_by_codes())
```

### Combining Filters

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def combine_filters():
    client = USPTOClient(api_key="your-api-key-here")
    
    # Combine date range and document code filters
    documents = await client.get_patent_documents(
        "18571476",
        official_date_from="2023-01-01",
        official_date_to="2023-12-31",
        document_codes="WFEE,SRNT"
    )
    
    print(f"Found {len(documents.documents)} documents matching all criteria")
    for doc in documents.documents:
        print(f"{doc.document_code}: {doc.document_description} - {doc.official_date.date()}")
    
    await client.session.close()

asyncio.run(combine_filters())
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
