import requests


API_URL = "https://en.wikipedia.org/w/api.php"

HEADERS = {
    "User-Agent": (
        "WikiClean/0.1 "
        "(https://github.com/zehdso/WikiClean)"
    )
}


def get_image_url(
    filename: str,
) -> str | None:
    if not filename:
        return None

    params = {
        "action": "query",
        "prop": "imageinfo",
        "iiprop": "url",
        "titles": f"File:{filename}",
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

    except (
        requests.RequestException,
        ValueError,
    ):
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

    imageinfo = pages[0].get(
        "imageinfo",
        [],
    )

    if not imageinfo:
        return None

    return imageinfo[0].get("url")


def add_image_urls(
    images: list[dict],
) -> list[dict]:
    enriched = []

    for image in images:
        item = dict(image)

        item["url"] = get_image_url(
            str(
                image.get(
                    "filename",
                    "",
                )
            )
        )

        enriched.append(item)

    return enriched