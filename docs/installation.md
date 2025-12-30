# Installation

## Prerequisites

- Python 3.9 or higher
- pip (Python package installer)

## Install from PyPI (Recommended)

The easiest way to install the USPTO ODP Python Client is using pip:

```bash
pip install uspto_odp
```

## Install from Source

If you want to install from the source code:

1. Clone the repository:
```bash
git clone https://github.com/KennethThompson/uspto_odp.git
cd uspto_odp
```

2. Install the package in development mode:
```bash
pip install -e .
```

## Development Installation

If you plan to contribute or modify the code, install with development dependencies:

```bash
pip install -e ".[dev]"
```

This includes:
- `pytest` - Testing framework
- `pytest-asyncio` - Async test support
- `coverage` - Code coverage tools
- `python-dotenv` - Environment variable management

## Documentation Dependencies

To build the documentation locally:

```bash
pip install -e ".[docs]"
```

This includes:
- `mkdocs` - Documentation generator
- `mkdocs-material` - Material theme
- `mkdocstrings[python]` - Python docstring parser

## Verify Installation

You can verify the installation by running:

```python
import uspto_odp
print(uspto_odp.__version__)
```

## API Key Required

Before using the library, you'll need to obtain an API key from the USPTO Developer Hub:

1. Visit [USPTO Developer Hub](https://developer.uspto.gov/)
2. Sign up for an account
3. Request an API key
4. Keep your API key secure and never commit it to version control

## Next Steps

- Read the [Quick Start Guide](quickstart.md) to begin using the library
- Check out [Examples](examples.md) for common use cases
- Review the [API Reference](api/client.md) for detailed method documentation
