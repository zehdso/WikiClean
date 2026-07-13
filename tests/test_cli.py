import requests

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
    monkeypatch.setattr(
        cli,
        "resolve_input",
        lambda value: "Test",
    )
    monkeypatch.setattr(
        cli,
        "fetch_article",
        lambda title: SAMPLE_ARTICLE,
    )

    assert (
        cli.process(
            "Test",
            "History",
            "json",
        )
        == 0
    )


def test_article_not_found_exit_code(monkeypatch):
    monkeypatch.setattr(
        cli,
        "resolve_input",
        lambda value: None,
    )

    assert (
        cli.process(
            "Missing",
            "summary",
            "json",
        )
        == 1
    )


def test_fetch_failure_exit_code(monkeypatch):
    monkeypatch.setattr(
        cli,
        "resolve_input",
        lambda value: "Test",
    )
    monkeypatch.setattr(
        cli,
        "fetch_article",
        lambda title: None,
    )

    assert (
        cli.process(
            "Test",
            "summary",
            "json",
        )
        == 2
    )


def test_invalid_section_exit_code(monkeypatch):
    monkeypatch.setattr(
        cli,
        "resolve_input",
        lambda value: "Test",
    )
    monkeypatch.setattr(
        cli,
        "fetch_article",
        lambda title: SAMPLE_ARTICLE,
    )

    assert (
        cli.process(
            "Test",
            "NotARealSection",
            "json",
        )
        == 3
    )


def test_output_error_exit_code(monkeypatch):
    monkeypatch.setattr(
        cli,
        "resolve_input",
        lambda value: "Test",
    )
    monkeypatch.setattr(
        cli,
        "fetch_article",
        lambda title: SAMPLE_ARTICLE,
    )

    def fake_format_output(
        result,
        output_format,
    ):
        raise ValueError("Invalid format")

    monkeypatch.setattr(
        cli,
        "format_output",
        fake_format_output,
    )

    assert (
        cli.process(
            "Test",
            "summary",
            "json",
        )
        == 4
    )


def test_search_success(monkeypatch, capsys):
    def fake_search(query):
        return {
            "title": "Albert Einstein",
            "pageid": 736,
            "snippet": "German-born physicist.",
        }

    monkeypatch.setattr(
        cli,
        "search",
        fake_search,
    )

    exit_code = cli.process_search(
        "Albert Einstein"
    )

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Albert Einstein" in captured.out
    assert "736" in captured.out
    assert "German-born physicist." in captured.out


def test_search_no_results(monkeypatch, capsys):
    monkeypatch.setattr(
        cli,
        "search",
        lambda query: None,
    )

    exit_code = cli.process_search(
        "Nothing"
    )

    captured = capsys.readouterr()

    assert exit_code == 1
    assert (
        "Error: No search results found."
        in captured.err
    )


def test_search_network_failure(
    monkeypatch,
    capsys,
):
    def fake_search(query):
        raise requests.RequestException(
            "Network failure"
        )

    monkeypatch.setattr(
        cli,
        "search",
        fake_search,
    )

    exit_code = cli.process_search("Holi")

    captured = capsys.readouterr()

    assert exit_code == 2
    assert (
        "Error: Could not search Wikipedia."
        in captured.err
    )


def test_search_missing_query(
    monkeypatch,
    capsys,
):
    monkeypatch.setattr(
        "sys.argv",
        [
            "wikiclean",
            "search",
        ],
    )

    exit_code = cli.main()

    captured = capsys.readouterr()

    assert exit_code == 1
    assert (
        "Error: Search query is required."
        in captured.err
    )