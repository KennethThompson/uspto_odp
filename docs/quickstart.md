# Quick Start Guide

This guide will help you get started with the USPTO ODP Python Client in just a few minutes.

## Basic Setup

### 1. Install the Library

```bash
pip install uspto_odp
```

### 2. Get Your API Key

Visit the [USPTO Developer Hub](https://developer.uspto.gov/) to obtain your API key.

### 3. Initialize the Client

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def main():
    # Create a client instance
    client = USPTOClient(api_key="your-api-key-here")
    
    # Your code here
    
    # Always close the session when done
    await client.session.close()

asyncio.run(main())
```

## Basic Examples

### Search Patent Applications

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def search_example():
    client = USPTOClient(api_key="your-api-key-here")
    
    # Search using GET method
    results = await client.search_patent_applications_get(
        q="applicationNumberText:14412875",
        limit=10
    )
    
    print(f"Found {results.get('totalNumFound', 0)} results")
    
    await client.session.close()

asyncio.run(search_example())
```

### Get Patent Metadata

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def metadata_example():
    client = USPTOClient(api_key="your-api-key-here")
    
    # Get metadata by application number
    metadata = await client.get_app_metadata("14412875")
    
    print(f"Application: {metadata.application_number}")
    print(f"Filing Date: {metadata.metadata.filing_date}")
    
    await client.session.close()

asyncio.run(metadata_example())
```

### Search with POST Method

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def post_search_example():
    client = USPTOClient(api_key="your-api-key-here")
    
    # Search using POST method with complex query
    payload = {
        "q": "applicationMetaData.patentNumber:12345678",
        "sort": "applicationMetaData.filingDate desc",
        "offset": 0,
        "limit": 25
    }
    
    results = await client.search_patent_applications(payload)
    
    print(f"Found {results.get('totalNumFound', 0)} results")
    
    await client.session.close()

asyncio.run(post_search_example())
```

## Error Handling

The library provides custom exceptions for better error handling:

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient, USPTOError

async def error_handling_example():
    client = USPTOClient(api_key="your-api-key-here")
    
    try:
        metadata = await client.get_app_metadata("invalid-number")
    except USPTOError as e:
        print(f"Error {e.code}: {e.error}")
        print(f"Details: {e.error_details}")
        if e.request_identifier:
            print(f"Request ID: {e.request_identifier}")
    finally:
        await client.session.close()

asyncio.run(error_handling_example())
```

## Using a Shared Session

For better performance when making multiple requests, reuse the same session:

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient
import aiohttp

async def shared_session_example():
    # Create a shared session
    async with aiohttp.ClientSession() as session:
        client = USPTOClient(api_key="your-api-key-here", session=session)
        
        # Make multiple requests
        metadata1 = await client.get_app_metadata("14412875")
        metadata2 = await client.get_app_metadata("14412876")
        
        print(f"App 1: {metadata1.application_number}")
        print(f"App 2: {metadata2.application_number}")
        
        # Session is automatically closed when exiting the context

asyncio.run(shared_session_example())
```

## Convenience Methods

The library provides convenience methods that combine multiple API calls:

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def convenience_example():
    client = USPTOClient(api_key="your-api-key-here")
    
    # Get metadata using patent number (searches for app number first)
    metadata = await client.get_app_metadata_from_patent_number("12345678")
    
    if metadata:
        print(f"Application: {metadata.application_number}")
    else:
        print("Patent number not found")
    
    await client.session.close()

asyncio.run(convenience_example())
```

## Next Steps

- Explore **[Endpoint Documentation](endpoints/patent-applications/index.md)** - Detailed guides for each endpoint with examples
- Check out [Examples](examples.md) for more comprehensive examples
- Review the [API Reference](api/client.md) for all available methods
- Read about [Contributing](contributing.md) if you want to help improve the library

### Browse Endpoints

Each endpoint category has comprehensive documentation:

- **[Patent Applications](endpoints/patent-applications/index.md)** - Search, metadata, documents, and more
- **[Status Codes](endpoints/status-codes/index.md)** - Look up status codes
- **[Bulk Datasets](endpoints/bulk-datasets/index.md)** - Access bulk data
- **[Petition Decisions](endpoints/petition-decisions/index.md)** - Petition decision records
- **[PTAB Endpoints](endpoints/trials-proceedings/index.md)** - Trials, appeals, and interferences
