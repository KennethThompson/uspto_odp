import sys
print(f"Python Path: {sys.path}")
import pytest
from unittest.mock import Mock, AsyncMock
import aiohttp
from uspto_odp.controller.uspto_odp_client import USPTOClient, USPTOError
from uspto_odp.models.patent_file_wrapper import PatentFileWrapper
from datetime import date



@pytest.fixture
def client():
    api_key = "test_api_key"
    mock_session = Mock(spec=aiohttp.ClientSession)
    return USPTOClient(api_key=api_key, session=mock_session), mock_session

@pytest.mark.asyncio
async def test_get_patent_wrapper_success(client):
    client, mock_session = client
    
    # Create mock response data exactly matching USPTO API response
    mock_response_data = {
        "count": 1,
        "patentFileWrapperDataBag": [{
            "eventDataBag": [
                {
                    "eventCode": "EML_NTR",
                    "eventDescriptionText": "Email Notification",
                    "eventDate": "2024-05-01"
                },
                {
                    "eventCode": "MM327",
                    "eventDescriptionText": "Mail Miscellaneous Communication to Applicant",
                    "eventDate": "2024-05-01"
                }
                # ... other events omitted for brevity, but would be included in actual test
            ],
            "applicationMetaData": {
                "firstInventorToFileIndicator": "N",
                "applicationStatusCode": 161,
                "applicationTypeCode": "UTL",
                "entityStatusData": {
                    "businessEntityStatusCategory": "Small"
                },
                "filingDate": "2008-12-30",
                "class/subclass": "235/472.01",
                "nationalStageIndicator": False,
                "firstInventorName": "Kai-Yuan Tien",
                "cpcClassificationBag": [
                    "G06K7/10831",
                    "G06K7/10702",
                    "G06K7/10732"
                ],
                "effectiveFilingDate": "2008-12-30",
                "publicationDateBag": ["2009-04-30"],
                "publicationSequenceNumberBag": ["0108066"],
                "earliestPublicationDate": "2009-04-30",
                "applicationTypeLabelName": "Utility",
                "applicationStatusDate": "2012-08-27",
                "class": "235",
                "applicationTypeCategory": "REGULAR",
                "applicationStatusDescriptionText": "Abandoned  --  Failure to Respond to an Office Action",
                "customerNumber": 84956,
                "groupArtUnitNumber": "2887",
                "earliestPublicationNumber": "US20090108066A1",
                "inventionTitle": "OPTICAL SYSTEM FOR BARCODE SCANNER",
                "applicationConfirmationNumber": 8142,
                "examinerNameText": "STANFORD, CHRISTOPHER J",
                "subclass": "472.01",
                "publicationCategoryBag": ["Pre-Grant Publications - PGPub"],
                "docketNumber": "OP-100000929",
                "customerNumber": 84956
            },
            "applicationNumberText": "12345678",
            # ... other fields would be included in actual test
        }],
        "requestIdentifier": "9d955e40-8ae9-4b05-ab6f-17d02e74d943"
    }
    
    # Create mock response
    mock_response = Mock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value=mock_response_data)
    
    # Create async context manager mock
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = mock_response
    mock_session.get.return_value = async_cm
    
    # Execute test
    result = await client.get_patent_wrapper("12345678")
    
    # Assertions
    assert result is not None
    assert result.application_number == "12345678"
    assert result.metadata.first_inventor_name == "Kai-Yuan Tien"
    assert result.metadata.invention_title == "OPTICAL SYSTEM FOR BARCODE SCANNER"
    assert len(result.events) >= 2  # At least the two events we included
    assert result.events[0].event_code == "EML_NTR"
    assert result.events[0].event_date == date(2024, 5, 1)
    assert result.metadata.customer_number == 84956
    mock_session.get.assert_called_once()
    mock_response.json.assert_called_once()

