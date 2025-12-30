"""
Shared fixtures for integration tests.
Integration tests require USPTO_API_KEY environment variable to be set.
"""
import os
import pytest
import aiohttp
from dotenv import load_dotenv
from uspto_odp.controller.uspto_odp_client import USPTOClient

# Load environment variables from .env if present
load_dotenv()


@pytest.fixture(scope="session")
def api_key():
    """
    Fixture that provides the USPTO API key from environment.
    Skips tests if API key is not set.
    """
    api_key = os.environ.get("USPTO_API_KEY")
    if not api_key or not api_key.strip():
        pytest.skip("USPTO_API_KEY environment variable not set. Skipping integration tests.")
    return api_key


@pytest.fixture
async def client(api_key):
    """
    Fixture that provides a USPTOClient instance with real aiohttp session.
    Automatically closes the session after the test.
    """
    session = aiohttp.ClientSession()
    client = USPTOClient(api_key=api_key, session=session)
    yield client
    await session.close()


@pytest.fixture
def known_application_numbers():
    """
    Fixture providing known valid application numbers for testing.
    """
    return {
        "utility": "14412875",
        "utility_2": "18382093",
        "pct": "PCTUS2004027676",
    }


@pytest.fixture
def known_patent_numbers():
    """
    Fixture providing known valid patent numbers for testing.
    """
    return {
        "with_prefix": "US11,989,999",
        "with_commas": "11,989,999",
        "plain": "11989999",
    }
