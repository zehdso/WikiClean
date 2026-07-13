import argparse
import json
import sys

import requests

from .fetch import fetch_article
from .filters import filter_article
from .input import resolve_input
from .output import format_output
from .parser import parse_article
from .search import search, search_many


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


def process_search(query, limit=None):
    try:
        if limit is None:
            result = search(query)

            if result is None:
                print(
                    "Error: No search results found.",
                    file=sys.stderr,
                )
                return 1

        else:
            if limit < 1:
                print(
                    "Error: Limit must be at least 1.",
                    file=sys.stderr,
                )
                return 1

            results = search_many(
                query,
                limit=limit,
            )

            if not results:
                print(
                    "Error: No search results found.",
                    file=sys.stderr,
                )
                return 1

            result = {
                "query": query,
                "count": len(results),
                "results": results,
            }

    except requests.RequestException:
        print(
            "Error: Could not search Wikipedia.",
            file=sys.stderr,
        )
        return 2

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

    parser.add_argument(
        "-l",
        "--limit",
        type=int,
        help=(
            "Number of search results "
            "to return"
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

        return process_search(
            args.query,
            limit=args.limit,
        )

    if args.limit is not None:
        print(
            "Error: --limit can only be used "
            "with the search command.",
            file=sys.stderr,
        )
        return 1

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