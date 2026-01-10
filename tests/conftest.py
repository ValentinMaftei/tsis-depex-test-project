"""
Pytest configuration file for the test suite.
"""
import sys
from pathlib import Path

# Add the project root to the path so imports work correctly
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pytest


@pytest.fixture(scope="session")
def test_session():
    """
    Session-scoped fixture for test setup.
    """
    print("\n=== Test Session Started ===")
    yield
    print("\n=== Test Session Completed ===")
