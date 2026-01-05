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


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_patent_applications_by_docket_number(client):
    """
    Integration test for searching by docket number.
    Searches for docket number "3NG00003USU1" and verifies application 18571476 is in the results.
    """
    result = await client.search_patent_applications_get(
        q="applicationMetaData.docketNumber:3NG00003USU1",
        limit=100  # Increase limit to ensure we find the application
    )
    
    assert result is not None
    assert "count" in result
    assert "patentFileWrapperDataBag" in result
    assert result["count"] > 0, "Expected at least one result for docket number 3NG00003USU1"
    
    # Verify that application 18571476 is in the results
    application_numbers = [
        app["applicationNumberText"] 
        for app in result["patentFileWrapperDataBag"]
    ]
    
    assert "18571476" in application_numbers, \
        f"Application 18571476 not found in search results. Found applications: {application_numbers[:10]}"
    
    # Find the specific application entry
    app_18571476 = next(
        app for app in result["patentFileWrapperDataBag"] 
        if app["applicationNumberText"] == "18571476"
    )
    
    # Verify it has the expected docket number
    assert "applicationMetaData" in app_18571476
    assert "docketNumber" in app_18571476["applicationMetaData"]
    assert app_18571476["applicationMetaData"]["docketNumber"] == "3NG00003USU1"
    
    print(f"✓ Found application 18571476 with docket number 3NG00003USU1")
    print(f"  Total results: {result['count']}")
    print(f"  Applications found: {len(result['patentFileWrapperDataBag'])}")
    
    await asyncio.sleep(1)  # Rate limiting


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_patent_applications_by_docket_number_and_customer_number(client):
    """
    Integration test for searching by docket number prefix and customer number.
    Searches for docket numbers beginning with "3NG" AND customerNumber equal to 51886.
    Verifies application 18571476 is in the results.
    """
    result = await client.search_patent_applications_get(
        q="applicationMetaData.docketNumber:3NG* AND applicationMetaData.customerNumber:51886",
        limit=100  # Increase limit to ensure we find the application
    )
    
    assert result is not None
    assert "count" in result
    assert "patentFileWrapperDataBag" in result
    assert result["count"] > 0, \
        "Expected at least one result for docket number beginning with 3NG and customerNumber 51886"
    
    # Verify that application 18571476 is in the results
    application_numbers = [
        app["applicationNumberText"] 
        for app in result["patentFileWrapperDataBag"]
    ]
    
    assert "18571476" in application_numbers, \
        f"Application 18571476 not found in search results. Found applications: {application_numbers[:10]}"
    
    # Find the specific application entry
    app_18571476 = next(
        app for app in result["patentFileWrapperDataBag"] 
        if app["applicationNumberText"] == "18571476"
    )
    
    # Verify it has the expected docket number (should begin with 3NG)
    assert "applicationMetaData" in app_18571476
    assert "docketNumber" in app_18571476["applicationMetaData"]
    assert app_18571476["applicationMetaData"]["docketNumber"].startswith("3NG"), \
        f"Expected docket number to start with '3NG', got: {app_18571476['applicationMetaData']['docketNumber']}"
    
    # Verify it has the expected customer number
    assert "customerNumber" in app_18571476["applicationMetaData"]
    assert app_18571476["applicationMetaData"]["customerNumber"] == 51886, \
        f"Expected customerNumber 51886, got: {app_18571476['applicationMetaData']['customerNumber']}"
    
    print(f"✓ Found application 18571476 with docket number starting with '3NG' and customerNumber 51886")
    print(f"  Docket Number: {app_18571476['applicationMetaData']['docketNumber']}")
    print(f"  Customer Number: {app_18571476['applicationMetaData']['customerNumber']}")
    print(f"  Total results: {result['count']}")
    print(f"  Applications found: {len(result['patentFileWrapperDataBag'])}")
    
    await asyncio.sleep(1)  # Rate limiting


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_patent_applications_post_complex_query(client):
    """
    Integration test for POST search method with complex query including filters, rangeFilters,
    sort, fields, pagination, and facets.
    Searches for Utility applications with status "Patented Case" granted between 2010-08-04 and 2022-08-04.
    """
    payload = {
        "q": "applicationMetaData.applicationTypeLabelName:Utility",
        "filters": [
            {
                "name": "applicationMetaData.applicationStatusDescriptionText",
                "value": [
                    "Patented Case"
                ]
            }
        ],
        "rangeFilters": [
            {
                "field": "applicationMetaData.grantDate",
                "valueFrom": "2010-08-04",
                "valueTo": "2022-08-04"
            }
        ],
        "sort": [
            {
                "field": "applicationMetaData.filingDate",
                "order": "desc"
            }
        ],
        "fields": [
            "applicationNumberText",
            "correspondenceAddressBag",
            "applicationMetaData.filingDate"
        ],
        "pagination": {
            "offset": 0,
            "limit": 25
        },
        "facets": [
            "applicationMetaData.applicationTypeLabelName",
            "applicationMetaData.applicationStatusCode"
        ]
    }
    
    result = await client.search_patent_applications(payload)
    
    assert result is not None
    assert "count" in result
    assert "patentFileWrapperDataBag" in result
    assert result["count"] >= 0  # May be 0 if no results match
    
    # Verify pagination limit
    assert len(result["patentFileWrapperDataBag"]) <= 25
    
    # If we have results, verify structure and filters
    if len(result["patentFileWrapperDataBag"]) > 0:
        # Verify requested fields are included
        first_app = result["patentFileWrapperDataBag"][0]
        assert "applicationNumberText" in first_app
        assert "applicationMetaData" in first_app
        assert "filingDate" in first_app["applicationMetaData"]
        assert "correspondenceAddressBag" in first_app
        
        # Note: When fields are specified, only those fields are returned
        # So we can't verify applicationTypeLabelName or applicationStatusDescriptionText
        # as they weren't in the fields list. The filters are still applied server-side.
        
        # Verify results are sorted by filing date descending
        filing_dates = []
        for app in result["patentFileWrapperDataBag"]:
            if "applicationMetaData" in app and "filingDate" in app["applicationMetaData"]:
                filing_dates.append(app["applicationMetaData"]["filingDate"])
        
        if len(filing_dates) > 1:
            assert filing_dates == sorted(filing_dates, reverse=True), \
                "Results should be sorted by filingDate desc"
    
    # Verify facets are present if results exist
    if result["count"] > 0:
        assert "facets" in result, "Facets should be present in response"
    
    print(f"✓ POST complex query successful: found {result['count']} results")
    print(f"  Applications returned: {len(result['patentFileWrapperDataBag'])}")
    if "facets" in result:
        print(f"  Facets present: {list(result['facets'].keys())}")
    
    await asyncio.sleep(1)  # Rate limiting
