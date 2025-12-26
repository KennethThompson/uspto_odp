<div style="display: flex; align-items: center;">
  <img src="https://github.com/user-attachments/assets/9e4277bc-ee25-4e69-99e0-00e6fb07a53f" alt="uspto_odp_python_logo" width="200" style="margin-right: 20px;">
  <h1>Python wrapper for the Beta USPTO Open Data Portal (ODP)</h1>
 
</div>

Simple, lightweight python client library to support access to the USPTO Open Data Portal (ODP)


| Python Version | Build Status |
|---------------|--------------|
| 3.9 | ![Python 3.9](https://github.com/KennethThompson/uspto_odp/actions/workflows/python-package-conda.yml/badge.svg?branch=main&python-version=3.9) |
| 3.10 | ![Python 3.10](https://github.com/KennethThompson/uspto_odp/actions/workflows/python-package-conda.yml/badge.svg?branch=main&python-version=3.10) |
| 3.11 | ![Python 3.11](https://github.com/KennethThompson/uspto_odp/actions/workflows/python-package-conda.yml/badge.svg?branch=main&python-version=3.11) |
| 3.12 | ![Python 3.12](https://github.com/KennethThompson/uspto_odp/actions/workflows/python-package-conda.yml/badge.svg?branch=main&python-version=3.12) |
| 3.13 | ![Python 3.13](https://github.com/KennethThompson/uspto_odp/actions/workflows/python-package-conda.yml/badge.svg?branch=main&python-version=3.13) |

From the USPTO as of November 27, 2024:
"The new Open Data Portal (ODP) is launching soon, informed by the Developer Hub (Open Data Portal beta) and real customer feedback. The first iteration will include patent data and improved functionality previously found on Patent Examination Data System (PEDS)."

This library is designed to support access to the ODP and is built on top of the existing USPTO Developer Hub API.

This library is not designed to be a full-featured ORM or database mapper. It is designed to be a simple, easy-to-use library for accessing the USPTO API with limited dependencies.

Currently, the ODP is in beta and this library is subject to change as the API evolves.

However, this library will seek to maintain backwards compatibility as much as possible as the ODP evolves.

Note: You must have an API key to use this library. You can learn more about how to get an API key at [getting-started](https://beta-data.uspto.gov/apis/getting-started). For up-to-date USPTO information regarding the Open Data Portal, please visit [USPTO Open Data Portal](https://data.uspto.gov/).

# API Endpoint Support Status

## Patent Application Endpoints

| Endpoint | API Methods | Support | Library Method |
|----------|-------------|---------|----------------|
| `.../search` | GET, POST | ✅ GET, POST | `search_patent_applications()` (POST)<br>`search_patent_applications_get()` (GET) |
| `.../search/download` | GET, POST | 🚧 None | - |
| `.../{appNumber}` | GET | ✅ GET | `get_patent_wrapper()` |
| `.../{appNumber}/meta-data` | GET | ⚠️ Workaround | `get_app_metadata_from_patent_number()` |
| `.../{appNumber}/adjustment` | GET | 🚧 None | - |
| `.../{appNumber}/assignment` | GET | ✅ GET | `get_patent_assignments()` |
| `.../{appNumber}/attorney` | GET | 🚧 None | - |
| `.../{appNumber}/continuity` | GET | ✅ GET | `get_continuity()` |
| `.../{appNumber}/foreign-priority` | GET | ✅ GET | `get_foreign_priority()` |
| `.../{appNumber}/transactions` | GET | ✅ GET | `get_patent_transactions()` |
| `.../{appNumber}/documents` | GET | ✅ GET | `get_patent_documents()` |
| `.../{appNumber}/associated-documents` | GET | 🚧 None | - |

**Note:** All endpoints begin with `/api/v1/patent/applications`

## Other Endpoints

| Endpoint | API Methods | Support | Library Method |
|----------|-------------|---------|----------------|
| `/api/v1/patent/status-codes` | GET, POST | 🚧 None | - |
| `/api/v1/datasets/products/search` | GET | 🚧 None | - |
| `/api/v1/datasets/products/{productId}` | GET | 🚧 None | - |
| `/api/v1/petition/decisions/search` | GET, POST | 🚧 None | - |
| `/api/v1/petition/decisions/search/download` | GET, POST | 🚧 None | - |
| `/api/v1/petition/decisions/{decisionId}` | GET | 🚧 None | - |

## Coverage Summary
- **Total Methods Available**: 24
- **Fully Supported**: 8 (33%)
- **Partially Supported**: 1 (4%)
- **Not Supported**: 15 (63%)

## Legend
- ✅ Fully Implemented and Available
- ⚠️ Partially Supported (workaround implementation)
- 🚧 Planned for Future Implementation

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
