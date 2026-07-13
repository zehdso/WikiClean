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
                        '<span class="searchmatch">'
                        "Holi"
                        "</span> is a festival."
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

    result = search_module.search(
        "NotARealArticle"
    )

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

    assert (
        result["snippet"]
        == "Tom & Jerry's history"
    )


def test_search_propagates_network_error(
    monkeypatch,
):
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


def test_search_many_returns_multiple_results(
    monkeypatch,
):
    data = {
        "query": {
            "search": [
                {
                    "title": "Albert Einstein",
                    "pageid": 736,
                    "snippet": (
                        "<span>Albert Einstein</span> "
                        "was a physicist."
                    ),
                },
                {
                    "title": "Hans Albert Einstein",
                    "pageid": 1373258,
                    "snippet": (
                        "Hans Albert Einstein "
                        "was an engineer."
                    ),
                },
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

    results = search_module.search_many(
        "Albert Einstein",
        limit=2,
    )

    assert len(results) == 2
    assert (
        results[0]["title"]
        == "Albert Einstein"
    )
    assert (
        results[1]["title"]
        == "Hans Albert Einstein"
    )


def test_search_many_sends_limit(
    monkeypatch,
):
    captured_params = {}

    data = {
        "query": {
            "search": []
        }
    }

    def fake_get(
        url,
        params=None,
        headers=None,
    ):
        captured_params.update(params)
        return FakeResponse(data)

    monkeypatch.setattr(
        search_module.requests,
        "get",
        fake_get,
    )

    search_module.search_many(
        "Einstein",
        limit=5,
    )

    assert captured_params["srlimit"] == 5


def test_search_many_cleans_snippets(
    monkeypatch,
):
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

    results = search_module.search_many(
        "Test",
        limit=5,
    )

    assert (
        results[0]["snippet"]
        == "Tom & Jerry's history"
    )


def test_search_many_rejects_invalid_limit():
    try:
        search_module.search_many(
            "Holi",
            limit=0,
        )
        assert False, "Expected ValueError"
    except ValueError as error:
        assert (
            str(error)
            == "Limit must be at least 1."
        )