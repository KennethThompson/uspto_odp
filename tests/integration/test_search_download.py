"""
Integration tests for search/download endpoint.
Requires USPTO_API_KEY environment variable to be set.
"""
import pytest
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOError


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_patent_applications_download_post_basic(client):
    """
    Test search_patent_applications_download POST method with basic search.
    """
    payload = {
        "q": "applicationNumberText:14412875",
        "pagination": {
            "offset": 0,
            "limit": 10
        }
    }
    
    result = await client.search_patent_applications_download(payload)
    
    assert result is not None
    assert hasattr(result, 'count')
    assert hasattr(result, 'patent_file_wrapper_data_bag')
    assert isinstance(result.count, int)
    assert isinstance(result.patent_file_wrapper_data_bag, list)
    assert result.count >= 0
    
    print(f"✓ Downloaded search results via POST")
    print(f"  Count: {result.count}")
    print(f"  Found {len(result.patent_file_wrapper_data_bag)} results")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_patent_applications_download_get_basic(client):
    """
    Test search_patent_applications_download_get GET method with basic query.
    """
    result = await client.search_patent_applications_download_get(
        q="applicationNumberText:14412875",
        format="json"
    )
    
    assert result is not None
    assert hasattr(result, 'count')
    assert hasattr(result, 'patent_file_wrapper_data_bag')
    assert isinstance(result.count, int)
    assert isinstance(result.patent_file_wrapper_data_bag, list)
    
    await asyncio.sleep(1)  # Rate limiting
    
    print(f"✓ Downloaded search results via GET (JSON)")
    print(f"  Count: {result.count}")
    print(f"  Found {len(result.patent_file_wrapper_data_bag)} results")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_patent_applications_download_get_csv_format(client):
    """
    Test search_patent_applications_download_get with CSV format.
    """
    result = await client.search_patent_applications_download_get(
        q="applicationNumberText:14412875",
        format="csv",
        limit=10
    )
    
    assert result is not None
    assert hasattr(result, 'count')
    # CSV format may return downloadUrl instead of data bag
    if result.download_url:
        assert isinstance(result.download_url, str)
        print(f"✓ CSV download URL: {result.download_url}")
    else:
        assert isinstance(result.patent_file_wrapper_data_bag, list)
    
    await asyncio.sleep(1)  # Rate limiting
    
    print(f"✓ Downloaded search results via GET (CSV)")
    print(f"  Count: {result.count}")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_patent_applications_download_get_with_pagination(client):
    """
    Test search_patent_applications_download_get with pagination.
    """
    result = await client.search_patent_applications_download_get(
        q="Utility",
        offset=0,
        limit=50,
        format="json"
    )
    
    assert result is not None
    assert result.count >= 0
    assert len(result.patent_file_wrapper_data_bag) <= 50
    
    await asyncio.sleep(1)  # Rate limiting
    
    print(f"✓ Downloaded search results with pagination")
    print(f"  Count: {result.count}")
    print(f"  Returned: {len(result.patent_file_wrapper_data_bag)} results")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_patent_applications_download_post_complex_query(client):
    """
    Test search_patent_applications_download POST method with complex query.
    """
    payload = {
        "q": "applicationMetaData.applicationTypeLabelName:Utility",
        "filters": [
            {
                "name": "applicationMetaData.applicationTypeCode",
                "value": ["UTL"]
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
            "limit": 25
        },
        "fields": ["applicationNumberText", "applicationMetaData.patentNumber"]
    }
    
    result = await client.search_patent_applications_download(payload)
    
    assert result is not None
    assert result.count >= 0
    
    await asyncio.sleep(1)  # Rate limiting
    
    print(f"✓ Downloaded search results with complex query")
    print(f"  Count: {result.count}")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_patent_applications_download_verify_structure(client):
    """
    Verify the structure of downloaded search results.
    """
    result = await client.search_patent_applications_download_get(
        q="applicationNumberText:14412875",
        format="json"
    )
    
    assert result is not None
    assert isinstance(result.count, int)
    assert isinstance(result.patent_file_wrapper_data_bag, list)
    
    if len(result.patent_file_wrapper_data_bag) > 0:
        first_result = result.patent_file_wrapper_data_bag[0]
        assert isinstance(first_result, dict)
        # Verify common fields exist
        if "applicationNumberText" in first_result:
            assert isinstance(first_result["applicationNumberText"], str)
    
    await asyncio.sleep(1)  # Rate limiting
    
    print(f"✓ Verified download response structure")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_patent_applications_download_error_handling(client):
    """
    Test error handling for invalid download requests.
    """
    # Test with invalid query
    with pytest.raises(USPTOError):
        await client.search_patent_applications_download_get(
            q="invalid:field:value",
            format="json"
        )
    
    await asyncio.sleep(1)  # Rate limiting
    
    print("✓ Error handling works correctly for invalid queries")
