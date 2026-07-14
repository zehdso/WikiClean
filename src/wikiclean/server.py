import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, unquote, urlparse

import requests

from .api import get
from .search import search, search_many
from .web import render_article, render_home


class WikiCleanHandler(BaseHTTPRequestHandler):
    def send_json(self, data, status=200):
        body = json.dumps(
            data,
            ensure_ascii=False,
            indent=2,
        ).encode("utf-8")

        self.send_response(status)
        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8",
        )
        self.send_header(
            "Content-Length",
            str(len(body)),
        )
        self.end_headers()
        self.wfile.write(body)

    def send_html(self, content, status=200):
        body = content.encode("utf-8")

        self.send_response(status)
        self.send_header(
            "Content-Type",
            "text/html; charset=utf-8",
        )
        self.send_header(
            "Content-Length",
            str(len(body)),
        )
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed_url = urlparse(self.path)

        if parsed_url.path == "/":
            self.send_json({
                "name": "WikiClean API",
                "version": "1",
                "status": "ok",
            })
            return

        if parsed_url.path == "/health":
            self.send_json({
                "status": "ok",
            })
            return

        if parsed_url.path == "/web":
            self.send_html(
                render_home()
            )
            return

        if parsed_url.path == "/web/article":
            query_params = parse_qs(
                parsed_url.query
            )

            query = query_params.get(
                "q",
                [""],
            )[0].strip()

            if not query:
                self.send_html(
                    render_home(),
                    400,
                )
                return

            try:
                result = get(
                    query,
                    section="all",
                )

                self.send_html(
                    render_article(result)
                )

            except ValueError:
                self.send_html(
                    render_article({
                        "title": "Article not found",
                        "summary": (
                            "The requested Wikipedia "
                            "article could not be found."
                        ),
                    }),
                    404,
                )

            except RuntimeError:
                self.send_html(
                    render_article({
                        "title": "Wikipedia unavailable",
                        "summary": (
                            "WikiClean could not fetch "
                            "the article from Wikipedia."
                        ),
                    }),
                    502,
                )

            except Exception:
                self.send_html(
                    render_article({
                        "title": "Internal server error",
                        "summary": (
                            "WikiClean could not process "
                            "this request."
                        ),
                    }),
                    500,
                )

            return

        if parsed_url.path == "/v1/search":
            query_params = parse_qs(
                parsed_url.query
            )

            query = query_params.get(
                "q",
                [""],
            )[0].strip()

            if not query:
                self.send_json(
                    {
                        "error": (
                            "Search query is required."
                        )
                    },
                    400,
                )
                return

            limit_value = query_params.get(
                "limit"
            )

            try:
                if limit_value is None:
                    result = search(query)

                    if result is None:
                        self.send_json(
                            {
                                "error": (
                                    "No search results found."
                                )
                            },
                            404,
                        )
                        return

                    self.send_json(result)
                    return

                try:
                    limit = int(
                        limit_value[0]
                    )
                except ValueError:
                    self.send_json(
                        {
                            "error": (
                                "Limit must be an integer."
                            )
                        },
                        400,
                    )
                    return

                if limit < 1:
                    self.send_json(
                        {
                            "error": (
                                "Limit must be at least 1."
                            )
                        },
                        400,
                    )
                    return

                results = search_many(
                    query,
                    limit=limit,
                )

                if not results:
                    self.send_json(
                        {
                            "error": (
                                "No search results found."
                            )
                        },
                        404,
                    )
                    return

                self.send_json({
                    "query": query,
                    "count": len(results),
                    "results": results,
                })

            except requests.RequestException:
                self.send_json(
                    {
                        "error": (
                            "Could not search Wikipedia."
                        )
                    },
                    502,
                )

            except Exception:
                self.send_json(
                    {
                        "error": (
                            "Internal server error."
                        )
                    },
                    500,
                )

            return

        article_prefixes = (
            "/v1/article/",
            "/article/",
        )

        prefix = next(
            (
                item
                for item in article_prefixes
                if parsed_url.path.startswith(item)
            ),
            None,
        )

        if prefix is not None:
            article = unquote(
                parsed_url.path[len(prefix):]
            ).strip()

            if not article:
                self.send_json(
                    {
                        "error": (
                            "Article is required."
                        )
                    },
                    400,
                )
                return

            query = parse_qs(
                parsed_url.query
            )

            section = query.get(
                "section",
                ["summary"],
            )[0]

            try:
                result = get(
                    article,
                    section=section,
                )
                self.send_json(result)

            except ValueError as error:
                self.send_json(
                    {
                        "error": str(error)
                    },
                    404,
                )

            except RuntimeError as error:
                self.send_json(
                    {
                        "error": str(error)
                    },
                    502,
                )

            except Exception:
                self.send_json(
                    {
                        "error": (
                            "Internal server error."
                        )
                    },
                    500,
                )

            return

        self.send_json(
            {
                "error": (
                    "Route not found."
                )
            },
            404,
        )


def run(
    host="127.0.0.1",
    port=8000,
):
    server = HTTPServer(
        (host, port),
        WikiCleanHandler,
    )

    print(
        f"WikiClean API running on "
        f"http://{host}:{port}"
    )

    try:
        server.serve_forever()

    except KeyboardInterrupt:
        print(
            "\nStopping WikiClean API."
        )

    finally:
        server.server_close()


if __name__ == "__main__":
    run(
        host="0.0.0.0",
        port=int(
            os.environ.get(
                "PORT",
                "8000",
            )
        ),
    )