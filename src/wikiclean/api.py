from .fetch import fetch_article
from .filters import filter_article
from .input import resolve_input
from .output import format_output
from .parser import parse_article


def get(
    article: str,
    section: str = "summary",
    output_format: str | None = None,
):
    title = resolve_input(article)

    if title is None:
        raise ValueError("Article not found.")

    fetched = fetch_article(title)

    if fetched is None:
        raise RuntimeError("Could not fetch the article.")

    parsed = parse_article(fetched)
    result = filter_article(parsed, section)

    if result is None:
        raise ValueError(f"Section not found: {section}")

    if output_format is None:
        return result

    return format_output(result, output_format)