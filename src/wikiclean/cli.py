from .fetch import fetch_article
from .filters import filter_article
from .input import resolve_input
from .output import format_output
from .parser import parse_article


def main():
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

    result = filter_article(parsed, option)

    if result is None:
        print("Option not found.")
        return

    output_format = input(
        "\nOutput format (json/text/markdown): "
    ).strip()

    try:
        print(format_output(result, output_format))
    except ValueError as error:
        print(error)


if __name__ == "__main__":
    main()