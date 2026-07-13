import html
import re

import requests


API_URL = "https://en.wikipedia.org/w/api.php"

HEADERS = {
    "User-Agent": (
        "WikiClean/0.1 "
        "(https://github.com/zehdso/WikiClean)"
    )
}


def clean_snippet(snippet: str) -> str:
    return html.unescape(
        re.sub(
            r"<[^>]+>",
            "",
            snippet,
        )
    )


def search_many(
    query: str,
    limit: int = 10,
) -> list[dict]:
    if limit < 1:
        raise ValueError(
            "Limit must be at least 1."
        )

    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "srlimit": limit,
        "format": "json",
    }

    response = requests.get(
        API_URL,
        params=params,
        headers=HEADERS,
    )
    response.raise_for_status()

    results = response.json()["query"]["search"]

    return [
        {
            "title": article["title"],
            "pageid": article["pageid"],
            "snippet": clean_snippet(
                article["snippet"]
            ),
        }
        for article in results
    ]


def search(query: str):
    results = search_many(
        query,
        limit=1,
    )

    if not results:
        return None

    return results[0]


if __name__ == "__main__":
    print(
        search_many(
            "Albert Einstein",
            limit=5,
        )
    )