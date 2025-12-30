# Contributing

Thank you for your interest in contributing to the USPTO ODP Python Client! This document provides guidelines and instructions for contributing.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/uspto_odp.git
   cd uspto_odp
   ```
3. **Install in development mode**:
   ```bash
   pip install -e ".[dev]"
   ```

## Development Setup

### Install Development Dependencies

```bash
pip install -e ".[dev]"
```

This installs:
- `pytest` - Testing framework
- `pytest-asyncio` - Async test support
- `coverage` - Code coverage tools
- `python-dotenv` - Environment variable management

### Running Tests

Run all tests:
```bash
pytest
```

Run only unit tests:
```bash
pytest tests/unit/
```

Run only integration tests (requires API key):
```bash
pytest tests/integration/ -m integration
```

Run with coverage:
```bash
pytest --cov=uspto_odp --cov-report=html
```

### Code Style

- Follow PEP 8 style guidelines
- Use type hints for all function signatures
- Write docstrings for all public methods and classes
- Keep line length to 100 characters or less

## Making Changes

### Branch Naming

Create a descriptive branch name:
- `feature/add-new-endpoint` - For new features
- `fix/error-handling-bug` - For bug fixes
- `docs/update-readme` - For documentation updates

### Commit Messages

Write clear, descriptive commit messages:
- Use present tense ("Add feature" not "Added feature")
- Keep the first line under 50 characters
- Add more details in the body if needed

Example:
```
Add support for new endpoint

Implements the /api/v1/patent/new-endpoint endpoint with
full unit and integration test coverage.
```

### Code Requirements

1. **Add Tests**: All new code must include tests
   - Unit tests for client methods
   - Integration tests for API calls (if applicable)

2. **Update Documentation**: 
   - Add docstrings to new methods
   - Update README.md if adding new features
   - Update API documentation

3. **Type Hints**: All functions must have type hints

4. **Error Handling**: Use `USPTOError` for API errors

## Pull Request Process

1. **Update Tests**: Ensure all tests pass
   ```bash
   pytest
   ```

2. **Update Documentation**: 
   - Update docstrings
   - Update README.md if needed
   - Update examples if applicable

3. **Check Coverage**: Ensure test coverage doesn't decrease
   ```bash
   pytest --cov=uspto_odp --cov-report=term-missing
   ```

4. **Create Pull Request**:
   - Provide a clear description of changes
   - Reference any related issues
   - Include examples if adding new features

## Testing Guidelines

### Unit Tests

- Test all code paths
- Mock external API calls
- Test error conditions
- Use descriptive test names

### Integration Tests

- Require `USPTO_API_KEY` environment variable
- Use real API calls (be mindful of rate limits)
- Mark with `@pytest.mark.integration`
- May be skipped if API key is not available

### Test Structure

```python
import pytest
from unittest.mock import AsyncMock, patch
from uspto_odp.controller.uspto_odp_client import USPTOClient

@pytest.mark.asyncio
async def test_method_name():
    """Test description."""
    client = USPTOClient(api_key="test-key")
    
    # Test implementation
    
    await client.session.close()
```

## Documentation

### Docstring Format

Use Google-style docstrings:

```python
async def method_name(self, param: str) -> ReturnType:
    """
    Brief description.
    
    Longer description if needed.
    
    Args:
        param: Parameter description.
    
    Returns:
        Return value description.
    
    Raises:
        USPTOError: When API request fails.
    """
```

### Updating Documentation

If adding new features:
1. Update method docstrings
2. Add examples to `docs/examples.md`
3. Update README.md if needed
4. API reference is auto-generated from docstrings

## Questions?

- Open an issue for questions or discussions
- Check existing issues for similar questions
- Review the codebase for examples

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Help others learn and grow

Thank you for contributing! 🎉
