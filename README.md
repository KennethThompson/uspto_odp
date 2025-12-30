<div style="display: flex; align-items: center;">
  <img src="https://github.com/user-attachments/assets/9e4277bc-ee25-4e69-99e0-00e6fb07a53f" alt="uspto_odp_python_logo" width="200" style="margin-right: 20px;">
  <h1>Python wrapper for the USPTO Open Data Portal (ODP)</h1>
 
</div>

Simple, lightweight python client library to support access to the USPTO Open Data Portal (ODP)


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
| `/api/v1/datasets/products/search` | GET | 🚧 None | - |
| `/api/v1/datasets/products/{productIdentifier}` | GET | 🚧 None | - |
| `/api/v1/datasets/products/files/{productIdentifier}/{fileName}` | GET | 🚧 None | - |

## Petition Decisions Endpoints

| Endpoint | API Methods | Support | Library Method |
|----------|-------------|---------|----------------|
| `/api/v1/petition/decisions/search` | GET, POST | 🚧 None | - |
| `/api/v1/petition/decisions/search/download` | GET, POST | 🚧 None | - |
| `/api/v1/petition/decisions/{petitionDecisionRecordIdentifier}` | GET | 🚧 None | - |

## PTAB Trials - Proceedings Endpoints

| Endpoint | API Methods | Support | Library Method |
|----------|-------------|---------|----------------|
| `/api/v1/patent/trials/proceedings/search` | GET, POST | 🚧 None | - |
| `/api/v1/patent/trials/proceedings/search/download` | GET, POST | 🚧 None | - |
| `/api/v1/patent/trials/proceedings/{trialNumber}` | GET | 🚧 None | - |

## PTAB Trials - Decisions Endpoints

| Endpoint | API Methods | Support | Library Method |
|----------|-------------|---------|----------------|
| `/api/v1/patent/trials/decisions/search` | GET, POST | 🚧 None | - |
| `/api/v1/patent/trials/decisions/search/download` | GET, POST | 🚧 None | - |
| `/api/v1/patent/trials/decisions/{documentIdentifier}` | GET | 🚧 None | - |
| `/api/v1/patent/trials/{trialNumber}/decisions` | GET | 🚧 None | - |

## PTAB Trials - Documents Endpoints

| Endpoint | API Methods | Support | Library Method |
|----------|-------------|---------|----------------|
| `/api/v1/patent/trials/documents/search` | GET, POST | 🚧 None | - |
| `/api/v1/patent/trials/documents/search/download` | GET, POST | 🚧 None | - |
| `/api/v1/patent/trials/documents/{documentIdentifier}` | GET | 🚧 None | - |
| `/api/v1/patent/trials/{trialNumber}/documents` | GET | 🚧 None | - |

## PTAB Appeals - Decisions Endpoints

| Endpoint | API Methods | Support | Library Method |
|----------|-------------|---------|----------------|
| `/api/v1/patent/appeals/decisions/search` | GET, POST | 🚧 None | - |
| `/api/v1/patent/appeals/decisions/search/download` | GET, POST | 🚧 None | - |
| `/api/v1/patent/appeals/decisions/{documentIdentifier}` | GET | 🚧 None | - |
| `/api/v1/patent/appeals/{appealNumber}/decisions` | GET | 🚧 None | - |

## PTAB Interferences - Decisions Endpoints

| Endpoint | API Methods | Support | Library Method |
|----------|-------------|---------|----------------|
| `/api/v1/patent/interferences/decisions/search` | GET, POST | 🚧 None | - |
| `/api/v1/patent/interferences/decisions/search/download` | GET, POST | 🚧 None | - |
| `/api/v1/patent/interferences/{interferenceNumber}/decisions` | GET | 🚧 None | - |
| `/api/v1/patent/interferences/decisions/{documentIdentifier}` | GET | 🚧 None | - |

## Coverage Summary
- **Total Methods Available**: 50
- **Fully Supported**: 15 (30%)
- **Partially Supported**: 0 (0%)
- **Not Supported**: 35 (70%)

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
To be completed at a later date.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
