import pytest

@pytest.fixture(scope="module")
def sample_config():
    return {
        "app_name": "Test Project",
        "version": "test"
    }
