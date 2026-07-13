from wikiclean.filters import filter_article
from wikiclean.metadata import extract_metadata
from wikiclean.output import format_output


def sample_article():
    return {
        "title": "Test",
        "pageid": 123,
        "url": "https://example.com/Test",
        "summary": "A test event happened in 2020.",
        "sections": [
            {
                "title": "History",
                "level": 1,
                "content": "In 2021, 50 people attended.",
            }
        ],
    }


def test_filter_section():
    result = filter_article(sample_article(), "History")

    assert result is not None
    assert result["results"][0]["section"]["title"] == "History"


def test_metadata_extraction():
    result = extract_metadata(sample_article())

    year_values = [item["value"] for item in result["years"]]
    number_values = [item["value"] for item in result["numbers"]]

    assert "2020" in year_values
    assert "2021" in year_values
    assert "50" in number_values
    assert "2020" not in number_values
    assert "2021" not in number_values


def test_json_output():
    result = format_output(
        {"title": "Test", "value": 123},
        "json",
    )

    assert '"title": "Test"' in result
    assert '"value": 123' in result