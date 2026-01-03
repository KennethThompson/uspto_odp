import pytest
from unittest.mock import Mock, AsyncMock
import aiohttp
from datetime import datetime
from uspto_odp.controller.uspto_odp_client import USPTOClient, USPTOError

@pytest.fixture
def client():
    api_key = "test_api_key"
    mock_session = Mock(spec=aiohttp.ClientSession)
    return USPTOClient(api_key=api_key, session=mock_session), mock_session

@pytest.mark.asyncio
async def test_get_patent_documents_success(client):
    client, mock_session = client
    # Complete mock response data exactly matching USPTO API response
    mock_response_data = {
        "documentBag": [
            {
                "applicationNumberText": "12345678",
                "officialDate": "2012-01-18T00:00:00.000-0500",
                "documentIdentifier": "GXKRD3UXPXXIFW4",
                "documentCode": "SRNT",
                "documentCodeDescriptionText": "Examiner's search strategy and results",
                "directionCategory": "INTERNAL",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://data.uspto.gov/api/v1/download/applications/12345678/GXKRD3UXPXXIFW4.pdf",
                        "pageTotalQuantity": 1
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2022-01-08T11:27:23.000-0500",
                "documentIdentifier": "KYABUKWLLDFLYX5",
                "documentCode": "OATH",
                "documentCodeDescriptionText": "Oath or Declaration filed",
                "directionCategory": "INCOMING",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://data.uspto.gov/api/v1/download/applications/12345678/KYABUKWLLDFLYX5.pdf",
                        "pageTotalQuantity": 3
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2008-12-30T15:24:30.000-0500",
                "documentIdentifier": "IYKJN6P7RXEAPX0",
                "documentCode": "WFEE",
                "documentCodeDescriptionText": "Fee Worksheet (SB06)",
                "directionCategory": "INTERNAL",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://data.uspto.gov/api/v1/download/applications/12345678/IYKJN6P7RXEAPX0.pdf",
                        "pageTotalQuantity": 1
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2011-10-06T00:00:00.000-0400",
                "documentIdentifier": "GTGKYNCBPPOPPY2",
                "documentCode": "WFEE",
                "documentCodeDescriptionText": "Fee Worksheet (SB06)",
                "directionCategory": "INTERNAL",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://data.uspto.gov/api/v1/download/applications/12345678/GTGKYNCBPPOPPY2.pdf",
                        "pageTotalQuantity": 2
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2012-01-31T00:00:00.000-0500",
                "documentIdentifier": "GY2ZH85NPXXIFW4",
                "documentCode": "FWCLM",
                "documentCodeDescriptionText": "Index of Claims",
                "directionCategory": "INTERNAL",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://data.uspto.gov/api/v1/download/applications/12345678/GY2ZH85NPXXIFW4.pdf",
                        "pageTotalQuantity": 1
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2011-10-06T00:00:00.000-0400",
                "documentIdentifier": "GVSJ4PX7PXXIFW4",
                "documentCode": "WFEE",
                "documentCodeDescriptionText": "Fee Worksheet (SB06)",
                "directionCategory": "INTERNAL",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://data.uspto.gov/api/v1/download/applications/12345678/GVSJ4PX7PXXIFW4.pdf",
                        "pageTotalQuantity": 1
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2009-01-16T00:00:00.000-0500",
                "documentIdentifier": "FQ0SPLX2PPOPPY5",
                "documentCode": "APP.FILE.REC",
                "documentCodeDescriptionText": "Filing Receipt",
                "directionCategory": "OUTGOING",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://data.uspto.gov/api/v1/download/applications/12345678/FQ0SPLX2PPOPPY5.pdf",
                        "pageTotalQuantity": 3
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2011-07-27T00:00:00.000-0400",
                "documentIdentifier": "GQMFBYJSPPOPPY5",
                "documentCode": "SRNT",
                "documentCodeDescriptionText": "Examiner's search strategy and results",
                "directionCategory": "INTERNAL",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://data.uspto.gov/api/v1/download/applications/12345678/GQMFBYJSPPOPPY5.pdf",
                        "pageTotalQuantity": 1
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2017-08-10T17:00:24.000-0400",
                "documentIdentifier": "J66XGWQGRXEAPX1",
                "documentCode": "WFEE",
                "documentCodeDescriptionText": "Fee Worksheet (SB06)",
                "directionCategory": "INTERNAL",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://data.uspto.gov/api/v1/download/applications/12345678/J66XGWQGRXEAPX1.pdf",
                        "pageTotalQuantity": 2
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2020-11-01T15:40:16.000-0500",
                "documentIdentifier": "KH10C73GLDFLYX4",
                "documentCode": "SRNT",
                "documentCodeDescriptionText": "Examiner's search strategy and results",
                "directionCategory": "INTERNAL",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://data.uspto.gov/api/v1/download/applications/12345678/KH10C73GLDFLYX4.pdf",
                        "pageTotalQuantity": 1
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2012-01-31T00:00:00.000-0500",
                "documentIdentifier": "GY2ZH85XPXXIFW4",
                "documentCode": "SRNT",
                "documentCodeDescriptionText": "Examiner's search strategy and results",
                "directionCategory": "INTERNAL",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://data.uspto.gov/api/v1/download/applications/12345678/GY2ZH85XPXXIFW4.pdf",
                        "pageTotalQuantity": 2
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2016-07-26T14:25:16.000-0400",
                "documentIdentifier": "IR3SLP23RXEAPX2",
                "documentCode": "SRNT",
                "documentCodeDescriptionText": "Examiner's search strategy and results",
                "directionCategory": "INTERNAL",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://data.uspto.gov/api/v1/download/applications/12345678/IR3SLP23RXEAPX2.pdf",
                        "pageTotalQuantity": 1
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2021-01-22T06:29:54.000-0500",
                "documentIdentifier": "KK87CFKWDFLYX11",
                "documentCode": "SRNT",
                "documentCodeDescriptionText": "Examiner's search strategy and results",
                "directionCategory": "INTERNAL",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://data.uspto.gov/api/v1/download/applications/12345678/KK87CFKWDFLYX11.pdf",
                        "pageTotalQuantity": 1
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2011-12-07T00:00:00.000-0500",
                "documentIdentifier": "GVWJ4NMLPXXIFW4",
                "documentCode": "N570",
                "documentCodeDescriptionText": "Communication - Re:  Power of Attorney (PTOL-308)",
                "directionCategory": "OUTGOING",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://data.uspto.gov/api/v1/download/applications/12345678/GVWJ4NMLPXXIFW4.pdf",
                        "pageTotalQuantity": 1
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2011-11-23T00:00:00.000-0500",
                "documentIdentifier": "GVCL8UT2PXXIFW3",
                "documentCode": "PA..",
                "documentCodeDescriptionText": "Power of Attorney",
                "directionCategory": "INCOMING",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://data.uspto.gov/api/v1/download/applications/12345678/GVCL8UT2PXXIFW3.pdf",
                        "pageTotalQuantity": 1
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2020-05-23T00:00:00.000-0400",
                "documentIdentifier": "FPC9GG5LPPOPPY4",
                "documentCode": "CLM",
                "documentCodeDescriptionText": "Claims",
                "directionCategory": "INCOMING",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://data.uspto.gov/api/v1/download/applications/12345678/FPC9GG5LPPOPPY4.pdf",
                        "pageTotalQuantity": 2
                    },
                    {
                        "mimeTypeIdentifier": "XML",
                        "downloadUrl": "https://data.uspto.gov/api/v1/download/applications/12345678/FPC9GG5LPPOPPY4/xmlarchive"
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2012-08-28T00:00:00.000-0400",
                "documentIdentifier": "H6F7E14JPXXIFW4",
                "documentCode": "ABN",
                "documentCodeDescriptionText": "Abandonment",
                "directionCategory": "OUTGOING",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://beta-api.uspto.gov/api/v1/download/applications/12345678/H6F7E14JPXXIFW4.pdf",
                        "pageTotalQuantity": 2
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2022-08-16T14:37:57.000-0400",
                "documentIdentifier": "L6XYI566XBLUEX3",
                "documentCode": "OATH",
                "documentCodeDescriptionText": "Oath or Declaration filed",
                "directionCategory": "INCOMING",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://beta-api.uspto.gov/api/v1/download/applications/12345678/L6XYI566XBLUEX3.pdf",
                        "pageTotalQuantity": 4
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2001-08-22T00:00:00.000-0400",
                "documentIdentifier": "ITDBOKLGPXXIFW2",
                "documentCode": "DRW",
                "documentCodeDescriptionText": "Drawings-only black and white line drawings",
                "directionCategory": "INCOMING",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://beta-api.uspto.gov/api/v1/download/applications/12345678/ITDBOKLGPXXIFW2.pdf",
                        "pageTotalQuantity": 2
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2011-07-26T00:00:00.000-0400",
                "documentIdentifier": "GQKVNGOQPPOPPY5",
                "documentCode": "SRNT",
                "documentCodeDescriptionText": "Examiner's search strategy and results",
                "directionCategory": "INTERNAL",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://beta-api.uspto.gov/api/v1/download/applications/12345678/GQKVNGOQPPOPPY5.pdf",
                        "pageTotalQuantity": 1
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2021-02-11T08:43:35.000-0500",
                "documentIdentifier": "KL0WXDVDLDFLYX4",
                "documentCode": "SRNT",
                "documentCodeDescriptionText": "Examiner's search strategy and results",
                "directionCategory": "INTERNAL",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://beta-api.uspto.gov/api/v1/download/applications/12345678/KL0WXDVDLDFLYX4.pdf",
                        "pageTotalQuantity": 1
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2020-05-23T00:00:00.000-0400",
                "documentIdentifier": "HMMDFW7KPXXIFW2",
                "documentCode": "ADS",
                "documentCodeDescriptionText": "Application Data Sheet",
                "directionCategory": "INCOMING",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://beta-api.uspto.gov/api/v1/download/applications/12345678/HMMDFW7KPXXIFW2.pdf",
                        "pageTotalQuantity": 4
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2021-01-08T08:51:15.000-0500",
                "documentIdentifier": "KJPRO4GUDFLYX10",
                "documentCode": "SRNT",
                "documentCodeDescriptionText": "Examiner's search strategy and results",
                "directionCategory": "INTERNAL",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://beta-api.uspto.gov/api/v1/download/applications/12345678/KJPRO4GUDFLYX10.pdf",
                        "pageTotalQuantity": 1
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2008-12-30T00:00:00.000-0500",
                "documentIdentifier": "FQ9G44BZPPOPPY5",
                "documentCode": "WFEE",
                "documentCodeDescriptionText": "Fee Worksheet (SB06)",
                "directionCategory": "INTERNAL",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://beta-api.uspto.gov/api/v1/download/applications/12345678/FQ9G44BZPPOPPY5.pdf",
                        "pageTotalQuantity": 1
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2011-10-06T00:00:00.000-0400",
                "documentIdentifier": "GTGKYN2JPPOPPY2",
                "documentCode": "A...",
                "documentCodeDescriptionText": "Amendment/Request for Reconsideration-After Non-Final Rejection",
                "directionCategory": "INCOMING",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://beta-api.uspto.gov/api/v1/download/applications/12345678/GTGKYN2JPPOPPY2.pdf",
                        "pageTotalQuantity": 1
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2022-07-30T05:18:20.000-0400",
                "documentIdentifier": "L6BYWPA9GREENX3",
                "documentCode": "OATH",
                "documentCodeDescriptionText": "Oath or Declaration filed",
                "directionCategory": "INCOMING",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://beta-api.uspto.gov/api/v1/download/applications/12345678/L6BYWPA9GREENX3.pdf",
                        "pageTotalQuantity": 2
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2020-05-23T00:00:00.000-0400",
                "documentIdentifier": "FPC9GFZSPPOPPY4",
                "documentCode": "ABST",
                "documentCodeDescriptionText": "Abstract",
                "directionCategory": "INCOMING",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://beta-api.uspto.gov/api/v1/download/applications/12345678/FPC9GFZSPPOPPY4.pdf",
                        "pageTotalQuantity": 1
                    },
                    {
                        "mimeTypeIdentifier": "XML",
                        "downloadUrl": "https://beta-api.uspto.gov/api/v1/download/applications/12345678/FPC9GFZSPPOPPY4/xmlarchive"
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2020-11-28T07:46:16.000-0500",
                "documentIdentifier": "KI1OUSP0DFLYX11",
                "documentCode": "SRNT",
                "documentCodeDescriptionText": "Examiner's search strategy and results",
                "directionCategory": "INTERNAL",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://beta-api.uspto.gov/api/v1/download/applications/12345678/KI1OUSP0DFLYX11.pdf",
                        "pageTotalQuantity": 1
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2022-07-30T05:18:20.000-0400",
                "documentIdentifier": "L6BYWPITXBLUEX2",
                "documentCode": "OATH",
                "documentCodeDescriptionText": "Oath or Declaration filed",
                "directionCategory": "INCOMING",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://.uspto.gov/api/v1/download/applications/12345678/L6BYWPITXBLUEX2.pdf",
                        "pageTotalQuantity": 4
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2020-03-09T16:36:58.000-0400",
                "documentIdentifier": "K7KXF7BVRXEAPX3",
                "documentCode": "SRNT",
                "documentCodeDescriptionText": "Examiner's search strategy and results",
                "directionCategory": "INTERNAL",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://beta-api.uspto.gov/api/v1/download/applications/12345678/K7KXF7BVRXEAPX3.pdf",
                        "pageTotalQuantity": 1
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2012-01-31T00:00:00.000-0500",
                "documentIdentifier": "GY2ZH852PXXIFW4",
                "documentCode": "892",
                "documentCodeDescriptionText": "List of references cited by examiner",
                "directionCategory": "OUTGOING",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://beta-api.uspto.gov/api/v1/download/applications/12345678/GY2ZH852PXXIFW4.pdf",
                        "pageTotalQuantity": 1
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2017-06-19T15:26:26.000-0400",
                "documentIdentifier": "J44J7RJXRXEAPX3",
                "documentCode": "SRNT",
                "documentCodeDescriptionText": "Examiner's search strategy and results",
                "directionCategory": "INTERNAL",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://beta-api.uspto.gov/api/v1/download/applications/12345678/J44J7RJXRXEAPX3.pdf",
                        "pageTotalQuantity": 1
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2014-12-16T00:00:00.000-0500",
                "documentIdentifier": "I3RM8VKEPXXIFW4",
                "documentCode": "SRNT",
                "documentCodeDescriptionText": "Examiner's search strategy and results",
                "directionCategory": "INTERNAL",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://beta-api.uspto.gov/api/v1/download/applications/12345678/I3RM8VKEPXXIFW4.pdf",
                        "pageTotalQuantity": 1
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2011-05-06T00:00:00.000-0400",
                "documentIdentifier": "GNDGBKPQPPOPPY5",
                "documentCode": "SRFW",
                "documentCodeDescriptionText": "Search information including classification, databases and other search related notes",
                "directionCategory": "INTERNAL",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://beta-api.uspto.gov/api/v1/download/applications/12345678/GNDGBKPQPPOPPY5.pdf",
                        "pageTotalQuantity": 1
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2020-05-23T00:00:00.000-0400",
                "documentIdentifier": "FPC9GGFBPPOPPY4",
                "documentCode": "OATH",
                "documentCodeDescriptionText": "Oath or Declaration filed",
                "directionCategory": "INCOMING",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://beta-api.uspto.gov/api/v1/download/applications/12345678/FPC9GGFBPPOPPY4.pdf",
                        "pageTotalQuantity": 2
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2011-11-23T00:00:00.000-0500",
                "documentIdentifier": "GVO3AAHLPXXIFW1",
                "documentCode": "R3.73",
                "documentCodeDescriptionText": "Assignee showing of ownership per 37 CFR 3.73",
                "directionCategory": "INCOMING",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://beta-api.uspto.gov/api/v1/download/applications/12345678/GVO3AAHLPXXIFW1.pdf",
                        "pageTotalQuantity": 1
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2011-11-23T00:00:00.000-0500",
                "documentIdentifier": "GVCL8UUOPXXIFW3",
                "documentCode": "N417",
                "documentCodeDescriptionText": "Electronic Filing System Acknowledgment Receipt",
                "directionCategory": "OUTGOING",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://beta-api.uspto.gov/api/v1/download/applications/12345678/GVCL8UUOPXXIFW3.pdf",
                        "pageTotalQuantity": 2
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2021-02-06T08:17:33.000-0500",
                "documentIdentifier": "KKTQSMYTDFLYX11",
                "documentCode": "SRNT",
                "documentCodeDescriptionText": "Examiner's search strategy and results",
                "directionCategory": "INTERNAL",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://beta-api.uspto.gov/api/v1/download/applications/12345678/KKTQSMYTDFLYX11.pdf",
                        "pageTotalQuantity": 1
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2012-01-31T00:00:00.000-0500",
                "documentIdentifier": "GY2ZH85DPXXIFW4",
                "documentCode": "SRFW",
                "documentCodeDescriptionText": "Search information including classification, databases and other search related notes",
                "directionCategory": "INTERNAL",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://beta-api.uspto.gov/api/v1/download/applications/12345678/GY2ZH85DPXXIFW4.pdf",
                        "pageTotalQuantity": 1
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2011-05-06T00:00:00.000-0400",
                "documentIdentifier": "GNDGBKJYPPOPPY5",
                "documentCode": "CTNF",
                "documentCodeDescriptionText": "Non-Final Rejection",
                "directionCategory": "OUTGOING",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://beta-api.uspto.gov/api/v1/download/applications/12345678/GNDGBKJYPPOPPY5.pdf",
                        "pageTotalQuantity": 7
                    },
                    {
                        "mimeTypeIdentifier": "MS_WORD",
                        "downloadUrl": "https://beta-api.uspto.gov/api/v1/download/applications/12345678/GNDGBKJYPPOPPY5/files/Non-Final%20Rejection.DOC"
                    },
                    {
                        "mimeTypeIdentifier": "XML",
                        "downloadUrl": "https://beta-api.uspto.gov/api/v1/download/applications/12345678/GNDGBKJYPPOPPY5/xmlarchive"
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2011-07-20T00:00:00.000-0400",
                "documentIdentifier": "GQCI5ULOPPOPPY5",
                "documentCode": "SRNT",
                "documentCodeDescriptionText": "Examiner's search strategy and results",
                "directionCategory": "INTERNAL",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://beta-api.uspto.gov/api/v1/download/applications/12345678/GQCI5ULOPPOPPY5.pdf",
                        "pageTotalQuantity": 1
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2016-08-03T15:55:59.000-0400",
                "documentIdentifier": "IRFBD6B0RXEAPX0",
                "documentCode": "SRNT",
                "documentCodeDescriptionText": "Examiner's search strategy and results",
                "directionCategory": "INTERNAL",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://beta-api.uspto.gov/api/v1/download/applications/12345678/IRFBD6B0RXEAPX0.pdf",
                        "pageTotalQuantity": 1
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2024-05-01T00:00:00.000-0400",
                "documentIdentifier": "LVLCSJF0BLUEX10",
                "documentCode": "M327",
                "documentCodeDescriptionText": "Miscellaneous Communication to Applicant - No Action Count",
                "directionCategory": "OUTGOING",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://beta-api.uspto.gov/api/v1/download/applications/12345678/LVLCSJF0BLUEX10.pdf",
                        "pageTotalQuantity": 1
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2019-07-16T19:18:25.000-0400",
                "documentIdentifier": "JY7V9T3CRXEAPX5",
                "documentCode": "OATH",
                "documentCodeDescriptionText": "Oath or Declaration filed",
                "directionCategory": "INCOMING",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://beta-api.uspto.gov/api/v1/download/applications/12345678/JY7V9T3CRXEAPX5.pdf",
                        "pageTotalQuantity": 3
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2016-09-29T13:09:52.000-0400",
                "documentIdentifier": "ITOLJ3O9RXEAPX0",
                "documentCode": "SRNT",
                "documentCodeDescriptionText": "Examiner's search strategy and results",
                "directionCategory": "INTERNAL",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://beta-api.uspto.gov/api/v1/download/applications/12345678/ITOLJ3O9RXEAPX0.pdf",
                        "pageTotalQuantity": 1
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2020-06-06T06:07:10.000-0400",
                "documentIdentifier": "KB3H43ZIRXEAPX5",
                "documentCode": "SRNT",
                "documentCodeDescriptionText": "Examiner's search strategy and results",
                "directionCategory": "INTERNAL",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://beta-api.uspto.gov/api/v1/download/applications/12345678/KB3H43ZIRXEAPX5.pdf",
                        "pageTotalQuantity": 1
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2020-05-23T00:00:00.000-0400",
                "documentIdentifier": "FPC9GGN3PPOPPY4",
                "documentCode": "N417",
                "documentCodeDescriptionText": "Electronic Filing System Acknowledgment Receipt",
                "directionCategory": "OUTGOING",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://beta-api.uspto.gov/api/v1/download/applications/12345678/FPC9GGN3PPOPPY4.pdf",
                        "pageTotalQuantity": 3
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2024-04-27T00:00:00.000-0400",
                "documentIdentifier": "LVISQHJFBLUEX10",
                "documentCode": "M327",
                "documentCodeDescriptionText": "Miscellaneous Communication to Applicant - No Action Count",
                "directionCategory": "OUTGOING",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://beta-api.uspto.gov/api/v1/download/applications/12345678/LVISQHJFBLUEX10.pdf",
                        "pageTotalQuantity": 1
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2012-02-28T00:00:00.000-0500",
                "documentIdentifier": "GZKAAHOPPXXIFW4",
                "documentCode": "WFEE",
                "documentCodeDescriptionText": "Fee Worksheet (SB06)",
                "directionCategory": "INTERNAL",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://beta-api.uspto.gov/api/v1/download/applications/12345678/GZKAAHOPPXXIFW4.pdf",
                        "pageTotalQuantity": 1
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2024-06-11T00:00:00.000-0400",
                "documentIdentifier": "LXBNP3BDXBLUEX5",
                "documentCode": "OATH",
                "documentCodeDescriptionText": "Oath or Declaration filed",
                "directionCategory": "INCOMING",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://beta-api.uspto.gov/api/v1/download/applications/12345678/LXBNP3BDXBLUEX5.pdf",
                        "pageTotalQuantity": 4
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2011-10-06T00:00:00.000-0400",
                "documentIdentifier": "GTGKYNE9PPOPPY2",
                "documentCode": "N417",
                "documentCodeDescriptionText": "Electronic Filing System Acknowledgment Receipt",
                "directionCategory": "OUTGOING",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://beta-api.uspto.gov/api/v1/download/applications/12345678/GTGKYNE9PPOPPY2.pdf",
                        "pageTotalQuantity": 2
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2016-07-26T14:25:16.000-0400",
                "documentIdentifier": "IR3TO9D9RXEAPX3",
                "documentCode": "SRNT",
                "documentCodeDescriptionText": "Examiner's search strategy and results",
                "directionCategory": "INTERNAL",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://beta-api.uspto.gov/api/v1/download/applications/12345678/IR3TO9D9RXEAPX3.pdf",
                        "pageTotalQuantity": 1
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2011-05-06T00:00:00.000-0400",
                "documentIdentifier": "GNDGBKOEPPOPPY5",
                "documentCode": "FWCLM",
                "documentCodeDescriptionText": "Index of Claims",
                "directionCategory": "INTERNAL",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://beta-api.uspto.gov/api/v1/download/applications/12345678/GNDGBKOEPPOPPY5.pdf",
                        "pageTotalQuantity": 1
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2009-04-30T00:00:00.000-0400",
                "documentIdentifier": "FU5ITDA7PPOPPY5",
                "documentCode": "NTC.PUB",
                "documentCodeDescriptionText": "Notice of Publication",
                "directionCategory": "OUTGOING",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://beta-api.uspto.gov/api/v1/download/applications/12345678/FU5ITDA7PPOPPY5.pdf",
                        "pageTotalQuantity": 1
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2016-08-18T14:23:47.000-0400",
                "documentIdentifier": "IS0NODLBRXEAPX4",
                "documentCode": "SRNT",
                "documentCodeDescriptionText": "Examiner's search strategy and results",
                "directionCategory": "INTERNAL",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://beta-api.uspto.gov/api/v1/download/applications/12345678/IS0NODLBRXEAPX4.pdf",
                        "pageTotalQuantity": 1
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2012-01-31T00:00:00.000-0500",
                "documentIdentifier": "GY2ZH82KPXXIFW4",
                "documentCode": "CTFR",
                "documentCodeDescriptionText": "Final Rejection",
                "directionCategory": "OUTGOING",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://beta-api.uspto.gov/api/v1/download/applications/12345678/GY2ZH82KPXXIFW4.pdf",
                        "pageTotalQuantity": 11
                    },
                    {
                        "mimeTypeIdentifier": "MS_WORD",
                        "downloadUrl": "https://beta-api.uspto.gov/api/v1/download/applications/12345678/GY2ZH82KPXXIFW4/files/Final%20Rejection.DOCM"
                    },
                    {
                        "mimeTypeIdentifier": "XML",
                        "downloadUrl": "https://beta-api.uspto.gov/api/v1/download/applications/12345678/GY2ZH82KPXXIFW4/xmlarchive"
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2020-05-23T00:00:00.000-0400",
                "documentIdentifier": "FPC9GG6CPPOPPY4",
                "documentCode": "DRW",
                "documentCodeDescriptionText": "Drawings-only black and white line drawings",
                "directionCategory": "INCOMING",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://beta-api.uspto.gov/api/v1/download/applications/12345678/FPC9GG6CPPOPPY4.pdf",
                        "pageTotalQuantity": 3
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2011-05-06T00:00:00.000-0400",
                "documentIdentifier": "GNDGBKN4PPOPPY5",
                "documentCode": "892",
                "documentCodeDescriptionText": "List of references cited by examiner",
                "directionCategory": "OUTGOING",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://beta-api.uspto.gov/api/v1/download/applications/12345678/GNDGBKN4PPOPPY5.pdf",
                        "pageTotalQuantity": 1
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2024-04-27T00:00:00.000-0400",
                "documentIdentifier": "LVISQHJGBLUEX10",
                "documentCode": "M327",
                "documentCodeDescriptionText": "Miscellaneous Communication to Applicant - No Action Count",
                "directionCategory": "OUTGOING",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://beta-api.uspto.gov/api/v1/download/applications/12345678/LVISQHJGBLUEX10.pdf",
                        "pageTotalQuantity": 1
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2021-02-11T09:33:03.000-0500",
                "documentIdentifier": "KL0YP0BQLDFLYX4",
                "documentCode": "SRNT",
                "documentCodeDescriptionText": "Examiner's search strategy and results",
                "directionCategory": "INTERNAL",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://beta-api.uspto.gov/api/v1/download/applications/12345678/KL0YP0BQLDFLYX4.pdf",
                        "pageTotalQuantity": 1
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2011-10-06T00:00:00.000-0400",
                "documentIdentifier": "GTMXKNSLPPOPPY1",
                "documentCode": "CLM",
                "documentCodeDescriptionText": "Claims",
                "directionCategory": "INCOMING",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://beta-api.uspto.gov/api/v1/download/applications/12345678/GTMXKNSLPPOPPY1.pdf",
                        "pageTotalQuantity": 2
                    },
                    {
                        "mimeTypeIdentifier": "XML",
                        "downloadUrl": "https://beta-api.uspto.gov/api/v1/download/applications/12345678/GTMXKNSLPPOPPY1/xmlarchive"
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2018-02-24T01:19:28.000-0500",
                "documentIdentifier": "JE0Z6Q3URXEAPX1",
                "documentCode": "SRNT",
                "documentCodeDescriptionText": "Examiner's search strategy and results",
                "directionCategory": "INTERNAL",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://beta-api.uspto.gov/api/v1/download/applications/12345678/JE0Z6Q3URXEAPX1.pdf",
                        "pageTotalQuantity": 1
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2020-09-10T12:23:40.000-0400",
                "documentIdentifier": "KEX0U2HBRXEAPX4",
                "documentCode": "SRNT",
                "documentCodeDescriptionText": "Examiner's search strategy and results",
                "directionCategory": "INTERNAL",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://beta-api.uspto.gov/api/v1/download/applications/12345678/KEX0U2HBRXEAPX4.pdf",
                        "pageTotalQuantity": 1
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2024-05-01T00:00:00.000-0400",
                "documentIdentifier": "LVLCSJEYBLUEX10",
                "documentCode": "M327",
                "documentCodeDescriptionText": "Miscellaneous Communication to Applicant - No Action Count",
                "directionCategory": "OUTGOING",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://beta-api.uspto.gov/api/v1/download/applications/12345678/LVLCSJEYBLUEX10.pdf",
                        "pageTotalQuantity": 1
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2020-05-23T00:00:00.000-0400",
                "documentIdentifier": "FPC9GGHIPPOPPY4",
                "documentCode": "WFEE",
                "documentCodeDescriptionText": "Fee Worksheet (SB06)",
                "directionCategory": "INTERNAL",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://beta-api.uspto.gov/api/v1/download/applications/12345678/FPC9GGHIPPOPPY4.pdf",
                        "pageTotalQuantity": 2
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2011-10-06T00:00:00.000-0400",
                "documentIdentifier": "GTMXKNWVPPOPPY1",
                "documentCode": "REM",
                "documentCodeDescriptionText": "Applicant Arguments/Remarks Made in an Amendment",
                "directionCategory": "INCOMING",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://beta-api.uspto.gov/api/v1/download/applications/12345678/GTMXKNWVPPOPPY1.pdf",
                        "pageTotalQuantity": 3
                    },
                    {
                        "mimeTypeIdentifier": "XML",
                        "downloadUrl": "https://beta-api.uspto.gov/api/v1/download/applications/12345678/GTMXKNWVPPOPPY1/xmlarchive"
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2011-05-06T00:00:00.000-0400",
                "documentIdentifier": "GNDGBKP1PPOPPY5",
                "documentCode": "SRNT",
                "documentCodeDescriptionText": "Examiner's search strategy and results",
                "directionCategory": "INTERNAL",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://beta-api.uspto.gov/api/v1/download/applications/12345678/GNDGBKP1PPOPPY5.pdf",
                        "pageTotalQuantity": 3
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2018-04-13T11:05:23.000-0400",
                "documentIdentifier": "JFY33WLQRXEAPX5",
                "documentCode": "SRNT",
                "documentCodeDescriptionText": "Examiner's search strategy and results",
                "directionCategory": "INTERNAL",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://beta-api.uspto.gov/api/v1/download/applications/12345678/JFY33WLQRXEAPX5.pdf",
                        "pageTotalQuantity": 1
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2017-08-10T17:00:24.000-0400",
                "documentIdentifier": "J66XGWQHRXEAPX1",
                "documentCode": "N417",
                "documentCodeDescriptionText": "Electronic Filing System Acknowledgment Receipt",
                "directionCategory": "OUTGOING",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://beta-api.uspto.gov/api/v1/download/applications/12345678/J66XGWQHRXEAPX1.pdf",
                        "pageTotalQuantity": 2
                    }
                ]
            },
            {
                "applicationNumberText": "12345678",
                "officialDate": "2020-05-23T00:00:00.000-0400",
                "documentIdentifier": "FPC9GG0KPPOPPY4",
                "documentCode": "SPEC",
                "documentCodeDescriptionText": "Specification",
                "directionCategory": "INCOMING",
                "downloadOptionBag": [
                    {
                        "mimeTypeIdentifier": "PDF",
                        "downloadUrl": "https://beta-api.uspto.gov/api/v1/download/applications/12345678/FPC9GG0KPPOPPY4.pdf",
                        "pageTotalQuantity": 10
                    },
                    {
                        "mimeTypeIdentifier": "XML",
                        "downloadUrl": "https://beta-api.uspto.gov/api/v1/download/applications/12345678/FPC9GG0KPPOPPY4/xmlarchive"
                    }
                ]
            }
        ]
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
    result = await client.get_patent_documents("12345678")
    
    # Assertions
    assert result is not None
    assert len(result.documents) == len(mock_response_data["documentBag"])
    
    # Test specific document types and their counts
    srnt_docs = [doc for doc in result.documents if doc.document_code == "SRNT"]
    oath_docs = [doc for doc in result.documents if doc.document_code == "OATH"]
    wfee_docs = [doc for doc in result.documents if doc.document_code == "WFEE"]
    
    assert len(srnt_docs) == 25  # Verify exact number of SRNT documents
    assert len(oath_docs) == 7   # Update to match actual count of OATH documents
    assert len(wfee_docs) == 7   # Verify exact number of WFEE documents
    
    # Test specific document properties
    spec_doc = next(doc for doc in result.documents if doc.document_code == "SPEC")
    assert spec_doc.document_description == "Specification"
    assert spec_doc.direction_category == "INCOMING"
    assert len(spec_doc.download_options) == 2  # PDF and XML options
    
    # Verify exact download URLs are preserved
    assert spec_doc.download_options[0].download_url == "https://beta-api.uspto.gov/api/v1/download/applications/12345678/FPC9GG0KPPOPPY4.pdf"
    assert spec_doc.download_options[1].download_url == "https://beta-api.uspto.gov/api/v1/download/applications/12345678/FPC9GG0KPPOPPY4/xmlarchive"
    
    # Test API call - verify params dict is passed (even if empty)
    mock_session.get.assert_called_once()
    call_args = mock_session.get.call_args
    assert call_args[0][0] == "https://api.uspto.gov/api/v1/patent/applications/12345678/documents"
    assert call_args[1]["headers"]["X-API-KEY"] == "test_api_key"
    assert call_args[1]["headers"]["accept"] == "application/json"
    # Params dict should be present (empty when no filters are provided)
    assert "params" in call_args[1]
    assert call_args[1]["params"] == {}
    mock_response.json.assert_called_once()

