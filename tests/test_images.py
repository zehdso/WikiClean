from wikiclean.images import extract_images


def test_extract_single_image():
    wikitext = """
[[File:Albert Einstein Head.jpg|thumb|Albert Einstein]]
"""

    result = extract_images(wikitext)

    assert result == [
        {
            "filename": "Albert Einstein Head.jpg",
            "options": [
                "thumb",
                "Albert Einstein",
            ],
        }
    ]


def test_no_images():
    wikitext = """
This article contains no images.
"""

    assert extract_images(wikitext) == []


def test_empty_wikitext():
    assert extract_images("") == []


def test_multiple_images():
    wikitext = """
[[File:First.jpg|thumb|First image]]

Article content.

[[File:Second.png|right|Second image]]
"""

    result = extract_images(wikitext)

    assert len(result) == 2

    assert result[0]["filename"] == "First.jpg"
    assert result[1]["filename"] == "Second.png"


def test_image_namespace():
    wikitext = """
[[Image:Example.jpg|thumb|Example image]]
"""

    result = extract_images(wikitext)

    assert result[0]["filename"] == "Example.jpg"


def test_case_insensitive_namespace():
    wikitext = """
[[FILE:Example.jpg|thumb]]
"""

    result = extract_images(wikitext)

    assert result[0]["filename"] == "Example.jpg"


def test_underscores_are_replaced():
    wikitext = """
[[File:Albert_Einstein_Head.jpg|thumb]]
"""

    result = extract_images(wikitext)

    assert (
        result[0]["filename"]
        == "Albert Einstein Head.jpg"
    )


def test_duplicate_images_are_removed():
    wikitext = """
[[File:Example.jpg|thumb]]
[[File:example.jpg|right]]
"""

    result = extract_images(wikitext)

    assert len(result) == 1
    assert result[0]["filename"] == "Example.jpg"


def test_image_without_options():
    wikitext = """
[[File:Example.jpg]]
"""

    result = extract_images(wikitext)

    assert result == [
        {
            "filename": "Example.jpg",
            "options": [],
        }
    ]


def test_nested_wikilink_in_caption():
    wikitext = """
[[File:Einstein.jpg|thumb|Albert and [[Elsa Einstein]] in 1921]]
"""

    result = extract_images(wikitext)

    assert result == [
        {
            "filename": "Einstein.jpg",
            "options": [
                "thumb",
                (
                    "Albert and [[Elsa Einstein]] "
                    "in 1921"
                ),
            ],
        }
    ]


def test_wikilink_pipe_in_caption():
    wikitext = """
[[File:Einstein.jpg|thumb|Einstein studied [[Physics|theoretical physics]]]]
"""

    result = extract_images(wikitext)

    assert result == [
        {
            "filename": "Einstein.jpg",
            "options": [
                "thumb",
                (
                    "Einstein studied "
                    "[[Physics|theoretical physics]]"
                ),
            ],
        }
    ]


def test_template_pipe_in_caption():
    wikitext = """
[[File:Einstein.jpg|thumb|Einstein at age {{age|1879|1955}}]]
"""

    result = extract_images(wikitext)

    assert result == [
        {
            "filename": "Einstein.jpg",
            "options": [
                "thumb",
                (
                    "Einstein at age "
                    "{{age|1879|1955}}"
                ),
            ],
        }
    ]


def test_nested_wikilink_and_template():
    wikitext = """
[[File:Einstein.jpg|thumb|[[Albert Einstein|Einstein]] at age {{age|1879|1955}}]]
"""

    result = extract_images(wikitext)

    assert result == [
        {
            "filename": "Einstein.jpg",
            "options": [
                "thumb",
                (
                    "[[Albert Einstein|Einstein]] "
                    "at age {{age|1879|1955}}"
                ),
            ],
        }
    ]