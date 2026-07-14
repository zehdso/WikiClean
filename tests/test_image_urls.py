from wikiclean import image_urls


class FakeResponse:
    def __init__(
        self,
        data,
    ):
        self.data = data

    def raise_for_status(self):
        pass

    def json(self):
        return self.data


def test_get_image_url(
    monkeypatch,
):
    def fake_get(
        url,
        params,
        headers,
        timeout,
    ):
        return FakeResponse({
            "query": {
                "pages": [
                    {
                        "imageinfo": [
                            {
                                "url": (
                                    "https://upload."
                                    "wikimedia.org/"
                                    "example.jpg"
                                )
                            }
                        ]
                    }
                ]
            }
        })

    monkeypatch.setattr(
        image_urls.requests,
        "get",
        fake_get,
    )

    result = image_urls.get_image_url(
        "Example.jpg"
    )

    assert result == (
        "https://upload."
        "wikimedia.org/"
        "example.jpg"
    )


def test_get_image_url_empty_filename():
    assert (
        image_urls.get_image_url("")
        is None
    )


def test_get_image_url_no_pages(
    monkeypatch,
):
    def fake_get(
        url,
        params,
        headers,
        timeout,
    ):
        return FakeResponse({
            "query": {
                "pages": []
            }
        })

    monkeypatch.setattr(
        image_urls.requests,
        "get",
        fake_get,
    )

    assert (
        image_urls.get_image_url(
            "Missing.jpg"
        )
        is None
    )


def test_get_image_url_no_imageinfo(
    monkeypatch,
):
    def fake_get(
        url,
        params,
        headers,
        timeout,
    ):
        return FakeResponse({
            "query": {
                "pages": [
                    {}
                ]
            }
        })

    monkeypatch.setattr(
        image_urls.requests,
        "get",
        fake_get,
    )

    assert (
        image_urls.get_image_url(
            "Missing.jpg"
        )
        is None
    )


def test_add_image_urls(
    monkeypatch,
):
    def fake_get_image_url(
        filename,
    ):
        return (
            "https://example.com/"
            + filename
        )

    monkeypatch.setattr(
        image_urls,
        "get_image_url",
        fake_get_image_url,
    )

    images = [
        {
            "filename": "First.jpg",
            "options": ["thumb"],
        },
        {
            "filename": "Second.png",
            "options": [],
        },
    ]

    result = image_urls.add_image_urls(
        images
    )

    assert result == [
        {
            "filename": "First.jpg",
            "options": ["thumb"],
            "url": (
                "https://example.com/"
                "First.jpg"
            ),
        },
        {
            "filename": "Second.png",
            "options": [],
            "url": (
                "https://example.com/"
                "Second.png"
            ),
        },
    ]