@pytest.mark.asyncio
async def test_get_patent_documents_error(client):
    client, mock_session = client
    
    # Create error response
    mock_response = Mock()
    mock_response.status = 404
    mock_response.json = AsyncMock(return_value={"message": "Not Found", "details": "No details provided"})
    
    # Create async context manager mock
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = mock_response
    mock_session.get.return_value = async_cm
    
    # Test error handling
    with pytest.raises(USPTOError) as exc_info:
        await client.get_patent_documents("12345678")
    
    assert str(exc_info.value) == "404: Not Found - No details provided"  # Update to match the actual error message


@pytest.mark.asyncio
async def test_get_patent_documents_with_date_from(client):
    """Test GET /documents endpoint with officialDateFrom parameter"""
    client, mock_session = client
    
    # Create mock response data
    mock_response_data = {
        "documentBag": [
            {
                "applicationNumberText": "12345678",
                "officialDate": "2023-06-15T00:00:00.000-0400",
                "documentIdentifier": "TEST123",
                "documentCode": "SRNT",
                "documentCodeDescriptionText": "Test document",
                "directionCategory": "INTERNAL",
                "downloadOptionBag": []
            }
        ]
    }
    
    # Create mock response
    mock_response = Mock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value=mock_response_data)
    
    # Create async context manager mock
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = mock_response
    mock_session.get.return_value = async_cm
    
    # Execute test with officialDateFrom parameter
    result = await client.get_patent_documents("12345678", official_date_from="2023-01-01")
    
    # Assertions
    assert result is not None
    assert len(result.documents) == 1
    
    # Verify API call was made with correct parameters
    mock_session.get.assert_called_once()
    call_args = mock_session.get.call_args
    assert call_args[0][0].endswith("/documents")
    # Check that params dict exists and contains the expected parameter
    assert "params" in call_args[1]
    assert call_args[1]["params"]["officialDateFrom"] == "2023-01-01"
    assert "officialDateTo" not in call_args[1].get("params", {})
    assert "documentCodes" not in call_args[1].get("params", {})


