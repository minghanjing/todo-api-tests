import logging
from urllib.parse import urljoin

import requests

from config.settings import BASE_URL, TIMEOUT


logger = logging.getLogger(__name__)


class ApiClient:
    """统一封装接口请求的公共逻辑。"""

    def __init__(self):
        self.base_url = BASE_URL
        self.timeout = TIMEOUT
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})

    def request(self, method, endpoint, **kwargs):
        url = urljoin(f"{self.base_url}/", endpoint.lstrip("/"))
        logger.info("%s %s", method.upper(), url)

        response = self.session.request(
            method,
            url,
            timeout=self.timeout,
            **kwargs,
        )

        logger.info("%s %s -> %s", method.upper(), url, response.status_code)
        if not response.ok:
            logger.warning("响应体: %s", response.text[:500])

        return response

    def get(self, endpoint, params=None, **kwargs):
        return self.request("GET", endpoint, params=params, **kwargs)

    def post(self, endpoint, payload=None, **kwargs):
        return self.request("POST", endpoint, json=payload, **kwargs)
