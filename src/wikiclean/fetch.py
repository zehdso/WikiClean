import requests

API_URL = "https://en.wikipedia.org/w/api.php"

HEADERS = {
    "User-Agent": "WikiClean/0.1 (https://github.com/zehdso/WikiClean)"
}


def fetch_article(title: str):
    params = {
        "action": "query",
        "prop": "extracts|categories|info",
        "titles": title,
        "explaintext": True,
        "inprop": "url",
        "cllimit": "max",
        "format": "json",
        "formatversion": 2,
    }

    response = requests.get(
        API_URL,
        params=params,
        headers=HEADERS,
        timeout=30,
    )
    response.raise_for_status()

    page = response.json()["query"]["pages"][0]

    if "missing" in page:
        return None

    return {
        "title": page["title"],
        "pageid": page["pageid"],
        "url": page.get("fullurl"),
        "text": page.get("extract", ""),
        "categories": [
            category["title"].removeprefix("Category:")
            for category in page.get("categories", [])
        ],
    }


if __name__ == "__main__":
    article = fetch_article("Holi")
    print(article)