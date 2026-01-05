import sys
print(f"Python Path: {sys.path}")
import pytest
from unittest.mock import Mock, AsyncMock
import aiohttp
from uspto_odp.controller.uspto_odp_client import USPTOClient, USPTOError
from uspto_odp.models.patent_file_wrapper import PatentFileWrapper
from uspto_odp.models.patent_metadata import ApplicationMetadataResponse
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
            assert isinstance(result1, ApplicationMetadataResponse)
            assert result1.application_number == "18085747"
            assert result1.metadata.docket_number == "06-1129-C5"
            assert result1.metadata.customer_number == 63710
            print(f"Found application number: {result1.application_number}, docket number: {result1.metadata.docket_number}")

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

            # All formats should return the same application number
            assert result1.application_number == result2.application_number == result3.application_number
    else:
        # Use mock testing
        print("No API key found, using mock testing")
        # Create mock client
        mock_session = Mock(spec=aiohttp.ClientSession)
        client = USPTOClient(api_key="test_api_key", session=mock_session)

        # Create mock response data for the search (to find application number)
        mock_search_response_data = {
            "count": 1,
            "patentFileWrapperDataBag": [{
                "applicationNumberText": "18085747",  # Application number found from patent search
                "applicationMetaData": {
                    "patentNumber": "11989999"
                }
            }],
            "requestIdentifier": "test-search-request-id"
        }

        # Create mock response data for the meta-data endpoint
        mock_metadata_response_data = {
            "count": 1,
            "patentFileWrapperDataBag": [{
                "applicationNumberText": "18085747",
                "applicationMetaData": {
                    "firstInventorToFileIndicator": "N",
                    "applicationStatusCode": 150,
                    "applicationTypeCode": "UTL",
                    "filingDate": "2023-01-15",
                    "firstInventorName": "Test Inventor",
                    "inventionTitle": "Test Patent Invention",
                    "patentNumber": "11989999",
                    "grantDate": "2024-01-15",
                    "docketNumber": "06-1129-C5",
                    "customerNumber": 63710
                }
            }],
            "requestIdentifier": "test-metadata-request-id"
        }

        # Create mock responses
        mock_search_response = Mock()
        mock_search_response.status = 200
        mock_search_response.json = AsyncMock(return_value=mock_search_response_data)

        mock_metadata_response = Mock()
        mock_metadata_response.status = 200
        mock_metadata_response.json = AsyncMock(return_value=mock_metadata_response_data)

        # Create async context manager mocks
        async_cm_search = AsyncMock()
        async_cm_search.__aenter__.return_value = mock_search_response
        mock_session.post.return_value = async_cm_search

        async_cm_metadata = AsyncMock()
        async_cm_metadata.__aenter__.return_value = mock_metadata_response
        mock_session.get.return_value = async_cm_metadata

        # Execute test with various patent number formats
        result1 = await client.get_app_metadata_from_patent_number("US11,989,999")
        result2 = await client.get_app_metadata_from_patent_number("11,989,999")
        result3 = await client.get_app_metadata_from_patent_number("11989999")

        # Assertions: check the ApplicationMetadataResponse object
        assert result1 is not None
        assert isinstance(result1, ApplicationMetadataResponse)
        assert result1.application_number == "18085747"
        assert result1.metadata.patent_number == "11989999"
        assert result1.metadata.docket_number == "06-1129-C5"
        assert result1.metadata.customer_number == 63710

        assert result2 is not None
        assert isinstance(result2, ApplicationMetadataResponse)
        assert result2.application_number == "18085747"

        assert result3 is not None
        assert isinstance(result3, ApplicationMetadataResponse)
        assert result3.application_number == "18085747"

        # Check that post was called 3 times (search) and get was called 3 times (meta-data)
        assert mock_session.post.call_count == 3
        assert mock_session.get.call_count == 3
        
        # Verify search payload
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
        
        # Verify meta-data endpoint URL
        get_args, get_kwargs = mock_session.get.call_args_list[0]
        assert "18085747" in get_args[0] or "18085747" in str(get_args[0])
        assert "meta-data" in get_args[0] or "meta-data" in str(get_args[0])

