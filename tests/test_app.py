import unittest
from unittest.mock import patch

import app


class DummyResponse:
    def __init__(self, payload, ok=True, status_code=200):
        self._payload = payload
        self.ok = ok
        self.status_code = status_code
        self.text = str(payload)

    def json(self):
        return self._payload


class FrontendBackendProxyTests(unittest.TestCase):
    def setUp(self):
        self.client = app.app.test_client()

    @patch("app.requests.post")
    def test_projection_proxies_backend_contract(self, post):
        post.return_value = DummyResponse({"projected_total": 221.5})
        response = self.client.post("/projection", json={"away_team": "Boston Celtics", "home_team": "New York Knicks", "bookie_total": "999"})
        self.assertEqual(response.status_code, 200)
        post.assert_called_once_with(
            "http://127.0.0.1:8000/api/basketball/projection",
            json={"away_team": "Boston Celtics", "home_team": "New York Knicks"},
            timeout=25,
        )

    @patch("app.requests.get")
    def test_health_check_includes_backend_status(self, get):
        get.return_value = DummyResponse({"status": "ok"})
        response = self.client.get("/health-check")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["backend_status"], "ok")
        get.assert_called_once_with("http://127.0.0.1:8000/health", timeout=5)


if __name__ == "__main__":
    unittest.main()
