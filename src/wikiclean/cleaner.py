import html
import re


def clean_wikitext(
    value: str,
) -> str:
    if not value:
        return ""

    text = str(value)

    text = re.sub(
        r"<!--.*?-->",
        "",
        text,
        flags=re.DOTALL,
    )

    text = re.sub(
        r"<ref\b[^>]*>.*?</ref\s*>",
        "",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )

    text = re.sub(
        r"<ref\b[^>]*/\s*>",
        "",
        text,
        flags=re.IGNORECASE,
    )

    text = re.sub(
        r"<section\b[^>]*/>",
        "",
        text,
        flags=re.IGNORECASE,
    )

    text = re.sub(
        r"\[\[([^|\]]+)\|([^\]]+)\]\]",
        r"\2",
        text,
    )

    text = re.sub(
        r"\[\[([^\]]+)\]\]",
        r"\1",
        text,
    )

    text = re.sub(
        r"'{2,5}",
        "",
        text,
    )

    text = re.sub(
        r"<[^>]+>",
        "",
        text,
    )

    text = html.unescape(text)
    text = text.replace("\xa0", " ")

    text = re.sub(
        r"[ \t]+",
        " ",
        text,
    )

    text = re.sub(
        r"\n\s*\n+",
        "\n",
        text,
    )

    return text.strip()