@pytest.mark.asyncio
async def test_get_app_metadata_success(client):
    """Test get_app_metadata method that calls the /meta-data endpoint directly"""
    client, mock_session = client
    
    # Create mock response data for the meta-data endpoint
    mock_response_data = {
        "count": 1,
        "patentFileWrapperDataBag": [{
            "applicationNumberText": "14412875",
            "applicationMetaData": {
                "firstInventorToFileIndicator": "Y",
                "applicationStatusCode": 161,
                "applicationTypeCode": "UTL",
                "filingDate": "2022-01-15",
                "firstInventorName": "John Doe",
                "inventionTitle": "Test Invention Title",
                "patentNumber": "12345678",
                "grantDate": "2023-01-15",
                "docketNumber": "TEST-001",
                "customerNumber": 12345,
                "groupArtUnitNumber": "1234",
                "examinerNameText": "Jane Examiner"
            }
        }],
        "requestIdentifier": "test-metadata-request-id"
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
    result = await client.get_app_metadata("14412875")
    
    # Assertions
    assert result is not None
    assert isinstance(result, ApplicationMetadataResponse)
    assert result.application_number == "14412875"
    assert result.metadata.application_status_code == 161
    assert result.metadata.invention_title == "Test Invention Title"
    assert result.metadata.patent_number == "12345678"
    assert result.metadata.docket_number == "TEST-001"
    assert result.metadata.customer_number == 12345
    assert result.request_identifier == "test-metadata-request-id"
    
    # Verify GET was called with correct URL
    assert mock_session.get.call_count == 1
    args, kwargs = mock_session.get.call_args_list[0]
    assert "14412875" in args[0] or "14412875" in str(args[0])
    assert "meta-data" in args[0] or "meta-data" in str(args[0])
    assert kwargs["headers"]["X-API-KEY"] == "test_api_key"

@pytest.mark.asyncio
async def test_get_app_metadata_not_found(client):
    """Test get_app_metadata method with non-existent application number"""
    client, mock_session = client
    
    # Create mock error response
    mock_error_data = {
        "code": 404,
        "error": "Not Found",
        "errorDetails": "No matching records found",
        "requestIdentifier": "test-error-id"
    }
    
    mock_response = Mock()
    mock_response.status = 404
    mock_response.json = AsyncMock(return_value=mock_error_data)
    
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = mock_response
    mock_session.get.return_value = async_cm
    
    # Execute test and expect USPTOError
    with pytest.raises(USPTOError) as exc_info:
        await client.get_app_metadata("99999999")
    
    assert exc_info.value.code == 404
    assert "Not Found" in str(exc_info.value)

@pytest.mark.asyncio
async def test_search_patent_applications_get_success(client):
    """Test GET /search endpoint with query parameters"""
    client, mock_session = client
    
    # Create mock response data (matching real API response format)
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

    # Create mock response data (matching real API response format)
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
    assert len(result["patentFileWrapperDataBag"]) == 1
    # The real API doesn't return pagination object, just the data
    assert "facets" in result
    
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

    # Create mock response data (matching real API response format)
    mock_response_data = {
        "count": 1000000,  # Total count in database
        "patentFileWrapperDataBag": [
            {"applicationNumberText": f"1000000{i}"} for i in range(25)
        ],
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
    assert result["count"] == 1000000  # Total count
    assert len(result["patentFileWrapperDataBag"]) == 25  # Default limit is 25

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


@pytest.mark.asyncio
async def test_search_patent_applications_get_by_docket_number(client):
    """Test GET /search endpoint with docket number query parameter"""
    client, mock_session = client
    
    # Create mock response data matching real API response format
    # Includes application 18571476 with docket number 3NG00003USU1
    mock_response_data = {
        "count": 2,
        "patentFileWrapperDataBag": [
            {
                "applicationNumberText": "18571476",
                "applicationMetaData": {
                    "docketNumber": "3NG00003USU1",
                    "patentNumber": None,
                    "inventionTitle": "SYSTEMS AND METHODS FOR ARCHIVAL OF DATA CAPTURES FROM A MOBILE COMMUNICATION NETWORK",
                    "applicationStatusCode": 41,
                    "applicationTypeCode": "UTL",
                    "applicationTypeLabelName": "Utility",
                    "filingDate": "2023-12-18",
                    "firstInventorName": "Kenneth Michael Thompson"
                }
            },
            {
                "applicationNumberText": "18571477",
                "applicationMetaData": {
                    "docketNumber": "3NG00003USU1",
                    "patentNumber": None,
                    "inventionTitle": "Another Application",
                    "applicationStatusCode": 40,
                    "applicationTypeCode": "UTL",
                    "applicationTypeLabelName": "Utility",
                    "filingDate": "2023-12-19"
                }
            }
        ],
        "requestIdentifier": "test-request-id-docket"
    }
    
    # Create mock response
    mock_response = Mock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value=mock_response_data)
    
    # Create async context manager mock
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = mock_response
    mock_session.get.return_value = async_cm
    
    # Execute test - search by docket number
    result = await client.search_patent_applications_get(
        q="applicationMetaData.docketNumber:3NG00003USU1",
        limit=100
    )
    
    # Assertions
    assert result is not None
    assert result["count"] == 2
    assert len(result["patentFileWrapperDataBag"]) == 2
    assert result["requestIdentifier"] == "test-request-id-docket"
    
    # Verify application 18571476 is in the results
    application_numbers = [
        app["applicationNumberText"] 
        for app in result["patentFileWrapperDataBag"]
    ]
    assert "18571476" in application_numbers
    
    # Find and verify the specific application entry
    app_18571476 = next(
        app for app in result["patentFileWrapperDataBag"] 
        if app["applicationNumberText"] == "18571476"
    )
    
    # Verify it has the expected docket number
    assert "applicationMetaData" in app_18571476
    assert "docketNumber" in app_18571476["applicationMetaData"]
    assert app_18571476["applicationMetaData"]["docketNumber"] == "3NG00003USU1"
    assert app_18571476["applicationNumberText"] == "18571476"
    
    # Verify API call was made with correct parameters
    mock_session.get.assert_called_once()
    call_args = mock_session.get.call_args
    assert call_args[0][0].endswith("/search")
    assert call_args[1]["params"]["q"] == "applicationMetaData.docketNumber:3NG00003USU1"
    assert call_args[1]["params"]["limit"] == 100
    mock_response.json.assert_called_once()


@pytest.mark.asyncio
async def test_search_patent_applications_post_complex_query(client):
    """Test POST /search endpoint with complex query including filters, rangeFilters, sort, fields, pagination, and facets"""
    client, mock_session = client
    
    # Create mock response data matching real API response format
    mock_response_data = {
        "count": 5,
        "patentFileWrapperDataBag": [
            {
                "applicationNumberText": "14412875",
                "correspondenceAddressBag": [],
                "applicationMetaData": {
                    "filingDate": "2014-12-31",
                    "applicationTypeLabelName": "Utility",
                    "applicationStatusDescriptionText": "Patented Case",
                    "grantDate": "2015-08-04",
                    "applicationStatusCode": 150
                }
            },
            {
                "applicationNumberText": "14412876",
                "correspondenceAddressBag": [],
                "applicationMetaData": {
                    "filingDate": "2014-12-30",
                    "applicationTypeLabelName": "Utility",
                    "applicationStatusDescriptionText": "Patented Case",
                    "grantDate": "2015-08-05",
                    "applicationStatusCode": 150
                }
            }
        ],
        "facets": {
            "applicationMetaData.applicationTypeLabelName": {
                "Utility": 5
            },
            "applicationMetaData.applicationStatusCode": {
                "150": 5
            }
        },
        "requestIdentifier": "test-request-id-complex"
    }
    
    # Create mock response
    mock_response = Mock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value=mock_response_data)
    
    # Create async context manager mock
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = mock_response
    mock_session.post.return_value = async_cm
    
    # Execute test - complex POST query
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
    
    # Assertions
    assert result is not None
    assert result["count"] == 5
    assert len(result["patentFileWrapperDataBag"]) == 2
    assert result["requestIdentifier"] == "test-request-id-complex"
    
    # Verify facets are present
    assert "facets" in result
    assert "applicationMetaData.applicationTypeLabelName" in result["facets"]
    assert "applicationMetaData.applicationStatusCode" in result["facets"]
    
    # Verify all results match filters
    for app in result["patentFileWrapperDataBag"]:
        assert "applicationMetaData" in app
        assert app["applicationMetaData"]["applicationTypeLabelName"] == "Utility"
        assert app["applicationMetaData"]["applicationStatusDescriptionText"] == "Patented Case"
        assert "filingDate" in app["applicationMetaData"]
        assert "applicationNumberText" in app
        assert "correspondenceAddressBag" in app
        
        # Verify grant date is within range
        if "grantDate" in app["applicationMetaData"]:
            grant_date = app["applicationMetaData"]["grantDate"]
            assert grant_date >= "2010-08-04" and grant_date <= "2022-08-04"
    
    # Verify results are sorted by filing date descending
    filing_dates = [
        app["applicationMetaData"]["filingDate"] 
        for app in result["patentFileWrapperDataBag"]
        if "filingDate" in app["applicationMetaData"]
    ]
    assert filing_dates == sorted(filing_dates, reverse=True), \
        "Results should be sorted by filingDate desc"
    
    # Verify API call was made with correct payload
    mock_session.post.assert_called_once()
    call_args = mock_session.post.call_args
    assert call_args[0][0].endswith("/search")
    assert call_args[1]["json"] == payload
    assert call_args[1]["headers"]["X-API-KEY"] == "test_api_key"
    assert call_args[1]["headers"]["accept"] == "application/json"
    mock_response.json.assert_called_once()