@pytest.mark.asyncio
async def test_get_app_metadata_from_patent_number(monkeypatch):
    """
    Test the get_app_metadata_from_patent_number method.
    This test will make real API calls if USPTO_API_KEY environment variable exists,
    otherwise it will use mock testing.
    """
    import os
    import aiohttp
    from uspto_odp.controller.uspto_odp_client import USPTOClient
    
    # Check if API key is available
    api_key = os.environ.get("USPTO_API_KEY")
    use_real_api = api_key and api_key.strip() != ""
    
    if use_real_api:
        # Use real API
        import asyncio
        print("Using real USPTO API with provided API key")
        async with aiohttp.ClientSession() as session:
            client = USPTOClient(api_key=api_key, session=session)

            # Test with various patent number formats
            result1 = await client.get_app_metadata_from_patent_number("US11,989,999")

            # Assert we got a result
            assert result1 is not None
            assert result1.get('applicationNumberText') == "18085747"
            assert result1.get('applicationMetaData').get('docketNumber') == "06-1129-C5"
            assert result1.get('applicationMetaData').get('customerNumber') == 63710
            print(f"Found application number: {result1.get('applicationNumberText')}, docket number: {result1.get('applicationMetaData').get('docketNumber')}")

            # Add delay to avoid rate limiting
            await asyncio.sleep(1)

            # Test different formats of the same patent number
            result2 = await client.get_app_metadata_from_patent_number("11,989,999")
            await asyncio.sleep(1)
            result3 = await client.get_app_metadata_from_patent_number("11989999")
            await asyncio.sleep(1)
            result4 = await client.get_patent_wrapper("12760185")
            await asyncio.sleep(1)
            result5 = await client.get_patent_wrapper("PCTUS0630638")
            await asyncio.sleep(1)
            result6 = await client.get_patent_wrapper("PCTUS2015015859")
            await asyncio.sleep(1)
            result7 = await client.get_patent_wrapper("PCTUS200403971")
            pass

            # All formats should return the same result
            assert result1 == result2 == result3
    else:
        # Use mock testing
        print("No API key found, using mock testing")
        # Create mock client
        mock_session = Mock(spec=aiohttp.ClientSession)
        client = USPTOClient(api_key="test_api_key", session=mock_session)

        # Create mock response data for the patent US11,989,999
        mock_response_data = {
            "count": 1,
            "patentFileWrapperDataBag": [{
                "applicationNumberText": "11989999",  # This is what we expect to get back
                "applicationMetaData": {
                    "patentNumber": "11989999",
                    "inventionTitle": "Test Patent Invention",
                    "applicationStatusCode": 150,
                    "applicationStatusDescriptionText": "Patented Case"
                }
            }],
            "requestIdentifier": "test-request-id-123"
        }

        # Create mock response
        mock_response = Mock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value=mock_response_data)

        # Create async context manager mock
        async_cm = AsyncMock()
        async_cm.__aenter__.return_value = mock_response
        mock_session.post.return_value = async_cm

        # Execute test with various patent number formats
        result1 = await client.get_app_metadata_from_patent_number("US11,989,999")
        result2 = await client.get_app_metadata_from_patent_number("11,989,999")
        result3 = await client.get_app_metadata_from_patent_number("11989999")

        # Assertions: check the applicationNumberText in the returned dict
        assert result1["applicationNumberText"] == "11989999"
        assert result2["applicationNumberText"] == "11989999"
        assert result3["applicationNumberText"] == "11989999"

        # Check that post was called 3 times (once for each test case)
        assert mock_session.post.call_count == 3
        args, kwargs = mock_session.post.call_args_list[0]
        expected_payload = {
            "q" : "applicationMetaData.patentNumber:11989999",
            "filters": [
                {
                    "name": "applicationMetaData.applicationTypeLabelName",
                    "value": ["Utility"]
                },
                {
                    "name": "applicationMetaData.publicationCategoryBag",
                    "value": ["Granted/Issued"]
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
            "fields": ["applicationNumberText", "applicationMetaData"],
            "facets": [
                "applicationMetaData.applicationTypeLabelName"
            ]        
        }
        assert kwargs["json"] == expected_payload

@pytest.mark.asyncio
async def test_search_patent_applications_get_success(client):
    """Test GET /search endpoint with query parameters"""
    client, mock_session = client
    
    # Create mock response data
    mock_response_data = {
        "count": 2,
        "patentFileWrapperDataBag": [
            {
                "applicationNumberText": "14412875",
                "applicationMetaData": {
                    "patentNumber": "9022434",
                    "inventionTitle": "Test Patent 1",
                    "applicationStatusCode": 150,
                    "applicationTypeLabelName": "Utility"
                }
            },
            {
                "applicationNumberText": "14412876",
                "applicationMetaData": {
                    "patentNumber": "9022435",
                    "inventionTitle": "Test Patent 2",
                    "applicationStatusCode": 150,
                    "applicationTypeLabelName": "Utility"
                }
            }
        ],
        "pagination": {
            "offset": 0,
            "limit": 25,
            "total": 2
        },
        "requestIdentifier": "test-request-id"
    }
    
    # Create mock response
    mock_response = Mock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value=mock_response_data)
    
    # Create async context manager mock
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = mock_response
    mock_session.get.return_value = async_cm
    
    # Execute test - simple query
    result = await client.search_patent_applications_get(q="applicationNumberText:14412875")
    
    # Assertions
    assert result is not None
    assert result["count"] == 2
    assert len(result["patentFileWrapperDataBag"]) == 2
    assert result["patentFileWrapperDataBag"][0]["applicationNumberText"] == "14412875"
    
    # Verify API call was made with correct parameters
    mock_session.get.assert_called_once()
    call_args = mock_session.get.call_args
    assert call_args[0][0].endswith("/search")
    assert call_args[1]["params"]["q"] == "applicationNumberText:14412875"
    mock_response.json.assert_called_once()

@pytest.mark.asyncio
async def test_search_patent_applications_get_with_all_params(client):
    """Test GET /search endpoint with all query parameters"""
    client, mock_session = client
    
    # Create mock response data
    mock_response_data = {
        "count": 1,
        "patentFileWrapperDataBag": [
            {
                "applicationNumberText": "14412875",
                "applicationMetaData": {
                    "patentNumber": "9022434",
                    "filingDate": "2014-12-31"
                }
            }
        ],
        "facets": {
            "applicationMetaData.applicationTypeCode": {
                "UTL": 100,
                "DES": 50
            }
        },
        "pagination": {
            "offset": 10,
            "limit": 50,
            "total": 100
        },
        "requestIdentifier": "test-request-id"
    }
    
    # Create mock response
    mock_response = Mock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value=mock_response_data)
    
    # Create async context manager mock
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = mock_response
    mock_session.get.return_value = async_cm
    
    # Execute test - all parameters
    result = await client.search_patent_applications_get(
        q="applicationMetaData.inventorBag.inventorNameText:Smith",
        sort="applicationMetaData.filingDate desc",
        offset=10,
        limit=50,
        facets="applicationMetaData.applicationTypeCode,applicationMetaData.docketNumber",
        fields="applicationNumberText,applicationMetaData.patentNumber",
        filters="applicationMetaData.applicationTypeCode UTL",
        range_filters="applicationMetaData.grantDate 2010-01-01:2011-01-01"
    )
    
    # Assertions
    assert result is not None
    assert result["count"] == 1
    assert result["pagination"]["offset"] == 10
    assert result["pagination"]["limit"] == 50
    
    # Verify API call was made with all parameters
    mock_session.get.assert_called_once()
    call_args = mock_session.get.call_args
    params = call_args[1]["params"]
    
    assert params["q"] == "applicationMetaData.inventorBag.inventorNameText:Smith"
    assert params["sort"] == "applicationMetaData.filingDate desc"
    assert params["offset"] == 10
    assert params["limit"] == 50
    assert params["facets"] == "applicationMetaData.applicationTypeCode,applicationMetaData.docketNumber"
    assert params["fields"] == "applicationNumberText,applicationMetaData.patentNumber"
    assert params["filters"] == "applicationMetaData.applicationTypeCode UTL"
    assert params["rangeFilters"] == "applicationMetaData.grantDate 2010-01-01:2011-01-01"

