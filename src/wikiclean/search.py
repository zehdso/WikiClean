import requests

API_URL = "https://en.wikipedia.org/w/api.php"

HEADERS = {
    "User-Agent": "WikiClean/0.1 (https://github.com/zehdso/WikiClean)"
}


def search(query: str):
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "format": "json",
    }

    response = requests.get(API_URL, params=params, headers=HEADERS)
    response.raise_for_status()

    results = response.json()["query"]["search"]

    if not results:
        return None

    article = results[0]

    return {
        "title": article["title"],
        "pageid": article["pageid"],
        "snippet": article["snippet"],
    }


if __name__ == "__main__":
    print(search("Holi"))

