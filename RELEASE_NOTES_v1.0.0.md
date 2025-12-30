# Release v1.0.0

## 🎉 First Stable Release

This is the first stable release of the USPTO ODP Python Client library, providing comprehensive support for all 53 API endpoints available in the USPTO Open Data Portal.

## ✨ Key Features

- ✅ **100% API Coverage** - All 53 API methods fully supported
- 🚀 **Async/Await** - Built on `aiohttp` for high-performance async operations
- 📦 **Type Hints** - Full type annotations for better IDE support
- 🔒 **Error Handling** - Comprehensive error handling with custom exceptions
- 📚 **Well Documented** - Extensive docstrings, examples, and comprehensive documentation site
- 🧪 **Fully Tested** - Comprehensive unit and integration tests

## 📋 Supported Endpoints

### Patent Applications (12 endpoints)

All endpoints under `/api/v1/patent/applications`:

| Endpoint | Methods | Library Methods |
|----------|---------|-----------------|
| `/search` | GET, POST | `search_patent_applications_get()`, `search_patent_applications()` |
| `/search/download` | GET, POST | `search_patent_applications_download_get()`, `search_patent_applications_download()` |
| `/{appNumber}` | GET | `get_patent_wrapper()` |
| `/{appNumber}/meta-data` | GET | `get_app_metadata()`, `get_app_metadata_from_patent_number()` (convenience) |
| `/{appNumber}/adjustment` | GET | `get_adjustment()` |
| `/{appNumber}/assignment` | GET | `get_patent_assignments()` |
| `/{appNumber}/attorney` | GET | `get_attorney()` |
| `/{appNumber}/continuity` | GET | `get_continuity()` |
| `/{appNumber}/foreign-priority` | GET | `get_foreign_priority()` |
| `/{appNumber}/transactions` | GET | `get_patent_transactions()` |
| `/{appNumber}/documents` | GET | `get_patent_documents()` |
| `/{appNumber}/associated-documents` | GET | `get_associated_documents()` |

### Status Codes (1 endpoint)

| Endpoint | Methods | Library Methods |
|----------|---------|-----------------|
| `/api/v1/patent/status-codes` | GET, POST | `search_status_codes_get()`, `search_status_codes()` |

### Bulk Datasets (3 endpoints)

All endpoints under `/api/v1/datasets/products`:

| Endpoint | Methods | Library Methods |
|----------|---------|-----------------|
| `/search` | GET | `search_dataset_products_get()` |
| `/{productIdentifier}` | GET | `get_dataset_product()` |
| `/files/{productIdentifier}/{fileName}` | GET | `get_dataset_file()` |

### Petition Decisions (3 endpoints)

All endpoints under `/api/v1/petition/decisions`:

| Endpoint | Methods | Library Methods |
|----------|---------|-----------------|
| `/search` | GET, POST | `search_petition_decisions_get()`, `search_petition_decisions()` |
| `/search/download` | GET, POST | `search_petition_decisions_download_get()`, `search_petition_decisions_download()` |
| `/{petitionDecisionRecordIdentifier}` | GET | `get_petition_decision()` |

### PTAB Trials - Proceedings (3 endpoints)

All endpoints under `/api/v1/patent/trials/proceedings`:

| Endpoint | Methods | Library Methods |
|----------|---------|-----------------|
| `/search` | GET, POST | `search_trial_proceedings_get()`, `search_trial_proceedings()` |
| `/search/download` | GET, POST | `search_trial_proceedings_download_get()`, `search_trial_proceedings_download()` |
| `/{trialNumber}` | GET | `get_trial_proceeding()` |

### PTAB Trials - Decisions (4 endpoints)

All endpoints under `/api/v1/patent/trials/decisions`:

| Endpoint | Methods | Library Methods |
|----------|---------|-----------------|
| `/search` | GET, POST | `search_trial_decisions_get()`, `search_trial_decisions()` |
| `/search/download` | GET, POST | `search_trial_decisions_download_get()`, `search_trial_decisions_download()` |
| `/{documentIdentifier}` | GET | `get_trial_decision()` |
| `/{trialNumber}/decisions` | GET | `get_trial_decisions_by_trial()` |

