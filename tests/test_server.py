import json
import threading
import urllib.error
import urllib.request
from http.server import HTTPServer

from wikiclean import server


def start_test_server(monkeypatch, fake_get):
    monkeypatch.setattr(server, "get", fake_get)

    httpd = HTTPServer(
        ("127.0.0.1", 0),
        server.WikiCleanHandler,
    )

    thread = threading.Thread(
        target=httpd.serve_forever,
        daemon=True,
    )
    thread.start()

    return httpd


def request_json(httpd, path):
    port = httpd.server_address[1]

    try:
        with urllib.request.urlopen(
            f"http://127.0.0.1:{port}{path}"
        ) as response:
            return response.status, json.load(response)

    except urllib.error.HTTPError as error:
        return error.code, json.load(error)


def test_root(monkeypatch):
    httpd = start_test_server(
        monkeypatch,
        lambda article, section="summary": {},
    )

    try:
        status, data = request_json(httpd, "/")

        assert status == 200
        assert data["name"] == "WikiClean API"
        assert data["status"] == "ok"
    finally:
        httpd.shutdown()
        httpd.server_close()


def test_article(monkeypatch):
    def fake_get(article, section="summary"):
        return {
            "title": article,
            "section": section,
        }

    httpd = start_test_server(monkeypatch, fake_get)

    try:
        status, data = request_json(
            httpd,
            "/article/Holi?section=History",
        )

        assert status == 200
        assert data["title"] == "Holi"
        assert data["section"] == "History"
    finally:
        httpd.shutdown()
        httpd.server_close()


def test_article_not_found(monkeypatch):
    def fake_get(article, section="summary"):
        raise ValueError("Article not found.")

    httpd = start_test_server(monkeypatch, fake_get)

    try:
        status, data = request_json(
            httpd,
            "/article/Missing",
        )

        assert status == 404
        assert data["error"] == "Article not found."
    finally:
        httpd.shutdown()
        httpd.server_close()


def test_fetch_failure(monkeypatch):
    def fake_get(article, section="summary"):
        raise RuntimeError("Could not fetch the article.")

    httpd = start_test_server(monkeypatch, fake_get)

    try:
        status, data = request_json(
            httpd,
            "/article/Test",
        )

        assert status == 502
        assert data["error"] == "Could not fetch the article."
    finally:
        httpd.shutdown()
        httpd.server_close()


def test_route_not_found(monkeypatch):
    httpd = start_test_server(
        monkeypatch,
        lambda article, section="summary": {},
    )

    try:
        status, data = request_json(
            httpd,
            "/not-a-real-route",
        )

        assert status == 404
        assert data["error"] == "Route not found."
    finally:
        httpd.shutdown()
        httpd.server_close()