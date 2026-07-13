import json
import threading
import urllib.error
import urllib.request
from http.server import HTTPServer

import requests

from wikiclean import server


def start_test_server(
    monkeypatch,
    fake_get,
    fake_search=None,
    fake_search_many=None,
):
    monkeypatch.setattr(
        server,
        "get",
        fake_get,
    )

    if fake_search is not None:
        monkeypatch.setattr(
            server,
            "search",
            fake_search,
        )

    if fake_search_many is not None:
        monkeypatch.setattr(
            server,
            "search_many",
            fake_search_many,
        )

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
        status, data = request_json(
            httpd,
            "/",
        )

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

    httpd = start_test_server(
        monkeypatch,
        fake_get,
    )

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
        raise ValueError(
            "Article not found."
        )

    httpd = start_test_server(
        monkeypatch,
        fake_get,
    )

    try:
        status, data = request_json(
            httpd,
            "/article/Missing",
        )

        assert status == 404
        assert (
            data["error"]
            == "Article not found."
        )
    finally:
        httpd.shutdown()
        httpd.server_close()


def test_fetch_failure(monkeypatch):
    def fake_get(article, section="summary"):
        raise RuntimeError(
            "Could not fetch the article."
        )

    httpd = start_test_server(
        monkeypatch,
        fake_get,
    )

    try:
        status, data = request_json(
            httpd,
            "/article/Test",
        )

        assert status == 502
        assert (
            data["error"]
            == "Could not fetch the article."
        )
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
        assert (
            data["error"]
            == "Route not found."
        )
    finally:
        httpd.shutdown()
        httpd.server_close()


def test_health(monkeypatch):
    httpd = start_test_server(
        monkeypatch,
        lambda article, section="summary": {},
    )

    try:
        status, data = request_json(
            httpd,
            "/health",
        )

        assert status == 200
        assert data["status"] == "ok"
    finally:
        httpd.shutdown()
        httpd.server_close()


def test_v1_article(monkeypatch):
    def fake_get(article, section="summary"):
        return {
            "title": article,
            "section": section,
        }

    httpd = start_test_server(
        monkeypatch,
        fake_get,
    )

    try:
        status, data = request_json(
            httpd,
            "/v1/article/Holi?section=History",
        )

        assert status == 200
        assert data["title"] == "Holi"
        assert data["section"] == "History"
    finally:
        httpd.shutdown()
        httpd.server_close()


def test_search_success(monkeypatch):
    def fake_search(query):
        return {
            "title": "Holi",
            "pageid": 489575,
            "snippet": "Holi is a festival.",
        }

    httpd = start_test_server(
        monkeypatch,
        lambda article, section="summary": {},
        fake_search=fake_search,
    )

    try:
        status, data = request_json(
            httpd,
            "/v1/search?q=Holi",
        )

        assert status == 200
        assert data["title"] == "Holi"
        assert data["pageid"] == 489575
        assert (
            data["snippet"]
            == "Holi is a festival."
        )
    finally:
        httpd.shutdown()
        httpd.server_close()


def test_search_missing_query(monkeypatch):
    httpd = start_test_server(
        monkeypatch,
        lambda article, section="summary": {},
    )

    try:
        status, data = request_json(
            httpd,
            "/v1/search",
        )

        assert status == 400
        assert (
            data["error"]
            == "Search query is required."
        )
    finally:
        httpd.shutdown()
        httpd.server_close()


def test_search_no_results(monkeypatch):
    def fake_search(query):
        return None

    httpd = start_test_server(
        monkeypatch,
        lambda article, section="summary": {},
        fake_search=fake_search,
    )

    try:
        status, data = request_json(
            httpd,
            "/v1/search?q=Nothing",
        )

        assert status == 404
        assert (
            data["error"]
            == "No search results found."
        )
    finally:
        httpd.shutdown()
        httpd.server_close()


def test_search_network_failure(monkeypatch):
    def fake_search(query):
        raise requests.RequestException(
            "Network failure"
        )

    httpd = start_test_server(
        monkeypatch,
        lambda article, section="summary": {},
        fake_search=fake_search,
    )

    try:
        status, data = request_json(
            httpd,
            "/v1/search?q=Holi",
        )

        assert status == 502
        assert (
            data["error"]
            == "Could not search Wikipedia."
        )
    finally:
        httpd.shutdown()
        httpd.server_close()


def test_search_multiple_results(monkeypatch):
    def fake_search_many(query, limit=10):
        return [
            {
                "title": "Albert Einstein",
                "pageid": 736,
                "snippet": "A physicist.",
            },
            {
                "title": "Hans Albert Einstein",
                "pageid": 1373258,
                "snippet": "An engineer.",
            },
        ]

    httpd = start_test_server(
        monkeypatch,
        lambda article, section="summary": {},
        fake_search_many=fake_search_many,
    )

    try:
        status, data = request_json(
            httpd,
            "/v1/search?q=Einstein&limit=2",
        )

        assert status == 200
        assert data["query"] == "Einstein"
        assert data["count"] == 2
        assert len(data["results"]) == 2
        assert (
            data["results"][0]["title"]
            == "Albert Einstein"
        )
    finally:
        httpd.shutdown()
        httpd.server_close()


def test_search_invalid_limit(monkeypatch):
    httpd = start_test_server(
        monkeypatch,
        lambda article, section="summary": {},
    )

    try:
        status, data = request_json(
            httpd,
            "/v1/search?q=Einstein&limit=abc",
        )

        assert status == 400
        assert (
            data["error"]
            == "Limit must be an integer."
        )
    finally:
        httpd.shutdown()
        httpd.server_close()


def test_search_limit_below_one(monkeypatch):
    httpd = start_test_server(
        monkeypatch,
        lambda article, section="summary": {},
    )

    try:
        status, data = request_json(
            httpd,
            "/v1/search?q=Einstein&limit=0",
        )

        assert status == 400
        assert (
            data["error"]
            == "Limit must be at least 1."
        )
    finally:
        httpd.shutdown()
        httpd.server_close()