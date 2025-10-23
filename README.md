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

# Status of uspto_odp wrapper support for USPTO API endpoints

## Patent Application Endpoints

| Endpoint | Status | Library Method | Description |
|----------|---------|----------------|-------------|
| `POST /api/v1/patent/applications/search` | ✅ | `search_patent_applications()` | Search patent applications by supplying json payload |
| `POST /api/v1/patent/applications/search/download` | 🚧 | - | Download patent data search results |
| `GET /api/v1/patent/applications/{applicationNumberText}` | ✅ | `get_patent_wrapper()` | Patent application data for a provided application number |
| `GET /api/v1/patent/applications/{applicationNumberText}/meta-data` | ⚠️ | `get_app_metadata_from_patent_number()` | Get patent application metadata (via search workaround) |
| `GET /api/v1/patent/applications/{applicationNumberText}/adjustment` | 🚧 | - | Get patent term adjustment data for an application number |
| `GET /api/v1/patent/applications/{applicationNumberText}/assignment` | ✅ | `get_patent_assignments()` | Get patent assignment data for an application number |
| `GET /api/v1/patent/applications/{applicationNumberText}/attorney` | 🚧 | - | Get attorney/agent data for an application number |
| `GET /api/v1/patent/applications/{applicationNumberText}/continuity` | ✅ | `get_continuity()` | Get continuity data for an application number |
| `GET /api/v1/patent/applications/{applicationNumberText}/foreign-priority` | ✅ | `get_foreign_priority()` | Get foreign-priority data for an application number |
| `GET /api/v1/patent/applications/{applicationNumberText}/transactions` | ✅ | `get_patent_transactions()` | Get transaction data for an application number |
| `GET /api/v1/patent/applications/{applicationNumberText}/documents` | ✅ | `get_patent_documents()` | Documents details for an application number |
| `GET /api/v1/patent/applications/{applicationNumberText}/associated-documents` | 🚧 | - | Associated documents metadata for an application |
| `POST /api/v1/patent/applications/text-to-search` | 🚧 | - | Convert natural language text to search query |

## Other Endpoints

| Endpoint | Status | Library Method | Description |
|----------|---------|----------------|-------------|
| `GET /api/v1/patent/status-codes` | 🚧 | - | Get list of patent status codes |
| `POST /api/v1/datasets/products/search` | 🚧 | - | Search bulk datasets |
| `GET /api/v1/datasets/products/{productIdentifier}` | 🚧 | - | Get specific bulk dataset |
| `POST /api/v1/petition/decisions/search` | 🚧 | - | Search petition decisions |
| `POST /api/v1/petition/decisions/search/download` | 🚧 | - | Download petition decision search results |
| `GET /api/v1/petition/decisions/{petitionDecisionRecordIdentifier}` | 🚧 | - | Get specific petition decision |

## Coverage Summary
- **Total Endpoints**: 19
- **Fully Supported**: 7 (37%)
- **Partially Supported**: 1 (5%)
- **Not Yet Supported**: 11 (58%)

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
