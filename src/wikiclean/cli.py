import argparse
import json
import sys

import requests

from .fetch import fetch_article
from .filters import filter_article
from .input import resolve_input
from .output import format_output
from .parser import parse_article
from .search import search


def process(user_input, option, output_format):
    title = resolve_input(user_input)

    if title is None:
        print(
            "Error: Article not found.",
            file=sys.stderr,
        )
        return 1

    article = fetch_article(title)

    if article is None:
        print(
            "Error: Could not fetch the article.",
            file=sys.stderr,
        )
        return 2

    parsed = parse_article(article)
    result = filter_article(parsed, option)

    if result is None:
        print(
            "Error: Option not found.",
            file=sys.stderr,
        )
        return 3

    try:
        print(
            format_output(
                result,
                output_format,
            )
        )
    except ValueError as error:
        print(
            f"Error: {error}",
            file=sys.stderr,
        )
        return 4

    return 0


def process_search(query):
    try:
        result = search(query)

    except requests.RequestException:
        print(
            "Error: Could not search Wikipedia.",
            file=sys.stderr,
        )
        return 2

    if result is None:
        print(
            "Error: No search results found.",
            file=sys.stderr,
        )
        return 1

    print(
        json.dumps(
            result,
            ensure_ascii=False,
            indent=2,
        )
    )

    return 0


def interactive_mode():
    user_input = input(
        "Enter a Wikipedia title or URL: "
    )

    title = resolve_input(user_input)

    if title is None:
        print(
            "Error: Article not found.",
            file=sys.stderr,
        )
        return 1

    article = fetch_article(title)

    if article is None:
        print(
            "Error: Could not fetch the article.",
            file=sys.stderr,
        )
        return 2

    parsed = parse_article(article)

    print("\nAvailable options:")
    print("• summary")
    print("• all")

    for section in parsed["sections"]:
        print(f'• {section["title"]}')

    option = input("\nWhat do you want? ")
    output_format = input(
        "\nOutput format (json/text/markdown): "
    ).strip()

    result = filter_article(
        parsed,
        option,
    )

    if result is None:
        print(
            "Error: Option not found.",
            file=sys.stderr,
        )
        return 3

    try:
        print(
            format_output(
                result,
                output_format,
            )
        )
    except ValueError as error:
        print(
            f"Error: {error}",
            file=sys.stderr,
        )
        return 4

    return 0


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Fetch, clean, and search "
            "Wikipedia articles."
        )
    )

    parser.add_argument(
        "article",
        nargs="?",
        help=(
            "Wikipedia article title, URL, "
            "or the 'search' command"
        ),
    )

    parser.add_argument(
        "query",
        nargs="?",
        help=(
            "Search query when using "
            "the 'search' command"
        ),
    )

    parser.add_argument(
        "-s",
        "--section",
        default="summary",
        help=(
            "Section to return "
            "(default: summary)"
        ),
    )

    parser.add_argument(
        "-f",
        "--format",
        default="text",
        choices=[
            "json",
            "text",
            "markdown",
        ],
        help=(
            "Output format "
            "(default: text)"
        ),
    )

    args = parser.parse_args()

    if args.article == "search":
        if not args.query:
            print(
                "Error: Search query is required.",
                file=sys.stderr,
            )
            return 1

        return process_search(args.query)

    if args.article is None:
        return interactive_mode()

    if args.query is not None:
        print(
            "Error: Unexpected argument.",
            file=sys.stderr,
        )
        return 1

    return process(
        args.article,
        args.section,
        args.format,
    )


if __name__ == "__main__":
    sys.exit(main())