### PTAB Trials - Documents (4 endpoints)

All endpoints under `/api/v1/patent/trials/documents`:

| Endpoint | Methods | Library Methods |
|----------|---------|-----------------|
| `/search` | GET, POST | `search_trial_documents_get()`, `search_trial_documents()` |
| `/search/download` | GET, POST | `search_trial_documents_download_get()`, `search_trial_documents_download()` |
| `/{documentIdentifier}` | GET | `get_trial_document()` |
| `/{trialNumber}/documents` | GET | `get_trial_documents_by_trial()` |

### PTAB Appeals - Decisions (4 endpoints)

All endpoints under `/api/v1/patent/appeals/decisions`:

| Endpoint | Methods | Library Methods |
|----------|---------|-----------------|
| `/search` | GET, POST | `search_appeal_decisions_get()`, `search_appeal_decisions()` |
| `/search/download` | GET, POST | `search_appeal_decisions_download_get()`, `search_appeal_decisions_download()` |
| `/{documentIdentifier}` | GET | `get_appeal_decision()` |
| `/{appealNumber}/decisions` | GET | `get_appeal_decisions_by_appeal()` |

### PTAB Interferences - Decisions (4 endpoints)

All endpoints under `/api/v1/patent/interferences/decisions`:

| Endpoint | Methods | Library Methods |
|----------|---------|-----------------|
| `/search` | GET, POST | `search_interference_decisions_get()`, `search_interference_decisions()` |
| `/search/download` | GET, POST | `search_interference_decisions_download_get()`, `search_interference_decisions_download()` |
| `/decisions/{documentIdentifier}` | GET | `get_interference_decision()` |
| `/{interferenceNumber}/decisions` | GET | `get_interference_decisions_by_interference()` |

## 📚 Documentation

Comprehensive documentation is available at: https://kenneththompson.github.io/uspto_odp/

The documentation includes:
- **Quick Start Guide** - Get up and running in minutes
- **Installation Instructions** - Detailed setup guide
- **Endpoint Documentation** - Detailed guides for all 38 endpoints with examples
- **API Reference** - Auto-generated API documentation
- **Examples** - Comprehensive code examples

## 🚀 Installation

```bash
pip install uspto_odp
```

## 📦 Requirements

- Python 3.9 or higher
- USPTO API Key ([Get one here](https://developer.uspto.gov/))

## 🔧 Dependencies

- `aiohttp>=3.11.7` - Async HTTP client
- `strenum>=0.4.10` - String enumeration support

## 🧪 Testing

The library includes comprehensive test coverage:
- Unit tests for all endpoints
- Integration tests (require API key)
- Test fixtures and utilities

Run tests:
```bash
# Unit tests
pytest tests/unit

# Integration tests (requires USPTO_API_KEY environment variable)
pytest tests/integration
```

## 📝 Usage Example

```python
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient

async def main():
    client = USPTOClient(api_key="your-api-key-here")
    
    # Search for patent applications
    results = await client.search_patent_applications_get(
        q="applicationNumberText:14412875"
    )
    
    # Get application metadata
    metadata = await client.get_app_metadata("14412875")
    
    print(f"Application: {metadata.application_number}")
    
    await client.session.close()

asyncio.run(main())
```

## 🔗 Links

- **Documentation**: https://kenneththompson.github.io/uspto_odp/
- **GitHub Repository**: https://github.com/KennethThompson/uspto_odp
- **Issue Tracker**: https://github.com/KennethThompson/uspto_odp/issues
- **USPTO Developer Hub**: https://developer.uspto.gov/
- **USPTO Open Data Portal**: https://data.uspto.gov/

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for details.

## 🙏 Acknowledgments

Built for the USPTO Open Data Portal community. Special thanks to the USPTO for providing comprehensive API access to patent data.
