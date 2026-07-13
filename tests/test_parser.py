from wikiclean.parser import parse_article


def test_parse_article():
    article = {
        "title": "Test",
        "pageid": 123,
        "url": "https://example.com/Test",
        "text": (
            "This is the summary.\n"
            "== History ==\n"
            "History content.\n"
            "=== Early history ===\n"
            "Early history content."
        ),
    }

    result = parse_article(article)

    assert result["title"] == "Test"
    assert result["summary"] == "This is the summary."
    assert len(result["sections"]) == 2

    assert result["sections"][0]["title"] == "History"
    assert result["sections"][1]["title"] == "Early history"

    assert result["section_tree"][0]["title"] == "History"
    assert result["section_tree"][0]["children"][0]["title"] == "Early history"