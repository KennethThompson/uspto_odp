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
            
            # Test different formats of the same patent number
            result2 = await client.get_app_metadata_from_patent_number("11,989,999")
            result3 = await client.get_app_metadata_from_patent_number("11989999")
            result4 = await client.get_patent_wrapper("12760185")
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
        result1 = await client.get_app_number_from_patent_number("US11,989,999")
        result2 = await client.get_app_number_from_patent_number("11,989,999")
        result3 = await client.get_app_number_from_patent_number("11989999")
        
        # Assertions
        assert result1 == "11989999"
        assert result2 == "11989999"
        assert result3 == "11989999"
        
        # Verify the API was called with the correct payload (sanitized patent number)
        expected_payload = {
            "filters": {
                "applicationMetaData.patentNumber": "11989999"
            }
        }
        
        # Check that post was called 3 times (once for each test case)
        assert mock_session.post.call_count == 3
        
        # Check the payload for the first call
        args, kwargs = mock_session.post.call_args_list[0]
        assert kwargs["json"] == expected_payload