@pytest.mark.asyncio
async def test_get_patent_documents_with_date_to(client):
    """Test GET /documents endpoint with officialDateTo parameter"""
    client, mock_session = client
    
    # Create mock response data
    mock_response_data = {
        "documentBag": [
            {
                "applicationNumberText": "12345678",
                "officialDate": "2023-06-15T00:00:00.000-0400",
                "documentIdentifier": "TEST123",
                "documentCode": "SRNT",
                "documentCodeDescriptionText": "Test document",
                "directionCategory": "INTERNAL",
                "downloadOptionBag": []
            }
        ]
    }
    
    # Create mock response
    mock_response = Mock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value=mock_response_data)
    
    # Create async context manager mock
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = mock_response
    mock_session.get.return_value = async_cm
    
    # Execute test with officialDateTo parameter
    result = await client.get_patent_documents("12345678", official_date_to="2023-12-31")
    
    # Assertions
    assert result is not None
    assert len(result.documents) == 1
    
    # Verify API call was made with correct parameters
    mock_session.get.assert_called_once()
    call_args = mock_session.get.call_args
    assert call_args[0][0].endswith("/documents")
    # Check that params dict exists and contains the expected parameter
    assert "params" in call_args[1]
    assert call_args[1]["params"]["officialDateTo"] == "2023-12-31"
    assert "officialDateFrom" not in call_args[1].get("params", {})
    assert "documentCodes" not in call_args[1].get("params", {})


