from wikiclean.tables import extract_tables


def test_extract_simple_table():
    wikitext = """
{| class="wikitable"
! Name !! Age
|-
| Alice || 30
|-
| Bob || 25
|}
"""

    result = extract_tables(wikitext)

    assert result == [
        {
            "headers": [
                "Name",
                "Age",
            ],
            "rows": [
                [
                    "Alice",
                    "30",
                ],
                [
                    "Bob",
                    "25",
                ],
            ],
        }
    ]


def test_no_tables():
    wikitext = """
This article contains no tables.
"""

    assert extract_tables(wikitext) == []


def test_empty_wikitext():
    assert extract_tables("") == []


def test_multiple_tables():
    wikitext = """
{| class="wikitable"
! Name !! Age
|-
| Alice || 30
|}

Some article text.

{| class="wikitable"
! City !! Country
|-
| Paris || France
|}
"""

    result = extract_tables(wikitext)

    assert len(result) == 2

    assert result[0]["headers"] == [
        "Name",
        "Age",
    ]

    assert result[1]["headers"] == [
        "City",
        "Country",
    ]


def test_multiline_cells():
    wikitext = """
{| class="wikitable"
! Name
! Description
|-
| Alice
| Software developer
|-
| Bob
| Scientist
|}
"""

    result = extract_tables(wikitext)

    assert result[0]["headers"] == [
        "Name",
        "Description",
    ]

    assert result[0]["rows"] == [
        [
            "Alice",
            "Software developer",
        ],
        [
            "Bob",
            "Scientist",
        ],
    ]


def test_table_caption_is_ignored():
    wikitext = """
{| class="wikitable"
|+ Example table
! Name !! Age
|-
| Alice || 30
|}
"""

    result = extract_tables(wikitext)

    assert result[0]["headers"] == [
        "Name",
        "Age",
    ]

    assert result[0]["rows"] == [
        [
            "Alice",
            "30",
        ]
    ]


def test_header_attributes_are_removed():
    wikitext = """
{| class="wikitable"
! style="width: 50%;" | Name
! style="width: 50%;" | Age
|-
| Alice
| 30
|}
"""

    result = extract_tables(wikitext)

    assert result[0]["headers"] == [
        "Name",
        "Age",
    ]


def test_cell_attributes_are_removed():
    wikitext = """
{| class="wikitable"
! Name !! Age
|-
| style="text-align: left;" | Alice
| style="text-align: center;" | 30
|}
"""

    result = extract_tables(wikitext)

    assert result[0]["rows"] == [
        [
            "Alice",
            "30",
        ]
    ]


def test_wikilink_pipes_are_cleaned():
    wikitext = """
{| class="wikitable"
! Person !! Field
|-
| [[Albert Einstein|Einstein]]
| [[Theoretical physics|Physics]]
|}
"""

    result = extract_tables(wikitext)

    assert result[0]["rows"] == [
        [
            "Einstein",
            "Physics",
        ]
    ]