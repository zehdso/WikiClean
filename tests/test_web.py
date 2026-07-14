from wikiclean.web import (
    render_article,
    render_home,
)


def test_render_home():
    result = render_home()

    assert "<!DOCTYPE html>" in result
    assert "<title>WikiClean</title>" in result
    assert "WikiClean" in result
    assert 'action="/web/article"' in result
    assert 'name="q"' in result


def test_render_home_has_search_form():
    result = render_home()

    assert "<form" in result
    assert 'method="get"' in result
    assert 'type="text"' in result
    assert "Clean article" in result


def test_render_article():
    result = render_article({
        "title": "Albert Einstein",
        "summary": (
            "Albert Einstein was a "
            "theoretical physicist."
        ),
    })

    assert (
        "<title>"
        "Albert Einstein - WikiClean"
        "</title>"
        in result
    )

    assert "<h1>Albert Einstein</h1>" in result

    assert (
        "Albert Einstein was a "
        "theoretical physicist."
        in result
    )


def test_render_article_escapes_title():
    result = render_article({
        "title": "<script>alert('x')</script>",
        "summary": "Safe summary.",
    })

    assert "<script>" not in result

    assert (
        "&lt;script&gt;"
        "alert(&#x27;x&#x27;)"
        "&lt;/script&gt;"
        in result
    )


def test_render_article_escapes_summary():
    result = render_article({
        "title": "Test",
        "summary": (
            "<script>alert('x')</script>"
        ),
    })

    assert "<script>" not in result

    assert (
        "&lt;script&gt;"
        "alert(&#x27;x&#x27;)"
        "&lt;/script&gt;"
        in result
    )


def test_render_article_handles_missing_data():
    result = render_article({})

    assert "<!DOCTYPE html>" in result
    assert "<h1></h1>" in result
    assert "<p></p>" in result


def test_render_article_has_back_link():
    result = render_article({
        "title": "Holi",
        "summary": "Holi is a festival.",
    })

    assert 'href="/web"' in result
    assert "Search another article" in result


def test_render_article_displays_image():
    result = render_article({
        "title": "Test",
        "summary": "Test article.",
        "images": [
            {
                "filename": "Example.jpg",
                "options": [
                    "thumb",
                    "Example image",
                ],
                "url": (
                    "https://upload."
                    "wikimedia.org/"
                    "example.jpg"
                ),
            }
        ],
    })

    assert "<h2>Images</h2>" in result

    assert (
        'src="https://upload.'
        'wikimedia.org/'
        'example.jpg"'
        in result
    )

    assert 'alt="Example.jpg"' in result
    assert 'loading="lazy"' in result
    assert "Example image" in result


def test_render_article_image_fallback():
    result = render_article({
        "title": "Test",
        "summary": "Test article.",
        "images": [
            {
                "filename": "Missing.jpg",
                "options": [],
                "url": None,
            }
        ],
    })

    assert "<h2>Images</h2>" in result
    assert "Missing.jpg" in result
    assert "Image unavailable" in result


def test_render_article_escapes_image_data():
    result = render_article({
        "title": "Test",
        "summary": "Test article.",
        "images": [
            {
                "filename": (
                    '<script>alert("x")</script>.jpg'
                ),
                "options": [
                    '<script>alert("y")</script>'
                ],
                "url": (
                    'https://example.com/'
                    '" onerror="alert(1)'
                ),
            }
        ],
    })

    assert "<script>" not in result
    assert 'onerror="alert(1)' not in result

    assert (
        "&lt;script&gt;"
        "alert(&quot;x&quot;)"
        "&lt;/script&gt;.jpg"
        in result
    )

    assert (
        "&lt;script&gt;"
        "alert(&quot;y&quot;)"
        "&lt;/script&gt;"
        in result
    )

    assert (
        "&quot; onerror="
        "&quot;alert(1)"
        in result
    )


def test_render_article_hides_empty_images():
    result = render_article({
        "title": "Test",
        "summary": "Test article.",
        "images": [],
    })

    assert "<h2>Images</h2>" not in result