from urllib.parse import unquote, urlparse

from search import search


def resolve_input(value: str) -> str | None:
    value = value.strip()

    # If the user provides a Wikipedia URL
    if value.startswith(("http://", "https://")):
        parsed_url = urlparse(value)

        if "wikipedia.org" not in parsed_url.netloc:
            raise ValueError("Only Wikipedia URLs are supported.")

        if not parsed_url.path.startswith("/wiki/"):
            raise ValueError("Invalid Wikipedia article URL.")

        title = parsed_url.path.removeprefix("/wiki/")
        return unquote(title).replace("_", " ")

    # If the user provides a title/search term
    result = search(value)

    if result is None:
        return None

    return result["title"]


if __name__ == "__main__":
    user_input = input("Enter a Wikipedia title or URL: ")

    title = resolve_input(user_input)

    if title:
        print("Resolved article:", title)
    else:
        print("Article not found.")