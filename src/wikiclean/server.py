import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, unquote, urlparse

from .api import get


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

    def do_GET(self):
        parsed_url = urlparse(self.path)

        if parsed_url.path == "/":
            self.send_json({
                "name": "WikiClean API",
                "status": "ok",
            })
            return

        if parsed_url.path.startswith("/article/"):
            article = unquote(
                parsed_url.path[len("/article/"):]
            ).strip()

            if not article:
                self.send_json(
                    {"error": "Article is required."},
                    400,
                )
                return

            query = parse_qs(parsed_url.query)
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
                    {"error": str(error)},
                    404,
                )

            except RuntimeError as error:
                self.send_json(
                    {"error": str(error)},
                    502,
                )

            except Exception:
                self.send_json(
                    {"error": "Internal server error."},
                    500,
                )

            return

        self.send_json(
            {"error": "Route not found."},
            404,
        )


def run(host="127.0.0.1", port=8000):
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
        print("\nStopping WikiClean API.")
    finally:
        server.server_close()


if __name__ == "__main__":
    run()