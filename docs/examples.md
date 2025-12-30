# Examples

This page provides comprehensive examples for common use cases with the USPTO ODP Python Client.

## Table of Contents

- [Patent Application Search](#patent-application-search)
- [Getting Patent Information](#getting-patent-information)
- [Petition Decisions](#petition-decisions)
- [PTAB Trials](#ptab-trials)
- [Bulk Datasets](#bulk-datasets)
- [Error Handling](#error-handling)

## Patent Application Search

### Basic Search

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def basic_search():
    client = USPTOClient(api_key="your-api-key-here")
    
    results = await client.search_patent_applications_get(
        q="applicationNumberText:14412875"
    )
    
    print(f"Total results: {results.get('totalNumFound', 0)}")
    
    await client.session.close()

asyncio.run(basic_search())
```

### Advanced Search with Filters

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def advanced_search():
    client = USPTOClient(api_key="your-api-key-here")
    
    results = await client.search_patent_applications_get(
        q="applicationMetaData.patentNumber:12345678",
        sort="applicationMetaData.filingDate desc",
        offset=0,
        limit=50,
        facets="applicationMetaData.applicationTypeCode",
        fields="applicationNumberText,applicationMetaData.patentNumber",
        filters="applicationMetaData.applicationTypeCode UTL",
        range_filters="applicationMetaData.filingDate 2020-01-01:2024-01-01"
    )
    
    print(f"Found {results.get('totalNumFound', 0)} results")
    
    await client.session.close()

asyncio.run(advanced_search())
```

### Search with POST Method

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def post_search():
    client = USPTOClient(api_key="your-api-key-here")
    
    payload = {
        "q": "applicationMetaData.patentNumber:12345678",
        "sort": "applicationMetaData.filingDate desc",
        "offset": 0,
        "limit": 25,
        "facets": ["applicationMetaData.applicationTypeCode"],
        "fields": ["applicationNumberText", "applicationMetaData.patentNumber"]
    }
    
    results = await client.search_patent_applications(payload)
    
    print(f"Found {results.get('totalNumFound', 0)} results")
    
    await client.session.close()

asyncio.run(post_search())
```

## Getting Patent Information

### Get Patent File Wrapper

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def get_file_wrapper():
    client = USPTOClient(api_key="your-api-key-here")
    
    wrapper = await client.get_patent_wrapper("14412875")
    
    print(f"Application Number: {wrapper.application_number}")
    print(f"Title: {wrapper.title}")
    print(f"Inventors: {[inv.name for inv in wrapper.inventors]}")
    
    await client.session.close()

asyncio.run(get_file_wrapper())
```

### Get Patent Metadata

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def get_metadata():
    client = USPTOClient(api_key="your-api-key-here")
    
    metadata = await client.get_app_metadata("14412875")
    
    print(f"Application: {metadata.application_number}")
    print(f"Filing Date: {metadata.metadata.filing_date}")
    print(f"Patent Number: {metadata.metadata.patent_number}")
    
    await client.session.close()

asyncio.run(get_metadata())
```

### Get Metadata from Patent Number

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def get_metadata_from_patent():
    client = USPTOClient(api_key="your-api-key-here")
    
    # This convenience method searches for the app number first
    metadata = await client.get_app_metadata_from_patent_number("12345678")
    
    if metadata:
        print(f"Application: {metadata.application_number}")
        print(f"Filing Date: {metadata.metadata.filing_date}")
    else:
        print("Patent number not found")
    
    await client.session.close()

asyncio.run(get_metadata_from_patent())
```

### Get Patent Documents

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def get_documents():
    client = USPTOClient(api_key="your-api-key-here")
    
    documents = await client.get_patent_documents("14412875")
    
    print(f"Total documents: {len(documents.documents)}")
    for doc in documents.documents:
        print(f"- {doc.document_type}: {doc.document_name}")
    
    await client.session.close()

asyncio.run(get_documents())
```

### Get Patent Assignments

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def get_assignments():
    client = USPTOClient(api_key="your-api-key-here")
    
    assignments = await client.get_patent_assignments("14412875")
    
    print(f"Total assignments: {len(assignments.assignments)}")
    for assignment in assignments.assignments:
        print(f"Assignee: {assignment.assignee_name}")
    
    await client.session.close()

asyncio.run(get_assignments())
```

## Petition Decisions

### Search Petition Decisions

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def search_petitions():
    client = USPTOClient(api_key="your-api-key-here")
    
    results = await client.search_petition_decisions_get(
        q="patentNumber:12345678",
        limit=25
    )
    
    print(f"Found {results.total_num_found} petition decisions")
    
    await client.session.close()

asyncio.run(search_petitions())
```

### Get Specific Petition Decision

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def get_petition():
    client = USPTOClient(api_key="your-api-key-here")
    
    decision = await client.get_petition_decision("petition-id-here")
    
    print(f"Decision Type: {decision.decision.decision_type_code_description_text}")
    print(f"Decision Date: {decision.decision.decision_date}")
    
    await client.session.close()

asyncio.run(get_petition())
```

## PTAB Trials

### Search Trial Proceedings

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def search_trials():
    client = USPTOClient(api_key="your-api-key-here")
    
    results = await client.search_trial_proceedings_get(
        q="trialNumber:IPR2020-00001",
        limit=25
    )
    
    print(f"Found {results.total_num_found} trial proceedings")
    
    await client.session.close()

asyncio.run(search_trials())
```

### Get Trial Decisions

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def get_trial_decisions():
    client = USPTOClient(api_key="your-api-key-here")
    
    # Get decisions for a specific trial
    decisions = await client.get_trial_decisions_by_trial("IPR2020-00001")
    
    print(f"Found {len(decisions.decisions)} decisions")
    for decision in decisions.decisions:
        print(f"- {decision.document_type}: {decision.document_name}")
    
    await client.session.close()

asyncio.run(get_trial_decisions())
```

## Bulk Datasets

### Search Dataset Products

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def search_datasets():
    client = USPTOClient(api_key="your-api-key-here")
    
    results = await client.search_dataset_products_get(
        q="Patent",
        limit=25
    )
    
    print(f"Found {results.total_num_found} dataset products")
    for product in results.products:
        print(f"- {product.product_name}: {product.product_identifier}")
    
    await client.session.close()

asyncio.run(search_datasets())
```

### Get Dataset Product Details

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def get_dataset_product():
    client = USPTOClient(api_key="your-api-key-here")
    
    product = await client.get_dataset_product("product-identifier")
    
    print(f"Product: {product.product.product_name}")
    print(f"Description: {product.product.product_description}")
    print(f"File Count: {product.product.file_count}")
    
    await client.session.close()

asyncio.run(get_dataset_product())
```

## Error Handling

### Comprehensive Error Handling

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient, USPTOError

async def error_handling():
    client = USPTOClient(api_key="your-api-key-here")
    
    try:
        metadata = await client.get_app_metadata("invalid-number")
    except USPTOError as e:
        if e.code == 404:
            print("Application not found")
        elif e.code == 403:
            print("Access forbidden - check your API key")
        elif e.code == 400:
            print(f"Bad request: {e.error_details}")
        elif e.code == 500:
            print("Server error - try again later")
        else:
            print(f"Unexpected error {e.code}: {e.error}")
        
        if e.request_identifier:
            print(f"Request ID for support: {e.request_identifier}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        await client.session.close()

asyncio.run(error_handling())
```

### Retry Logic

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient, USPTOError
import time

async def retry_example():
    client = USPTOClient(api_key="your-api-key-here")
    
    max_retries = 3
    retry_delay = 1
    
    for attempt in range(max_retries):
        try:
            metadata = await client.get_app_metadata("14412875")
            print(f"Success: {metadata.application_number}")
            break
        except USPTOError as e:
            if e.code == 500 and attempt < max_retries - 1:
                print(f"Server error, retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
                retry_delay *= 2
            else:
                raise
    finally:
        await client.session.close()

asyncio.run(retry_example())
```

## Next Steps

- Review the [API Reference](api/client.md) for complete method documentation
- Check the [Quick Start Guide](quickstart.md) for basic usage
- Read [Contributing](contributing.md) if you want to contribute