@pytest.mark.asyncio
async def test_get_patent_documents_with_date_range(client):
    """Test GET /documents endpoint with both date parameters"""
    client, mock_session = client
    
    # Create mock response data
    mock_response_data = {
        "documentBag": [
            {
                "applicationNumberText": "12345678",
                "officialDate": "2023-06-15T00:00:00.000-0400",
                "documentIdentifier": "TEST123",
                "documentCode": "SRNT",
                "documentCodeDescriptionText": "Test document",
                "directionCategory": "INTERNAL",
                "downloadOptionBag": []
            }
        ]
    }
    
    # Create mock response
    mock_response = Mock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value=mock_response_data)
    
    # Create async context manager mock
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = mock_response
    mock_session.get.return_value = async_cm
    
    # Execute test with both date parameters
    result = await client.get_patent_documents(
        "12345678",
        official_date_from="2023-01-01",
        official_date_to="2023-12-31"
    )
    
    # Assertions
    assert result is not None
    assert len(result.documents) == 1
    
    # Verify API call was made with correct parameters
    mock_session.get.assert_called_once()
    call_args = mock_session.get.call_args
    assert call_args[0][0].endswith("/documents")
    # Check that params dict exists and contains the expected parameters
    assert "params" in call_args[1]
    assert call_args[1]["params"]["officialDateFrom"] == "2023-01-01"
    assert call_args[1]["params"]["officialDateTo"] == "2023-12-31"
    assert "documentCodes" not in call_args[1].get("params", {})


