from rest_framework.test import APIClient
import pytest


@pytest.fixture()
def api_client():
    """
    Fixture to provide an API client
    """
    yield APIClient()
