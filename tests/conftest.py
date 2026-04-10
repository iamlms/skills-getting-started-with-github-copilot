"""
Pytest configuration and shared fixtures for API tests.
"""

import pytest
import copy
from fastapi.testclient import TestClient
from src.app import app, activities


# Store the original activities state
ORIGINAL_ACTIVITIES = copy.deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to original state before each test."""
    # Clear and repopulate activities with fresh copy
    activities.clear()
    activities.update(copy.deepcopy(ORIGINAL_ACTIVITIES))
    yield
    # Cleanup after test
    activities.clear()
    activities.update(copy.deepcopy(ORIGINAL_ACTIVITIES))


@pytest.fixture
def client():
    """Provide a TestClient instance for making requests to the API."""
    return TestClient(app)
