from wikiclean.infobox import extract_infobox


def test_extract_infobox():
    wikitext = """
{{Infobox person
| name = Albert Einstein
| birth_date = 14 March 1879
| occupation = Physicist
}}
Article content.
"""

    result = extract_infobox(wikitext)

    assert result == {
        "type": "person",
        "fields": {
            "name": "Albert Einstein",
            "birth_date": "14 March 1879",
            "occupation": "Physicist",
        },
    }


def test_no_infobox():
    wikitext = """
This article has no infobox.
"""

    result = extract_infobox(wikitext)

    assert result is None


def test_empty_wikitext():
    assert extract_infobox("") is None


def test_nested_templates():
    wikitext = """
{{Infobox person
| name = Test Person
| birth_date = {{Birth date|2000|1|1}}
| occupation = Developer
}}
Article content.
"""

    result = extract_infobox(wikitext)

    assert result["type"] == "person"
    assert (
        result["fields"]["birth_date"]
        == "{{Birth date|2000|1|1}}"
    )
    assert (
        result["fields"]["occupation"]
        == "Developer"
    )


def test_case_insensitive_infobox():
    wikitext = """
{{INFOBOX person
| name = Test Person
}}
"""

    result = extract_infobox(wikitext)

    assert result["type"] == "person"
    assert (
        result["fields"]["name"]
        == "Test Person"
    )


def test_multiline_template_value():
    wikitext = """
{{Infobox person
| name = Test Person
| spouse = {{plainlist|
* {{marriage|Person One|2000|2010}}
* {{marriage|Person Two|2012}}
}}
| occupation = Developer
}}
"""

    result = extract_infobox(wikitext)

    spouse = result["fields"]["spouse"]

    assert "{{plainlist|" in spouse
    assert (
        "{{marriage|Person One|2000|2010}}"
        in spouse
    )
    assert (
        "{{marriage|Person Two|2012}}"
        in spouse
    )
    assert (
        result["fields"]["occupation"]
        == "Developer"
    )


def test_multiline_plain_value():
    wikitext = """
{{Infobox test
| name = Example
| description = First line
Second line
Third line
| status = Active
}}
"""

    result = extract_infobox(wikitext)

    assert (
        result["fields"]["description"]
        == "First line\nSecond line\nThird line"
    )
    assert (
        result["fields"]["status"]
        == "Active"
    )


def test_nested_links_with_pipes():
    wikitext = """
{{Infobox person
| name = [[Albert Einstein|Einstein]]
| field = [[Theoretical physics|Physics]]
}}
"""

    result = extract_infobox(wikitext)

    assert (
        result["fields"]["name"]
        == "[[Albert Einstein|Einstein]]"
    )
    assert (
        result["fields"]["field"]
        == "[[Theoretical physics|Physics]]"
    )


def test_deeply_nested_templates():
    wikitext = """
{{Infobox scientist
| name = Test Scientist
| awards = {{collapsible list|
{{plainlist|
* {{award|Prize One|2020}}
* {{award|Prize Two|2021}}
}}
}}
| field = Physics
}}
"""

    result = extract_infobox(wikitext)

    awards = result["fields"]["awards"]

    assert "{{collapsible list|" in awards
    assert "{{plainlist|" in awards
    assert "{{award|Prize One|2020}}" in awards
    assert "{{award|Prize Two|2021}}" in awards
    assert result["fields"]["field"] == "Physics"