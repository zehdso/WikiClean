from wikiclean import cli


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


def test_success_exit_code(monkeypatch):
    monkeypatch.setattr(cli, "resolve_input", lambda value: "Test")
    monkeypatch.setattr(cli, "fetch_article", lambda title: SAMPLE_ARTICLE)

    assert cli.process("Test", "History", "json") == 0


def test_article_not_found_exit_code(monkeypatch):
    monkeypatch.setattr(cli, "resolve_input", lambda value: None)

    assert cli.process("Missing", "summary", "json") == 1


def test_fetch_failure_exit_code(monkeypatch):
    monkeypatch.setattr(cli, "resolve_input", lambda value: "Test")
    monkeypatch.setattr(cli, "fetch_article", lambda title: None)

    assert cli.process("Test", "summary", "json") == 2


def test_invalid_section_exit_code(monkeypatch):
    monkeypatch.setattr(cli, "resolve_input", lambda value: "Test")
    monkeypatch.setattr(cli, "fetch_article", lambda title: SAMPLE_ARTICLE)

    assert cli.process("Test", "NotARealSection", "json") == 3


def test_output_error_exit_code(monkeypatch):
    monkeypatch.setattr(cli, "resolve_input", lambda value: "Test")
    monkeypatch.setattr(cli, "fetch_article", lambda title: SAMPLE_ARTICLE)

    def fake_format_output(result, output_format):
        raise ValueError("Invalid format")

    monkeypatch.setattr(cli, "format_output", fake_format_output)

    assert cli.process("Test", "summary", "json") == 4