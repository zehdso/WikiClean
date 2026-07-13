import requests

from wikiclean.fetch import fetch_article


def test_timeout(monkeypatch):
    def fake_get(*args, **kwargs):
        raise requests.Timeout

    monkeypatch.setattr("wikiclean.fetch.requests.get", fake_get)

    assert fetch_article("Holi") is None


def test_connection_error(monkeypatch):
    def fake_get(*args, **kwargs):
        raise requests.ConnectionError

    monkeypatch.setattr("wikiclean.fetch.requests.get", fake_get)

    assert fetch_article("Holi") is None


def test_http_error(monkeypatch):
    class FakeResponse:
        def raise_for_status(self):
            raise requests.HTTPError("500 Server Error")

    monkeypatch.setattr(
        "wikiclean.fetch.requests.get",
        lambda *args, **kwargs: FakeResponse(),
    )

    assert fetch_article("Holi") is None


def test_invalid_json(monkeypatch):
    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            raise ValueError("Invalid JSON")

    monkeypatch.setattr(
        "wikiclean.fetch.requests.get",
        lambda *args, **kwargs: FakeResponse(),
    )

    assert fetch_article("Holi") is None


def test_missing_article(monkeypatch):
    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {
                "query": {
                    "pages": [
                        {
                            "title": "Missing",
                            "missing": True,
                        }
                    ]
                }
            }

    monkeypatch.setattr(
        "wikiclean.fetch.requests.get",
        lambda *args, **kwargs: FakeResponse(),
    )

    assert fetch_article("Missing") is None