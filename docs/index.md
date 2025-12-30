# USPTO ODP Python Client

<div style="display: flex; align-items: center; margin-bottom: 2rem;">
  <img src="https://github.com/user-attachments/assets/9e4277bc-ee25-4e69-99e0-00e6fb07a53f" alt="uspto_odp_python_logo" width="200" style="margin-right: 20px;">
  <div>
    <h2 style="margin-top: 0;">Simple, lightweight Python client library</h2>
    <p style="margin-bottom: 0;">Access the USPTO Open Data Portal (ODP) API with ease</p>
  </div>
</div>

## Overview

The **USPTO ODP Python Client** is a simple, easy-to-use library for accessing the USPTO Open Data Portal API. This library provides a clean, async interface to interact with all available USPTO endpoints, including:

- **Patent Applications** - Search, metadata, documents, assignments, and more
- **Status Codes** - Query patent application status codes
- **Petition Decisions** - Access petition decision records
- **PTAB Trials** - Proceedings, decisions, and documents
- **PTAB Appeals** - Appeal decisions
- **PTAB Interferences** - Interference decisions
- **Bulk Datasets** - Search and download bulk dataset products

## Key Features

- ✅ **100% API Coverage** - All 53 API methods fully supported
- 🚀 **Async/Await** - Built on `aiohttp` for high-performance async operations
- 📦 **Type Hints** - Full type annotations for better IDE support
- 🔒 **Error Handling** - Comprehensive error handling with custom exceptions
- 📚 **Well Documented** - Extensive docstrings and examples
- 🧪 **Fully Tested** - Comprehensive unit and integration tests

## Quick Example

```python
import asyncio
from uspto_odp import USPTOClient

async def main():
    # Initialize the client
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

## Installation

```bash
pip install uspto_odp
```

For development:

```bash
pip install -e ".[dev]"
```

## Requirements

- Python 3.9 or higher
- USPTO API Key ([Get one here](https://developer.uspto.gov/))

## Documentation

- **[Quick Start Guide](quickstart.md)** - Get up and running quickly
- **[Installation Guide](installation.md)** - Detailed installation instructions
- **[Endpoint Documentation](endpoints/patent-applications/index.md)** - Comprehensive endpoint guides with detailed examples
- **[Examples](examples.md)** - Comprehensive code examples
- **[API Reference](api/client.md)** - Complete API documentation

### Endpoint Categories

Browse detailed documentation for each endpoint category:

- **[Patent Applications](endpoints/patent-applications/index.md)** - 12 endpoints for patent application data
- **[Status Codes](endpoints/status-codes/index.md)** - Status code lookup
- **[Bulk Datasets](endpoints/bulk-datasets/index.md)** - Access bulk data products
- **[Petition Decisions](endpoints/petition-decisions/index.md)** - Petition decision records
- **[PTAB Trials - Proceedings](endpoints/trials-proceedings/index.md)** - Trial proceeding information
- **[PTAB Trials - Decisions](endpoints/trials-decisions/index.md)** - Trial decision documents
- **[PTAB Trials - Documents](endpoints/trials-documents/index.md)** - Trial documents
- **[PTAB Appeals - Decisions](endpoints/appeals-decisions/index.md)** - Appeal decision documents
- **[PTAB Interferences - Decisions](endpoints/interferences-decisions/index.md)** - Interference decision documents

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/KennethThompson/uspto_odp/blob/main/LICENSE) file for details.

## Links

- [GitHub Repository](https://github.com/KennethThompson/uspto_odp)
- [Issue Tracker](https://github.com/KennethThompson/uspto_odp/issues)
- [USPTO Developer Hub](https://developer.uspto.gov/)
- [USPTO Open Data Portal](https://data.uspto.gov/)
