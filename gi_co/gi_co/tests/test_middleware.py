import pytest
from django.core.cache import cache
from django.test import RequestFactory
from django.http import HttpResponse
from gi_co.middleware import TrafficHandlerMiddleware
# import logging

# logger = logging.getLogger(__name__)


def dummy_response(request):
    return HttpResponse("Success")


@pytest.fixture(autouse=True)
def clear_cache():
    cache.clear()

@pytest.fixture()
def request_client():
    ip = '198.168.1.1'
    factory = RequestFactory()
    request = factory.get('/accounts/user-data/')
    request.META['REMOTE_ADDR'] = ip
    return request


def test_single_request(request_client):
    """
    Test for a single request.
    """
    middleware = TrafficHandlerMiddleware(dummy_response)
    response = middleware(request_client)
    ip = request_client.META['REMOTE_ADDR']
    assert response.status_code == 200
    assert cache.get(ip) == 1

def test_multiple_requests(request_client):
    """
    Test for multiple request, not exceeding the limit.
    """
    middleware = TrafficHandlerMiddleware(dummy_response)
    ip = request_client.META['REMOTE_ADDR']
    for i in range(10):
        response = middleware(request_client)
    assert cache.get(ip) == 10

def test_limit_exceed(request_client):
    """
    Test for request exceeding limit.
    """
    middleware = TrafficHandlerMiddleware(dummy_response)
    ip = request_client.META["REMOTE_ADDR"]

    for i in range(101):
        response = middleware(request_client)
        if i >= 100:
            assert response.status_code == 429

