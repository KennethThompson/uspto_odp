"""
Integration tests for search endpoints.
Requires USPTO_API_KEY environment variable to be set.
"""
import pytest
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOClient, USPTOError


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_patent_applications_get_basic(client):
    """
    Integration test for search_patent_applications_get using real API.
    Tests basic search functionality with a specific application number.
    """
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


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_patent_applications_get_with_pagination(client):
    """
    Integration test for GET search with pagination parameters.
    """
    result = await client.search_patent_applications_get(
        q="applicationMetaData.applicationTypeLabelName:Utility",
        limit=10,
        offset=0
    )
    
    assert result is not None
    assert "patentFileWrapperDataBag" in result
    assert len(result["patentFileWrapperDataBag"]) <= 10
    assert result["count"] > 0
    
    print(f"✓ Retrieved {len(result['patentFileWrapperDataBag'])} results with pagination (limit=10)")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_patent_applications_get_with_sorting(client):
    """
    Integration test for GET search with sorting.
    """
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


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_patent_applications_get_with_fields(client):
    """
    Integration test for GET search with field selection.
    """
    result = await client.search_patent_applications_get(
        q="applicationNumberText:14412875",
        fields="applicationNumberText,applicationMetaData.patentNumber"
    )
    
    assert result is not None
    assert len(result["patentFileWrapperDataBag"]) > 0
    
    app_data = result["patentFileWrapperDataBag"][0]
    assert "applicationNumberText" in app_data
    
    print(f"✓ Retrieved limited fields for application {app_data['applicationNumberText']}")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_patent_applications_get_no_params(client):
    """
    Integration test for GET search with no parameters (top 25 results).
    """
    result = await client.search_patent_applications_get()
    
    assert result is not None
    assert "count" in result
    assert "patentFileWrapperDataBag" in result
    assert len(result["patentFileWrapperDataBag"]) <= 25
    
    print(f"✓ Retrieved {len(result['patentFileWrapperDataBag'])} results with no parameters")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_patent_applications_get_with_filters(client):
    """
    Integration test for GET search with filters.
    """
    result = await client.search_patent_applications_get(
        q="applicationMetaData.applicationTypeLabelName:Utility",
        filters="applicationMetaData.applicationTypeCode UTL",
        limit=5
    )
    
    assert result is not None
    assert len(result["patentFileWrapperDataBag"]) > 0
    
    # Verify all results match the filter
    for app in result["patentFileWrapperDataBag"]:
        if "applicationMetaData" in app and "applicationTypeCode" in app["applicationMetaData"]:
            assert app["applicationMetaData"]["applicationTypeCode"] == "UTL"
    
    print(f"✓ Retrieved filtered results: {len(result['patentFileWrapperDataBag'])} applications")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_patent_applications_get_with_range_filters(client):
    """
    Integration test for GET search with range filters.
    """
    result = await client.search_patent_applications_get(
        q="applicationMetaData.applicationTypeLabelName:Utility",
        range_filters="applicationMetaData.filingDate 2010-01-01:2015-01-01",
        limit=5
    )
    
    assert result is not None
    assert len(result["patentFileWrapperDataBag"]) > 0
    
    print(f"✓ Retrieved results with range filter: {len(result['patentFileWrapperDataBag'])} applications")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_patent_applications_get_with_facets(client):
    """
    Integration test for GET search with facets.
    """
    result = await client.search_patent_applications_get(
        q="applicationMetaData.applicationTypeLabelName:Utility",
        facets="applicationMetaData.applicationTypeCode",
        limit=5
    )
    
    assert result is not None
    assert "facets" in result or len(result["patentFileWrapperDataBag"]) > 0
    
    print(f"✓ Retrieved results with facets: {len(result.get('patentFileWrapperDataBag', []))} applications")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_patent_applications_post_method(client):
    """
    Integration test for POST search method with JSON payload.
    """
    payload = {
        "q": "applicationNumberText:14412875",
        "filters": [
            {
                "name": "applicationMetaData.applicationTypeLabelName",
                "value": ["Utility"]
            }
        ],
        "sort": [
            {
                "field": "applicationMetaData.filingDate",
                "order": "desc"
            }
        ],
        "pagination": {
            "offset": 0,
            "limit": 10
        },
        "fields": ["applicationNumberText", "applicationMetaData"]
    }
    
    result = await client.search_patent_applications(payload)
    
    assert result is not None
    assert "count" in result
    assert "patentFileWrapperDataBag" in result
    assert len(result["patentFileWrapperDataBag"]) > 0
    
    app_data = result["patentFileWrapperDataBag"][0]
    assert app_data["applicationNumberText"] == "14412875"
    
    print(f"✓ POST search successful: found {result['count']} results")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_patent_applications_inventor_query(client):
    """
    Test search by inventor name.
    """
    result = await client.search_patent_applications_get(
        q="applicationMetaData.inventorBag.inventorNameText:Smith",
        limit=5
    )
    
    assert result is not None
    assert result["count"] >= 0  # May be 0 if no results
    
    print(f"✓ Inventor search returned {result['count']} results")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_patent_applications_error_handling(client):
    """
    Test error handling for invalid search queries.
    """
    # Test with invalid field name
    with pytest.raises(USPTOError):
        await client.search_patent_applications_get(
            q="invalidField:value"
        )
    
    print("✓ Error handling works correctly for invalid queries")