@pytest.mark.asyncio
async def test_get_patent_documents_with_document_codes(client):
    """Test GET /documents endpoint with documentCodes parameter"""
    client, mock_session = client
    
    # Create mock response data
    mock_response_data = {
        "documentBag": [
            {
                "applicationNumberText": "12345678",
                "officialDate": "2023-06-15T00:00:00.000-0400",
                "documentIdentifier": "TEST123",
                "documentCode": "WFEE",
                "documentCodeDescriptionText": "Fee Worksheet",
                "directionCategory": "INTERNAL",
                "downloadOptionBag": []
            }
        ]
    }
    
    # Create mock response
    mock_response = Mock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value=mock_response_data)
    
    # Create async context manager mock
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = mock_response
    mock_session.get.return_value = async_cm
    
    # Test with single document code
    result = await client.get_patent_documents("12345678", document_codes="WFEE")
    
    # Assertions
    assert result is not None
    assert len(result.documents) == 1
    
    # Verify API call was made with correct parameters
    mock_session.get.assert_called_once()
    call_args = mock_session.get.call_args
    assert call_args[0][0].endswith("/documents")
    # Check that params dict exists and contains the expected parameter
    assert "params" in call_args[1]
    assert call_args[1]["params"]["documentCodes"] == "WFEE"
    assert "officialDateFrom" not in call_args[1].get("params", {})
    assert "officialDateTo" not in call_args[1].get("params", {})
    
    # Reset mock for multiple document codes test
    mock_session.get.reset_mock()
    async_cm.__aenter__.return_value = mock_response
    
    # Test with multiple document codes
    result = await client.get_patent_documents("12345678", document_codes="SRFW,SRNT")
    
    # Assertions
    assert result is not None
    
    # Verify API call was made with correct parameters
    mock_session.get.assert_called_once()
    call_args = mock_session.get.call_args
    assert "params" in call_args[1]
    assert call_args[1]["params"]["documentCodes"] == "SRFW,SRNT"


