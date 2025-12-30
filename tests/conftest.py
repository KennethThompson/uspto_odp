import sys
from pathlib import Path

def pytest_configure(config):
    # Get the absolute path to src directory
    src_path = str(Path(__file__).parent.parent.absolute() / "src")
    print(f"Adding src path: {src_path}")
    
    # Add src to the beginning of sys.path if not already there
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
    
    print(f"Final sys.path: {sys.path}")
    
    # Verify the correct module location
    try:
        import uspto_odp
        print(f"uspto_odp location: {uspto_odp.__file__}")
    except ImportError as e:
        print(f"Import error: {e}")
    
    # Register custom markers
    config.addinivalue_line("markers", "integration: marks tests as integration tests (requires USPTO_API_KEY)")

pytest_plugins = ["pytest_asyncio"]