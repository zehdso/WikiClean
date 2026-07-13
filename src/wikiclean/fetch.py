import requests

API_URL = "https://en.wikipedia.org/w/api.php"

HEADERS = {
    "User-Agent": (
        "WikiClean/0.1 "
        "(https://github.com/zehdso/WikiClean)"
    )
}


def fetch_article(title: str) -> dict | None:
    params = {
        "action": "query",
        "prop": "extracts|revisions",
        "explaintext": True,
        "rvprop": "content",
        "rvslots": "main",
        "redirects": True,
        "titles": title,
        "format": "json",
        "formatversion": 2,
    }

    try:
        response = requests.get(
            API_URL,
            params=params,
            headers=HEADERS,
            timeout=15,
        )
        response.raise_for_status()
        data = response.json()

    except requests.Timeout:
        print(
            "Error: Wikipedia request timed out."
        )
        return None

    except requests.ConnectionError:
        print(
            "Error: Could not connect to Wikipedia."
        )
        return None

    except requests.HTTPError as error:
        print(
            "Error: Wikipedia returned an "
            f"HTTP error: {error}"
        )
        return None

    except requests.RequestException as error:
        print(
            "Error: Network request failed: "
            f"{error}"
        )
        return None

    except ValueError:
        print(
            "Error: Wikipedia returned an "
            "invalid response."
        )
        return None

    pages = data.get(
        "query",
        {},
    ).get(
        "pages",
        [],
    )

    if not pages:
        return None

    page = pages[0]

    if page.get("missing"):
        return None

    wikitext = ""

    revisions = page.get(
        "revisions",
        [],
    )

    if revisions:
        wikitext = (
            revisions[0]
            .get("slots", {})
            .get("main", {})
            .get("content", "")
        )

    return {
        "title": page.get("title"),
        "pageid": page.get("pageid"),
        "url": (
            "https://en.wikipedia.org/wiki/"
            + page.get(
                "title",
                "",
            ).replace(
                " ",
                "_",
            )
        ),
        "text": page.get(
            "extract",
            "",
        ),
        "wikitext": wikitext,
    }


if __name__ == "__main__":
    print(
        fetch_article(
            "Albert Einstein"
        )
    )