@pytest.mark.asyncio
async def test_get_patent_documents_with_all_filters(client):
    """Test GET /documents endpoint with all filter parameters"""
    client, mock_session = client
    
    # Create mock response data
    mock_response_data = {
        "documentBag": [
            {
                "applicationNumberText": "12345678",
                "officialDate": "2023-06-15T00:00:00.000-0400",
                "documentIdentifier": "TEST123",
                "documentCode": "WFEE",
                "documentCodeDescriptionText": "Fee Worksheet",
                "directionCategory": "INTERNAL",
                "downloadOptionBag": []
            }
        ]
    }
    
    # Create mock response
    mock_response = Mock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value=mock_response_data)
    
    # Create async context manager mock
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = mock_response
    mock_session.get.return_value = async_cm
    
    # Execute test with all parameters
    result = await client.get_patent_documents(
        "12345678",
        official_date_from="2023-01-01",
        official_date_to="2023-12-31",
        document_codes="WFEE,SRNT"
    )
    
    # Assertions
    assert result is not None
    assert len(result.documents) == 1
    
    # Verify API call was made with all correct parameters
    mock_session.get.assert_called_once()
    call_args = mock_session.get.call_args
    assert call_args[0][0].endswith("/documents")
    # Check that params dict exists and contains all expected parameters
    assert "params" in call_args[1]
    params = call_args[1]["params"]
    assert params["officialDateFrom"] == "2023-01-01"
    assert params["officialDateTo"] == "2023-12-31"
    assert params["documentCodes"] == "WFEE,SRNT"