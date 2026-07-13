import requests

from wikiclean import search as search_module


class FakeResponse:
    def __init__(self, data):
        self.data = data

    def raise_for_status(self):
        pass

    def json(self):
        return self.data


def test_search_returns_first_result(monkeypatch):
    data = {
        "query": {
            "search": [
                {
                    "title": "Holi",
                    "pageid": 489575,
                    "snippet": (
                        '<span class="searchmatch">Holi</span> '
                        "is a festival."
                    ),
                }
            ]
        }
    }

    def fake_get(*args, **kwargs):
        return FakeResponse(data)

    monkeypatch.setattr(
        search_module.requests,
        "get",
        fake_get,
    )

    result = search_module.search("Holi")

    assert result == {
        "title": "Holi",
        "pageid": 489575,
        "snippet": "Holi is a festival.",
    }


def test_search_returns_none_when_empty(monkeypatch):
    data = {
        "query": {
            "search": []
        }
    }

    def fake_get(*args, **kwargs):
        return FakeResponse(data)

    monkeypatch.setattr(
        search_module.requests,
        "get",
        fake_get,
    )

    result = search_module.search("NotARealArticle")

    assert result is None


def test_search_decodes_html_entities(monkeypatch):
    data = {
        "query": {
            "search": [
                {
                    "title": "Test",
                    "pageid": 123,
                    "snippet": (
                        "Tom &amp; Jerry&#039;s "
                        "<span>history</span>"
                    ),
                }
            ]
        }
    }

    def fake_get(*args, **kwargs):
        return FakeResponse(data)

    monkeypatch.setattr(
        search_module.requests,
        "get",
        fake_get,
    )

    result = search_module.search("Test")

    assert result["snippet"] == "Tom & Jerry's history"


def test_search_propagates_network_error(monkeypatch):
    def fake_get(*args, **kwargs):
        raise requests.RequestException(
            "Network failure"
        )

    monkeypatch.setattr(
        search_module.requests,
        "get",
        fake_get,
    )

    try:
        search_module.search("Holi")
        assert False, "Expected RequestException"
    except requests.RequestException:
        pass