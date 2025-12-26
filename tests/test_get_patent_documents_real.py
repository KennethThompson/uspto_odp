import os
from dotenv import load_dotenv
import pytest
import aiohttp
from uspto_odp.controller.uspto_odp_client import USPTOClient

# Load environment variables from .env if present
load_dotenv()

@pytest.mark.asyncio
async def test_get_patent_documents_real():
    """
    Integration test for get_patent_documents using a real serial number.
    """
    api_key = os.environ.get("USPTO_API_KEY")
    if not api_key:
        pytest.skip("USPTO_API_KEY environment variable not set.")
    serial_number = "18382093"
    async with aiohttp.ClientSession() as session:
        client = USPTOClient(api_key=api_key, session=session)
        result = await client.get_patent_documents(serial_number)
        assert result is not None
        assert hasattr(result, 'documents')
        assert isinstance(result.documents, list)
        assert len(result.documents) > 0
        print(f"Found {len(result.documents)} documents for serial {serial_number}")