@pytest.mark.asyncio
async def test_search_patent_applications_get_no_params(client):
    """Test GET /search endpoint with no parameters (returns top 25)"""
    client, mock_session = client
    
    # Create mock response data
    mock_response_data = {
        "count": 25,
        "patentFileWrapperDataBag": [
            {"applicationNumberText": f"1000000{i}"} for i in range(25)
        ],
        "pagination": {
            "offset": 0,
            "limit": 25,
            "total": 1000000
        },
        "requestIdentifier": "test-request-id"
    }
    
    # Create mock response
    mock_response = Mock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value=mock_response_data)
    
    # Create async context manager mock
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = mock_response
    mock_session.get.return_value = async_cm
    
    # Execute test - no parameters
    result = await client.search_patent_applications_get()
    
    # Assertions
    assert result is not None
    assert result["count"] == 25
    assert len(result["patentFileWrapperDataBag"]) == 25
    
    # Verify API call was made with empty params
    mock_session.get.assert_called_once()
    call_args = mock_session.get.call_args
    params = call_args[1]["params"]
    assert params == {}  # No parameters should be sent

@pytest.mark.asyncio
async def test_search_patent_applications_get_error_404(client):
    """Test GET /search endpoint error handling"""
    client, mock_session = client
    
    # Create error response
    mock_response = Mock()
    mock_response.status = 404
    mock_response.json = AsyncMock(return_value={
        "code": 404,
        "error": "Not Found",
        "errorDetails": "No matching records found",
        "requestIdentifier": "test-request-id"
    })
    
    # Create async context manager mock
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = mock_response
    mock_session.get.return_value = async_cm
    
    # Execute test - should raise USPTOError
    with pytest.raises(USPTOError) as exc_info:
        await client.search_patent_applications_get(q="nonexistent:12345")
    
    # Verify error details
    assert exc_info.value.code == 404
    assert exc_info.value.error == "Not Found"
    assert exc_info.value.error_details == "No matching records found"
    assert exc_info.value.request_identifier == "test-request-id"
