import os
from dotenv import load_dotenv
import pytest
import aiohttp
from uspto_odp.controller.uspto_odp_client import USPTOClient

# Load environment variables from .env if present
load_dotenv()

@pytest.mark.asyncio
async def test_search_patent_applications_get_real():
    """
    Integration test for search_patent_applications_get using real API.
    Tests basic search functionality with a specific application number.
    """
    api_key = os.environ.get("USPTO_API_KEY")
    if not api_key:
        pytest.skip("USPTO_API_KEY environment variable not set.")
    
    async with aiohttp.ClientSession() as session:
        client = USPTOClient(api_key=api_key, session=session)
        
        # Test 1: Search by application number
        result = await client.search_patent_applications_get(
            q="applicationNumberText:14412875"
        )
        
        assert result is not None
        assert "count" in result
        assert result["count"] > 0
        assert "patentFileWrapperDataBag" in result
        assert len(result["patentFileWrapperDataBag"]) > 0
        
        # Verify we got the correct application
        app_data = result["patentFileWrapperDataBag"][0]
        assert app_data["applicationNumberText"] == "14412875"
        
        print(f"✓ Found application {app_data['applicationNumberText']}")
        if "applicationMetaData" in app_data and "patentNumber" in app_data["applicationMetaData"]:
            print(f"  Patent Number: {app_data['applicationMetaData']['patentNumber']}")

@pytest.mark.asyncio
async def test_search_patent_applications_get_with_pagination():
    """
    Integration test for GET search with pagination parameters.
    """
    api_key = os.environ.get("USPTO_API_KEY")
    if not api_key:
        pytest.skip("USPTO_API_KEY environment variable not set.")

    async with aiohttp.ClientSession() as session:
        client = USPTOClient(api_key=api_key, session=session)

        # Test with limit and offset
        result = await client.search_patent_applications_get(
            q="applicationMetaData.applicationTypeLabelName:Utility",
            limit=10,
            offset=0
        )

        assert result is not None
        assert "patentFileWrapperDataBag" in result
        # Note: The real API doesn't return a separate "pagination" object
        # It returns the data directly, and we verify the limit was respected
        assert len(result["patentFileWrapperDataBag"]) <= 10
        assert result["count"] > 0  # Should have a total count

        print(f"✓ Retrieved {len(result['patentFileWrapperDataBag'])} results with pagination (limit=10)")

@pytest.mark.asyncio
async def test_search_patent_applications_get_with_sorting():
    """
    Integration test for GET search with sorting.
    """
    api_key = os.environ.get("USPTO_API_KEY")
    if not api_key:
        pytest.skip("USPTO_API_KEY environment variable not set.")
    
    async with aiohttp.ClientSession() as session:
        client = USPTOClient(api_key=api_key, session=session)
        
        # Test with sorting by filing date
        result = await client.search_patent_applications_get(
            q="applicationMetaData.applicationTypeLabelName:Utility",
            sort="applicationMetaData.filingDate desc",
            limit=5
        )
        
        assert result is not None
        assert len(result["patentFileWrapperDataBag"]) > 0
        
        # Verify results are sorted (filing dates should be descending)
        filing_dates = []
        for app in result["patentFileWrapperDataBag"]:
            if "applicationMetaData" in app and "filingDate" in app["applicationMetaData"]:
                filing_dates.append(app["applicationMetaData"]["filingDate"])
        
        # Check if dates are in descending order
        if len(filing_dates) > 1:
            assert filing_dates == sorted(filing_dates, reverse=True), "Results should be sorted by filingDate desc"
        
        print(f"✓ Retrieved sorted results: {filing_dates[:3]}")

@pytest.mark.asyncio
async def test_search_patent_applications_get_with_fields():
    """
    Integration test for GET search with field selection.
    """
    api_key = os.environ.get("USPTO_API_KEY")
    if not api_key:
        pytest.skip("USPTO_API_KEY environment variable not set.")
    
    async with aiohttp.ClientSession() as session:
        client = USPTOClient(api_key=api_key, session=session)
        
        # Test with specific fields only
        result = await client.search_patent_applications_get(
            q="applicationNumberText:14412875",
            fields="applicationNumberText,applicationMetaData.patentNumber"
        )
        
        assert result is not None
        assert len(result["patentFileWrapperDataBag"]) > 0
        
        app_data = result["patentFileWrapperDataBag"][0]
        assert "applicationNumberText" in app_data
        
        print(f"✓ Retrieved limited fields for application {app_data['applicationNumberText']}")

@pytest.mark.asyncio  
async def test_search_patent_applications_get_no_params():
    """
    Integration test for GET search with no parameters (top 25 results).
    """
    api_key = os.environ.get("USPTO_API_KEY")
    if not api_key:
        pytest.skip("USPTO_API_KEY environment variable not set.")
    
    async with aiohttp.ClientSession() as session:
        client = USPTOClient(api_key=api_key, session=session)
        
        # Test with no parameters - should return top 25
        result = await client.search_patent_applications_get()
        
        assert result is not None
        assert "count" in result
        assert "patentFileWrapperDataBag" in result
        # Should return up to 25 results by default
        assert len(result["patentFileWrapperDataBag"]) <= 25
        
        print(f"✓ Retrieved {len(result['patentFileWrapperDataBag'])} results with no parameters")
