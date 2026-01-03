#!/usr/bin/env python3
"""
CLI script to test the USPTO status-codes endpoint.
Tests both paginated and non-paginated requests to see the API responses.
"""
import asyncio
import json
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from uspto_odp.controller.uspto_odp_client import USPTOClient, USPTOError

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)


def print_section(title: str):
    """Print a formatted section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def print_response(result, title: str):
    """Pretty print the API response."""
    print_section(title)
    print(f"Total Count: {result.count}")
    print(f"Status Codes Returned: {len(result.status_codes)}")
    if result.request_identifier:
        print(f"Request Identifier: {result.request_identifier}")
    
    if result.status_codes:
        print("\nStatus Codes:")
        print("-" * 80)
        for idx, status_code in enumerate(result.status_codes, 1):
            print(f"{idx:3d}. Code: {status_code.application_status_code:3d} | "
                  f"Description: {status_code.application_status_description_text}")
    else:
        print("\n⚠️  No status codes returned in response (only count provided)")
    
    print("\n" + "-" * 80)
    print("Raw JSON Response:")
    print(json.dumps({
        "count": result.count,
        "statusCodeDataBag": [
            {
                "applicationStatusCode": sc.application_status_code,
                "applicationStatusDescriptionText": sc.application_status_description_text
            }
            for sc in result.status_codes
        ],
        "requestIdentifier": result.request_identifier
    }, indent=2))


async def test_without_pagination(client: USPTOClient):
    """Test the endpoint without any pagination parameters."""
    print_section("Test 1: GET /status-codes (No Parameters)")
    print("Calling endpoint without any query parameters or pagination...")
    
    try:
        result = await client.search_status_codes_get()
        print_response(result, "Response: No Parameters")
        return result
    except USPTOError as e:
        print(f"\n❌ Error: {e.code} - {e.error}")
        if e.error_details:
            print(f"   Details: {e.error_details}")
        return None
    except Exception as e:
        print(f"\n❌ Unexpected error: {type(e).__name__}: {e}")
        return None


async def test_with_pagination(client: USPTOClient, limit: int = 25, offset: int = 0):
    """Test the endpoint with pagination parameters."""
    print_section(f"Test 2: GET /status-codes (With Pagination: limit={limit}, offset={offset})")
    print(f"Calling endpoint with pagination parameters (limit={limit}, offset={offset})...")
    
    try:
        result = await client.search_status_codes_get(limit=limit, offset=offset)
        print_response(result, f"Response: Pagination (limit={limit}, offset={offset})")
        return result
    except USPTOError as e:
        print(f"\n❌ Error: {e.code} - {e.error}")
        if e.error_details:
            print(f"   Details: {e.error_details}")
        return None
    except Exception as e:
        print(f"\n❌ Unexpected error: {type(e).__name__}: {e}")
        return None


async def test_fetch_all_with_pagination(client: USPTOClient, page_size: int = 25):
    """Fetch all status codes by paginating through all results."""
    print_section(f"Test 3: GET /status-codes (Fetch All with Pagination, page_size={page_size})")
    print(f"Fetching all status codes by paginating through results...")
    
    all_status_codes = []
    offset = 0
    total_count = None
    
    try:
        while True:
            print(f"\n📄 Fetching page: offset={offset}, limit={page_size}")
            result = await client.search_status_codes_get(limit=page_size, offset=offset)
            
            # Store total count from first response
            if total_count is None:
                total_count = result.count
                print(f"   Total available: {total_count} status codes")
            
            # Add status codes from this page
            if result.status_codes:
                all_status_codes.extend(result.status_codes)
                print(f"   Retrieved: {len(result.status_codes)} status codes (total so far: {len(all_status_codes)})")
            
            # Check if we've retrieved all available status codes
            if len(all_status_codes) >= total_count or not result.status_codes:
                break
            
            # Move to next page
            offset += page_size
            
            # Small delay to respect rate limits
            await asyncio.sleep(0.5)
        
        print_section("Final Results: All Status Codes Retrieved")
        print(f"Total Count (from API): {total_count}")
        print(f"Status Codes Retrieved: {len(all_status_codes)}")
        
        if all_status_codes:
            print("\nAll Status Codes:")
            print("-" * 80)
            for idx, status_code in enumerate(all_status_codes, 1):
                print(f"{idx:3d}. Code: {status_code.application_status_code:3d} | "
                      f"Description: {status_code.application_status_description_text}")
        
        return {
            "total_count": total_count,
            "retrieved_count": len(all_status_codes),
            "status_codes": all_status_codes
        }
        
    except USPTOError as e:
        print(f"\n❌ Error: {e.code} - {e.error}")
        if e.error_details:
            print(f"   Details: {e.error_details}")
        return None
    except Exception as e:
        print(f"\n❌ Unexpected error: {type(e).__name__}: {e}")
        return None


async def test_with_query(client: USPTOClient):
    """Test the endpoint with a query parameter."""
    print_section("Test 4: GET /status-codes (With Query Parameter)")
    print("Calling endpoint with a query parameter to filter results...")
    
    try:
        # Search for status codes containing "Patent" in description
        result = await client.search_status_codes_get(
            q="applicationStatusDescriptionText:Patent",
            limit=10
        )
        print_response(result, "Response: With Query Parameter")
        return result
    except USPTOError as e:
        print(f"\n❌ Error: {e.code} - {e.error}")
        if e.error_details:
            print(f"   Details: {e.error_details}")
        return None
    except Exception as e:
        print(f"\n❌ Unexpected error: {type(e).__name__}: {e}")
        return None


async def main():
    """Main function to run all tests."""
    # Get API key from environment
    api_key = os.environ.get("USPTO_API_KEY")
    
    if not api_key:
        print("❌ Error: USPTO_API_KEY not found in environment variables.")
        print("   Please set it in your .env file or export it as an environment variable.")
        sys.exit(1)
    
    print("=" * 80)
    print("  USPTO Status Codes Endpoint Test Script")
    print("=" * 80)
    print(f"\nAPI Key: {api_key[:10]}...{api_key[-4:] if len(api_key) > 14 else ''}")
    print(f"Endpoint: https://api.uspto.gov/api/v1/patent/status-codes")
    
    # Create client
    client = USPTOClient(api_key=api_key)
    
    try:
        # Test 1: Without pagination
        await test_without_pagination(client)
        await asyncio.sleep(1)  # Rate limiting
        
        # Test 2: With pagination
        await test_with_pagination(client, limit=10, offset=0)
        await asyncio.sleep(1)  # Rate limiting
        
        # Test 3: Fetch all with pagination
        await test_fetch_all_with_pagination(client, page_size=25)
        await asyncio.sleep(1)  # Rate limiting
        
        # Test 4: With query parameter
        await test_with_query(client)
        
    finally:
        # Clean up
        await client.session.close()
    
    print_section("All Tests Complete")
    print("✅ Finished testing status-codes endpoint")


if __name__ == "__main__":
    asyncio.run(main())
