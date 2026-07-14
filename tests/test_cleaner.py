from wikiclean.cleaner import clean_wikitext


def test_empty_value():
    assert clean_wikitext("") == ""


def test_removes_comments():
    value = (
        "Hello "
        "<!-- hidden comment -->"
        "World"
    )

    assert clean_wikitext(value) == "Hello World"


def test_removes_reference():
    value = (
        "Albert Einstein"
        "<ref>Reference text</ref>"
    )

    assert (
        clean_wikitext(value)
        == "Albert Einstein"
    )


def test_removes_self_closing_reference():
    value = (
        "Albert Einstein"
        '<ref name="test" />'
    )

    assert (
        clean_wikitext(value)
        == "Albert Einstein"
    )


def test_removes_section_tags():
    value = (
        '<section begin="population" />'
        "1,438,069,596"
        '<section end="population" />'
    )

    assert (
        clean_wikitext(value)
        == "1,438,069,596"
    )


def test_cleans_piped_link():
    value = (
        "[[Albert Einstein|Einstein]]"
    )

    assert clean_wikitext(value) == "Einstein"


def test_cleans_simple_link():
    value = "[[Physics]]"

    assert clean_wikitext(value) == "Physics"


def test_removes_wiki_formatting():
    value = (
        "'''Albert Einstein''' was "
        "a ''physicist''."
    )

    assert (
        clean_wikitext(value)
        == "Albert Einstein was "
        "a physicist."
    )


def test_decodes_html_entities():
    value = (
        "German&nbsp;Empire "
        "&amp; Switzerland"
    )

    assert (
        clean_wikitext(value)
        == "German Empire "
        "& Switzerland"
    )


def test_removes_html_tags():
    value = (
        "E=mc<sup>2</sup>"
    )

    assert clean_wikitext(value) == "E=mc2"


def test_normalizes_spaces():
    value = "Hello     World"

    assert clean_wikitext(value) == "Hello World"


def test_combined_cleaning():
    value = (
        "'''[[Albert Einstein|Einstein]]''' "
        "was a [[Physics|physicist]]"
        "<ref>Source</ref>."
    )

    assert (
        clean_wikitext(value)
        == "Einstein was a physicist."
    )