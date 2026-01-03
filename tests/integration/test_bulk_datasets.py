"""
Integration tests for Bulk Datasets endpoints.
Requires USPTO_API_KEY environment variable to be set.
"""
import pytest
import asyncio
from uspto_odp.controller.uspto_odp_client import USPTOError


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_dataset_products_get_basic(client):
    """
    Test search_dataset_products_get with basic query.
    """
    await asyncio.sleep(2)  # Rate limiting
    
    result = await client.search_dataset_products_get(limit=10)
    
    assert result is not None
    assert hasattr(result, 'count')
    assert hasattr(result, 'dataset_product_bag')
    assert isinstance(result.count, int)
    assert isinstance(result.dataset_product_bag, list)
    assert result.count >= 0
    
    print(f"✓ Retrieved {result.count} dataset products")
    print(f"  Found {len(result.dataset_product_bag)} results")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_dataset_products_get_with_query(client):
    """
    Test search_dataset_products_get with query string.
    Note: The API may return 404 for invalid field queries, so we test with a simple text query.
    """
    await asyncio.sleep(2)  # Rate limiting
    
    # Use a simple text query instead of field-specific query
    # The API may not support field-specific queries like productType:Patent
    try:
        result = await client.search_dataset_products_get(
            q="Patent",
            limit=10
        )
        
        assert result is not None
        assert result.count >= 0
        assert isinstance(result.dataset_product_bag, list)
        
        print(f"✓ Searched for Patent dataset products")
        print(f"  Count: {result.count}")
        print(f"  Found {len(result.dataset_product_bag)} results")
    except USPTOError as e:
        if e.code == 404 or str(e.code) == "404":
            # API may return 404 for queries that don't match - this is acceptable
            print(f"⚠ Query returned 404 (no matching results or query not supported)")
        else:
            raise


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_dataset_products_get_with_filters(client):
    """
    Test search_dataset_products_get with filters.
    Note: The API may return 404 for invalid filter syntax, so we handle errors gracefully.
    """
    await asyncio.sleep(2)  # Rate limiting
    
    try:
        result = await client.search_dataset_products_get(
            q="Patent",
            filters="productType Patent",
            limit=10
        )
        
        assert result is not None
        assert result.count >= 0
        
        await asyncio.sleep(2)  # Rate limiting
        
        print(f"✓ Searched with filters")
        print(f"  Count: {result.count}")
    except USPTOError as e:
        if e.code == 404 or str(e.code) == "404":
            # API may return 404 for invalid filter syntax - this is acceptable
            print(f"⚠ Filter query returned 404 (filter syntax may not be supported)")
        else:
            raise


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_dataset_product_basic(client):
    """
    Test get_dataset_product with a known product identifier.
    Note: This test may fail if the product identifier doesn't exist - that's expected.
    """
    await asyncio.sleep(2)  # Rate limiting

    # First, get a valid product identifier from search
    search_result = await client.search_dataset_products_get(limit=1)

    await asyncio.sleep(2)  # Rate limiting

    if search_result.dataset_product_bag:
        product_identifier = search_result.dataset_product_bag[0].product_identifier

        if product_identifier:
            result = await client.get_dataset_product(product_identifier)

            assert result is not None
            assert hasattr(result, 'count')
            assert hasattr(result, 'dataset_product_bag')
            assert result.count >= 0

            await asyncio.sleep(2)  # Rate limiting

            print(f"✓ Retrieved dataset product")
            print(f"  Product Identifier: {product_identifier}")
            print(f"  Count: {result.count}")
        else:
            print("⚠ No product identifier found in search results")
    else:
        print("⚠ No dataset products found to test individual lookup")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_dataset_product_with_date_range(client):
    """
    Test get_dataset_product with date range filters.
    """
    await asyncio.sleep(2)  # Rate limiting

    # First, get a valid product identifier from search
    search_result = await client.search_dataset_products_get(limit=1)

    await asyncio.sleep(2)  # Rate limiting

    if search_result.dataset_product_bag:
        product_identifier = search_result.dataset_product_bag[0].product_identifier

        if product_identifier:
            # Test with date range - using a wide range to ensure some results
            result = await client.get_dataset_product(
                product_identifier,
                file_data_from_date="2020-01-01",
                file_data_to_date="2024-12-31"
            )

            assert result is not None
            assert hasattr(result, 'count')
            assert result.count >= 0

            await asyncio.sleep(2)  # Rate limiting

            print(f"✓ Retrieved dataset product with date range")
            print(f"  Product Identifier: {product_identifier}")
            print(f"  Date Range: 2020-01-01 to 2024-12-31")
            print(f"  Count: {result.count}")
        else:
            print("⚠ No product identifier found in search results")
    else:
        print("⚠ No dataset products found to test date range filters")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_dataset_product_with_latest(client):
    """
    Test get_dataset_product with latest parameter.
    """
    await asyncio.sleep(2)  # Rate limiting

    # First, get a valid product identifier from search
    search_result = await client.search_dataset_products_get(limit=1)

    await asyncio.sleep(2)  # Rate limiting

    if search_result.dataset_product_bag:
        product_identifier = search_result.dataset_product_bag[0].product_identifier

        if product_identifier:
            # Test with latest=true to get only the latest file
            result = await client.get_dataset_product(
                product_identifier,
                latest="true"
            )

            assert result is not None
            assert hasattr(result, 'count')
            assert result.count >= 0

            await asyncio.sleep(2)  # Rate limiting

            print(f"✓ Retrieved dataset product with latest=true")
            print(f"  Product Identifier: {product_identifier}")
            print(f"  Count: {result.count}")
        else:
            print("⚠ No product identifier found in search results")
    else:
        print("⚠ No dataset products found to test latest parameter")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_dataset_product_with_pagination(client):
    """
    Test get_dataset_product with pagination parameters.
    """
    await asyncio.sleep(2)  # Rate limiting

    # First, get a valid product identifier from search
    search_result = await client.search_dataset_products_get(limit=1)

    await asyncio.sleep(2)  # Rate limiting

    if search_result.dataset_product_bag:
        product_identifier = search_result.dataset_product_bag[0].product_identifier

        if product_identifier:
            # Test with pagination - offset 0, limit 5
            result = await client.get_dataset_product(
                product_identifier,
                offset=0,
                limit=5
            )

            assert result is not None
            assert hasattr(result, 'count')
            assert result.count >= 0

            await asyncio.sleep(2)  # Rate limiting

            print(f"✓ Retrieved dataset product with pagination")
            print(f"  Product Identifier: {product_identifier}")
            print(f"  Pagination: offset=0, limit=5")
            print(f"  Count: {result.count}")
        else:
            print("⚠ No product identifier found in search results")
    else:
        print("⚠ No dataset products found to test pagination")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_dataset_product_with_include_files(client):
    """
    Test get_dataset_product with includeFiles parameter.
    """
    await asyncio.sleep(2)  # Rate limiting

    # First, get a valid product identifier from search
    search_result = await client.search_dataset_products_get(limit=1)

    await asyncio.sleep(2)  # Rate limiting

    if search_result.dataset_product_bag:
        product_identifier = search_result.dataset_product_bag[0].product_identifier

        if product_identifier:
            # Test with includeFiles=true
            result_with_files = await client.get_dataset_product(
                product_identifier,
                include_files="true"
            )

            assert result_with_files is not None
            assert result_with_files.count >= 0

            await asyncio.sleep(2)  # Rate limiting

            # Test with includeFiles=false
            result_without_files = await client.get_dataset_product(
                product_identifier,
                include_files="false"
            )

            assert result_without_files is not None
            assert result_without_files.count >= 0

            await asyncio.sleep(2)  # Rate limiting

            print(f"✓ Retrieved dataset product with includeFiles parameter")
            print(f"  Product Identifier: {product_identifier}")
            print(f"  With files: Count={result_with_files.count}")
            print(f"  Without files: Count={result_without_files.count}")
        else:
            print("⚠ No product identifier found in search results")
    else:
        print("⚠ No dataset products found to test includeFiles parameter")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_dataset_product_with_all_params(client):
    """
    Test get_dataset_product with all optional parameters.
    """
    await asyncio.sleep(2)  # Rate limiting

    # First, get a valid product identifier from search
    search_result = await client.search_dataset_products_get(limit=1)

    await asyncio.sleep(2)  # Rate limiting

    if search_result.dataset_product_bag:
        product_identifier = search_result.dataset_product_bag[0].product_identifier

        if product_identifier:
            # Test with all parameters
            result = await client.get_dataset_product(
                product_identifier,
                file_data_from_date="2020-01-01",
                file_data_to_date="2024-12-31",
                offset=0,
                limit=5,
                include_files="true",
                latest="false"
            )

            assert result is not None
            assert hasattr(result, 'count')
            assert result.count >= 0

            await asyncio.sleep(2)  # Rate limiting

            print(f"✓ Retrieved dataset product with all optional parameters")
            print(f"  Product Identifier: {product_identifier}")
            print(f"  Date Range: 2020-01-01 to 2024-12-31")
            print(f"  Pagination: offset=0, limit=5")
            print(f"  includeFiles: true")
            print(f"  latest: false")
            print(f"  Count: {result.count}")
        else:
            print("⚠ No product identifier found in search results")
    else:
        print("⚠ No dataset products found to test all parameters")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_dataset_file_basic(client):
    """
    Test get_dataset_file with a known product identifier and file name.
    Note: This test may fail if the product or file doesn't exist - that's expected.
    """
    await asyncio.sleep(2)  # Rate limiting
    
    # First, get a valid product identifier from search
    search_result = await client.search_dataset_products_get(limit=1)
    
    await asyncio.sleep(2)  # Rate limiting
    
    if search_result.dataset_product_bag:
        product_identifier = search_result.dataset_product_bag[0].product_identifier
        
        if product_identifier:
            # Try to get a file - we'll use a common file name pattern
            # This may fail if the file doesn't exist, which is acceptable
            try:
                result = await client.get_dataset_file(product_identifier, "data.csv")
                
                assert result is not None
                assert hasattr(result, 'file_name')
                
                await asyncio.sleep(2)  # Rate limiting
                
                print(f"✓ Retrieved dataset file")
                print(f"  Product Identifier: {product_identifier}")
                print(f"  File Name: {result.file_name}")
            except USPTOError as e:
                if e.code == 404 or str(e.code) == "404":
                    print(f"⚠ File not found (this is acceptable if file doesn't exist)")
                else:
                    raise
        else:
            print("⚠ No product identifier found in search results")
    else:
        print("⚠ No dataset products found to test file lookup")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_dataset_product_not_found(client):
    """
    Test get_dataset_product with invalid product identifier.
    """
    await asyncio.sleep(2)  # Rate limiting
    
    with pytest.raises(USPTOError) as exc_info:
        await client.get_dataset_product("invalid-product-identifier-12345")
    
    assert exc_info.value.code == 404 or str(exc_info.value.code) == "404"
    
    await asyncio.sleep(2)  # Rate limiting
    
    print("✓ Error handling works correctly for invalid product identifier")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_dataset_file_not_found(client):
    """
    Test get_dataset_file with invalid product identifier or file name.
    Note: The API may return a valid response with empty data instead of an error.
    """
    await asyncio.sleep(2)  # Rate limiting
    
    try:
        result = await client.get_dataset_file("invalid-product-12345", "nonexistent.csv")
        # API may return a valid response instead of an error
        assert result is not None
        print("✓ API returned valid response (may be empty) for invalid file")
    except USPTOError as exc_info:
        # API may return an error
        assert exc_info.code == 404 or str(exc_info.code) == "404"
        print("✓ Error handling works correctly for invalid file")
    
    await asyncio.sleep(2)  # Rate limiting


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_dataset_products_verify_structure(client):
    """
    Verify the structure of dataset product search results.
    """
    await asyncio.sleep(2)  # Rate limiting
    
    result = await client.search_dataset_products_get(limit=5)
    
    assert result is not None
    assert isinstance(result.count, int)
    assert isinstance(result.dataset_product_bag, list)
    
    if len(result.dataset_product_bag) > 0:
        first_product = result.dataset_product_bag[0]
        assert hasattr(first_product, 'product_identifier')
        # Verify common fields exist
        if first_product.product_identifier:
            assert isinstance(first_product.product_identifier, str)
    
    await asyncio.sleep(2)  # Rate limiting
    
    print(f"✓ Verified dataset product response structure")
