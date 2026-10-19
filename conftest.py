import pytest

from utils.api_client import ApiClient


@pytest.fixture
def api_client():
    """每条测试使用独立客户端，避免 Session 状态互相污染。"""
    client = ApiClient()
    yield client
    client.session.close()
