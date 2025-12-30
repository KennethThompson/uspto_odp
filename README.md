<div style="display: flex; align-items: center;">
  <img src="https://github.com/user-attachments/assets/9e4277bc-ee25-4e69-99e0-00e6fb07a53f" alt="uspto_odp_python_logo" width="200" style="margin-right: 20px;">
  <h1>Python wrapper for the USPTO Open Data Portal (ODP)</h1>
 
</div>

Simple, lightweight python client library to support access to the USPTO Open Data Portal (ODP)

[![Documentation](https://img.shields.io/badge/docs-latest-blue)](https://kenneththompson.github.io/uspto_odp/)
[![PyPI version](https://badge.fury.io/py/uspto-odp.svg)](https://badge.fury.io/py/uspto-odp)


| Python Version | Build Status |
|---------------|--------------|
| 3.9 | ![Python 3.9](https://github.com/KennethThompson/uspto_odp/actions/workflows/python-package-conda.yml/badge.svg?branch=main&python-version=3.9) |
| 3.10 | ![Python 3.10](https://github.com/KennethThompson/uspto_odp/actions/workflows/python-package-conda.yml/badge.svg?branch=main&python-version=3.10) |
| 3.11 | ![Python 3.11](https://github.com/KennethThompson/uspto_odp/actions/workflows/python-package-conda.yml/badge.svg?branch=main&python-version=3.11) |
| 3.12 | ![Python 3.12](https://github.com/KennethThompson/uspto_odp/actions/workflows/python-package-conda.yml/badge.svg?branch=main&python-version=3.12) |
| 3.13 | ![Python 3.13](https://github.com/KennethThompson/uspto_odp/actions/workflows/python-package-conda.yml/badge.svg?branch=main&python-version=3.13) |

This library is designed to support access to the USPTO Open Data Portal (ODP) and is built on top of the USPTO API.

This library is not designed to be a full-featured ORM or database mapper. It is designed to be a simple, easy-to-use library for accessing the USPTO API with limited dependencies.

This library will seek to maintain backwards compatibility as much as possible as the ODP evolves.

Note: You must have an API key to use this library. You can learn more about how to get an API key at [getting-started](https://data.uspto.gov/apis/getting-started). For up-to-date USPTO information regarding the Open Data Portal, please visit [USPTO Open Data Portal](https://data.uspto.gov/).

# API Endpoint Support Status

## Patent Application Endpoints

| Endpoint | API Methods | Support | Library Method |
|----------|-------------|---------|----------------|
| `.../search` | GET, POST | ✅ GET, POST | `search_patent_applications()` (POST)<br>`search_patent_applications_get()` (GET) |
| `.../search/download` | GET, POST | ✅ GET, POST | `search_patent_applications_download()` (POST)<br>`search_patent_applications_download_get()` (GET) |
| `.../{appNumber}` | GET | ✅ GET | `get_patent_wrapper()` |
| `.../{appNumber}/meta-data` | GET | ✅ GET | `get_app_metadata()` (direct endpoint)<br>`get_app_metadata_from_patent_number()` (convenience: uses search + meta-data) |
| `.../{appNumber}/adjustment` | GET | ✅ GET | `get_adjustment()` |
| `.../{appNumber}/assignment` | GET | ✅ GET | `get_patent_assignments()` |
| `.../{appNumber}/attorney` | GET | ✅ GET | `get_attorney()` |
| `.../{appNumber}/continuity` | GET | ✅ GET | `get_continuity()` |
| `.../{appNumber}/foreign-priority` | GET | ✅ GET | `get_foreign_priority()` |
| `.../{appNumber}/transactions` | GET | ✅ GET | `get_patent_transactions()` |
| `.../{appNumber}/documents` | GET | ✅ GET | `get_patent_documents()` |
| `.../{appNumber}/associated-documents` | GET | ✅ GET | `get_associated_documents()` |

**Note:** All endpoints begin with `/api/v1/patent/applications`

**Additional Library Methods:**
- `get_app_metadata_from_patent_number()` - This is a convenience method (not a USPTO endpoint) that searches for an application number using a patent number, then calls the `/meta-data` endpoint. It uses the `/search` endpoint internally to find the application number before making the meta-data request.

## Other Patent Endpoints

| Endpoint | API Methods | Support | Library Method |
|----------|-------------|---------|----------------|
| `/api/v1/patent/status-codes` | GET, POST | ✅ GET, POST | `search_status_codes_get()` (GET)<br>`search_status_codes()` (POST) |

## Bulk Datasets Endpoints

| Endpoint | API Methods | Support | Library Method |
|----------|-------------|---------|----------------|
| `/api/v1/datasets/products/search` | GET | ✅ GET | `search_dataset_products_get()` |
| `/api/v1/datasets/products/{productIdentifier}` | GET | ✅ GET | `get_dataset_product()` |
| `/api/v1/datasets/products/files/{productIdentifier}/{fileName}` | GET | ✅ GET | `get_dataset_file()` |

## Petition Decisions Endpoints

| Endpoint | API Methods | Support | Library Method |
|----------|-------------|---------|----------------|
| `/api/v1/petition/decisions/search` | GET, POST | ✅ GET, POST | `search_petition_decisions()` (POST)<br>`search_petition_decisions_get()` (GET) |
| `/api/v1/petition/decisions/search/download` | GET, POST | ✅ GET, POST | `search_petition_decisions_download()` (POST)<br>`search_petition_decisions_download_get()` (GET) |
| `/api/v1/petition/decisions/{petitionDecisionRecordIdentifier}` | GET | ✅ GET | `get_petition_decision()` |

## PTAB Trials - Proceedings Endpoints

| Endpoint | API Methods | Support | Library Method |
|----------|-------------|---------|----------------|
| `/api/v1/patent/trials/proceedings/search` | GET, POST | ✅ GET, POST | `search_trial_proceedings()` (POST)<br>`search_trial_proceedings_get()` (GET) |
| `/api/v1/patent/trials/proceedings/search/download` | GET, POST | ✅ GET, POST | `search_trial_proceedings_download()` (POST)<br>`search_trial_proceedings_download_get()` (GET) |
| `/api/v1/patent/trials/proceedings/{trialNumber}` | GET | ✅ GET | `get_trial_proceeding()` |

## PTAB Trials - Decisions Endpoints

| Endpoint | API Methods | Support | Library Method |
|----------|-------------|---------|----------------|
| `/api/v1/patent/trials/decisions/search` | GET, POST | ✅ GET, POST | `search_trial_decisions()` (POST)<br>`search_trial_decisions_get()` (GET) |
| `/api/v1/patent/trials/decisions/search/download` | GET, POST | ✅ GET, POST | `search_trial_decisions_download()` (POST)<br>`search_trial_decisions_download_get()` (GET) |
| `/api/v1/patent/trials/decisions/{documentIdentifier}` | GET | ✅ GET | `get_trial_decision()` |
| `/api/v1/patent/trials/{trialNumber}/decisions` | GET | ✅ GET | `get_trial_decisions_by_trial()` |

## PTAB Trials - Documents Endpoints

| Endpoint | API Methods | Support | Library Method |
|----------|-------------|---------|----------------|
| `/api/v1/patent/trials/documents/search` | GET, POST | ✅ GET, POST | `search_trial_documents()` (POST)<br>`search_trial_documents_get()` (GET) |
| `/api/v1/patent/trials/documents/search/download` | GET, POST | ✅ GET, POST | `search_trial_documents_download()` (POST)<br>`search_trial_documents_download_get()` (GET) |
| `/api/v1/patent/trials/documents/{documentIdentifier}` | GET | ✅ GET | `get_trial_document()` |
| `/api/v1/patent/trials/{trialNumber}/documents` | GET | ✅ GET | `get_trial_documents_by_trial()` |

## PTAB Appeals - Decisions Endpoints

| Endpoint | API Methods | Support | Library Method |
|----------|-------------|---------|----------------|
| `/api/v1/patent/appeals/decisions/search` | GET, POST | ✅ GET, POST | `search_appeal_decisions()` (POST)<br>`search_appeal_decisions_get()` (GET) |
| `/api/v1/patent/appeals/decisions/search/download` | GET, POST | ✅ GET, POST | `search_appeal_decisions_download()` (POST)<br>`search_appeal_decisions_download_get()` (GET) |
| `/api/v1/patent/appeals/decisions/{documentIdentifier}` | GET | ✅ GET | `get_appeal_decision()` |
| `/api/v1/patent/appeals/{appealNumber}/decisions` | GET | ✅ GET | `get_appeal_decisions_by_appeal()` |

## PTAB Interferences - Decisions Endpoints

| Endpoint | API Methods | Support | Library Method |
|----------|-------------|---------|----------------|
| `/api/v1/patent/interferences/decisions/search` | GET, POST | ✅ GET, POST | `search_interference_decisions()` (POST)<br>`search_interference_decisions_get()` (GET) |
| `/api/v1/patent/interferences/decisions/search/download` | GET, POST | ✅ GET, POST | `search_interference_decisions_download()` (POST)<br>`search_interference_decisions_download_get()` (GET) |
| `/api/v1/patent/interferences/{interferenceNumber}/decisions` | GET | ✅ GET | `get_interference_decisions_by_interference()` |
| `/api/v1/patent/interferences/decisions/{documentIdentifier}` | GET | ✅ GET | `get_interference_decision()` |

## Coverage Summary
- **Total Methods Available**: 53
- **Fully Supported**: 53 (100%)
- **Partially Supported**: 0 (0%)
- **Not Supported**: 0 (0%)

## Legend
- ✅ Fully Implemented and Available
- ⚠️ Partially Supported (workaround implementation)
- 🚧 Planned for Future Implementation

**Note on Convenience Methods:**
Some library methods (like `get_app_metadata_from_patent_number()`) are convenience wrappers that combine multiple USPTO API calls. These are not direct USPTO endpoints but provide a simpler interface for common use cases. The implementation details are documented in the method docstrings.

## Installation

### Prerequisites
- Python 3.9 or higher
- pip (Python package installer)

### From PyPI (Recommended)
```bash
pip install uspto_odp
```

### From Source
1. Clone the repository:
```bash
git clone https://github.com/KennethThompson/uspto_odp.git
cd uspto_odp
```

2. Install the package in development mode:
```bash
pip install -e .
```

### Development Installation
If you plan to contribute or modify the code, install with development dependencies:
```bash
pip install -e ".[dev]"
```

### API Key Required
Before using the library, you'll need to obtain an API key from the USPTO Developer Hub. Visit [USPTO Developer Hub](https://developer.uspto.gov/) to request your API key.

### Verify Installation
You can verify the installation by running:
```python
import uspto_odp
print(uspto_odp.__version__)
```

## Usage

### Quick Example

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def main():
    # Initialize the client with your API key
    client = USPTOClient(api_key="your-api-key-here")
    
    # Search for patent applications
    results = await client.search_patent_applications_get(
        q="applicationNumberText:14412875"
    )
    
    # Get patent metadata
    metadata = await client.get_app_metadata("14412875")
    print(f"Application: {metadata.application_number}")
    
    # Clean up
    await client.session.close()

asyncio.run(main())
```

## Common Examples

Here are practical examples for the most common use cases:

### 1. Get Patent File Wrapper

Retrieve complete patent application information including inventors, title, events, and metadata:

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def get_file_wrapper():
    client = USPTOClient(api_key="your-api-key-here")
    
    # Get complete file wrapper for an application
    wrapper = await client.get_patent_wrapper("14412875")
    
    print(f"Application Number: {wrapper.application_number}")
    print(f"Title: {wrapper.title}")
    print(f"Inventors: {[inv.name for inv in wrapper.inventors]}")
    
    # Access application events/history
    for event in wrapper.events:
        print(f"Event: {event.event_code} - {event.event_description}")
    
    await client.session.close()

asyncio.run(get_file_wrapper())
```

### 2. Get Application Metadata

Retrieve essential application metadata including filing date, patent number, and status:

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def get_metadata():
    client = USPTOClient(api_key="your-api-key-here")
    
    # Get metadata by application number
    metadata = await client.get_app_metadata("14412875")
    
    print(f"Application Number: {metadata.application_number}")
    print(f"Filing Date: {metadata.metadata.filing_date}")
    print(f"Patent Number: {metadata.metadata.patent_number}")
    print(f"Application Type: {metadata.metadata.application_type}")
    print(f"Status: {metadata.metadata.status}")
    
    await client.session.close()

asyncio.run(get_metadata())
```

### 3. Search for Application Number Using Patent Number

Find an application serial number when you only have a patent number:

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def find_app_from_patent():
    client = USPTOClient(api_key="your-api-key-here")
    
    # Method 1: Use convenience method (recommended)
    # This searches for the app number and returns metadata
    metadata = await client.get_app_metadata_from_patent_number("9022434")
    
    if metadata:
        print(f"Found Application: {metadata.application_number}")
        print(f"Filing Date: {metadata.metadata.filing_date}")
    else:
        print("Patent number not found")
    
    # Method 2: Manual search approach
    # Search for applications with this patent number
    search_results = await client.search_patent_applications_get(
        q="applicationMetaData.patentNumber:9022434",
        limit=1
    )
    
    if search_results.get('totalNumFound', 0) > 0:
        app_data = search_results['patentFileWrapperDataBag'][0]
        app_number = app_data.get('applicationNumberText')
        print(f"Application Number: {app_number}")
        
        # Now get full metadata
        metadata = await client.get_app_metadata(app_number)
        print(f"Filing Date: {metadata.metadata.filing_date}")
    
    await client.session.close()

asyncio.run(find_app_from_patent())
```

### 4. Download a Patent Document

Retrieve and download documents from a patent application:

```python
import asyncio
import os
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def download_document():
    client = USPTOClient(api_key="your-api-key-here")
    
    # First, get the list of documents for an application
    app_number = "14412875"
    documents = await client.get_patent_documents(app_number)
    
    print(f"Found {len(documents.documents)} documents")
    
    # Create download directory
    download_dir = "./downloads"
    os.makedirs(download_dir, exist_ok=True)
    
    # Download the first document as PDF
    if documents.documents:
        doc = documents.documents[0]
        print(f"Downloading: {doc.document_code} - {doc.document_name}")
        
        # Download as PDF
        file_path = await client.download_document(
            document=doc,
            save_path=download_dir,
            mime_type="PDF"  # Options: "PDF", "MS_WORD", "XML"
        )
        
        print(f"Downloaded to: {file_path}")
        
        # Check available formats
        print("Available formats:")
        for option in doc.download_options:
            print(f"  - {option.mime_type}")
    
    await client.session.close()

asyncio.run(download_document())
```

### 5. Advanced Search Examples

Search for applications using various criteria:

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def advanced_search():
    client = USPTOClient(api_key="your-api-key-here")
    
    # Example 1: Search by inventor name
    results = await client.search_patent_applications_get(
        q="applicationMetaData.inventorBag.inventorNameText:Smith",
        limit=25
    )
    print(f"Found {results.get('totalNumFound', 0)} applications")
    
    # Example 2: Search with filters and date range
    results = await client.search_patent_applications_get(
        q="applicationMetaData.applicationTypeCode:UTL",
        filters="applicationMetaData.applicationTypeCode UTL",
        range_filters="applicationMetaData.filingDate 2020-01-01:2024-01-01",
        sort="applicationMetaData.filingDate desc",
        limit=50
    )
    print(f"Found {results.get('totalNumFound', 0)} utility applications")
    
    # Example 3: Search by patent number (to find application number)
    patent_number = "12345678"
    results = await client.search_patent_applications_get(
        q=f"applicationMetaData.patentNumber:{patent_number}",
        limit=1
    )
    
    if results.get('totalNumFound', 0) > 0:
        app_number = results['patentFileWrapperDataBag'][0].get('applicationNumberText')
        print(f"Patent {patent_number} corresponds to Application {app_number}")
    
    await client.session.close()

asyncio.run(advanced_search())
```

### Error Handling

Always handle errors appropriately:

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient, USPTOError

async def search_with_error_handling():
    client = USPTOClient(api_key="your-api-key-here")
    
    try:
        wrapper = await client.get_patent_wrapper("invalid-number")
    except USPTOError as e:
        if e.code == 404:
            print("Application not found")
        elif e.code == 403:
            print("Access forbidden - check your API key")
        elif e.code == 400:
            print(f"Bad request: {e.error_details}")
        else:
            print(f"Error {e.code}: {e.error}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        await client.session.close()

asyncio.run(search_with_error_handling())
```

### Documentation

For comprehensive documentation, examples, and API reference, visit:

**📚 [Full Documentation](https://kenneththompson.github.io/uspto_odp/)**

The documentation includes:
- [Quick Start Guide](https://kenneththompson.github.io/uspto_odp/quickstart/) - Get up and running quickly
- [Installation Guide](https://kenneththompson.github.io/uspto_odp/installation/) - Detailed setup instructions
- [Examples](https://kenneththompson.github.io/uspto_odp/examples/) - Comprehensive code examples
- [API Reference](https://kenneththompson.github.io/uspto_odp/api/client/) - Complete API documentation

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
