import pytest

from wikiclean import api


SAMPLE_ARTICLE = {
    "title": "Test",
    "pageid": 123,
    "url": "https://example.com/Test",
    "text": (
        "Test summary.\n"
        "== History ==\n"
        "History content."
    ),
}


def test_get_returns_python_data(monkeypatch):
    monkeypatch.setattr(api, "resolve_input", lambda value: "Test")
    monkeypatch.setattr(api, "fetch_article", lambda title: SAMPLE_ARTICLE)

    result = api.get("Test", section="History")

    assert result["title"] == "Test"
    assert result["results"][0]["section"]["title"] == "History"


def test_get_returns_json(monkeypatch):
    monkeypatch.setattr(api, "resolve_input", lambda value: "Test")
    monkeypatch.setattr(api, "fetch_article", lambda title: SAMPLE_ARTICLE)

    result = api.get(
        "Test",
        section="History",
        output_format="json",
    )

    assert isinstance(result, str)
    assert '"title": "History"' in result


def test_article_not_found(monkeypatch):
    monkeypatch.setattr(api, "resolve_input", lambda value: None)

    with pytest.raises(ValueError, match="Article not found"):
        api.get("Missing")


def test_fetch_failure(monkeypatch):
    monkeypatch.setattr(api, "resolve_input", lambda value: "Test")
    monkeypatch.setattr(api, "fetch_article", lambda title: None)

    with pytest.raises(RuntimeError, match="Could not fetch"):
        api.get("Test")


def test_section_not_found(monkeypatch):
    monkeypatch.setattr(api, "resolve_input", lambda value: "Test")
    monkeypatch.setattr(api, "fetch_article", lambda title: SAMPLE_ARTICLE)

    with pytest.raises(ValueError, match="Section not found"):
        api.get("Test", section="NotARealSection")