import argparse

from .fetch import fetch_article
from .filters import filter_article
from .input import resolve_input
from .output import format_output
from .parser import parse_article


def process(user_input, option, output_format):
    title = resolve_input(user_input)

    if title is None:
        print("Article not found.")
        return

    article = fetch_article(title)

    if article is None:
        print("Could not fetch the article.")
        return

    parsed = parse_article(article)
    result = filter_article(parsed, option)

    if result is None:
        print("Option not found.")
        return

    try:
        print(format_output(result, output_format))
    except ValueError as error:
        print(error)


def interactive_mode():
    user_input = input("Enter a Wikipedia title or URL: ")

    title = resolve_input(user_input)

    if title is None:
        print("Article not found.")
        return

    article = fetch_article(title)

    if article is None:
        print("Could not fetch the article.")
        return

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

    result = filter_article(parsed, option)

    if result is None:
        print("Option not found.")
        return

    try:
        print(format_output(result, output_format))
    except ValueError as error:
        print(error)


def main():
    parser = argparse.ArgumentParser(
        description="Fetch and clean Wikipedia articles."
    )

    parser.add_argument(
        "article",
        nargs="?",
        help="Wikipedia article title or URL",
    )

    parser.add_argument(
        "-s",
        "--section",
        default="summary",
        help="Section to return (default: summary)",
    )

    parser.add_argument(
        "-f",
        "--format",
        default="text",
        choices=["json", "text", "markdown"],
        help="Output format (default: text)",
    )

    args = parser.parse_args()

    if args.article is None:
        interactive_mode()
    else:
        process(args.article, args.section, args.format)


if __name__ == "__main__":
    main()