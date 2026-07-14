import html


def _escape(
    value,
) -> str:
    return html.escape(
        str(value or "")
    )


def _render_infobox(
    infobox,
) -> str:
    if not infobox:
        return ""

    infobox_type = _escape(
        infobox.get("type")
    )

    fields = infobox.get(
        "fields",
        {},
    )

    rows = []

    for key, value in fields.items():
        rows.append(
            f"""
            <div class="info-row">
                <strong>{_escape(key)}</strong>
                <span>{_escape(value)}</span>
            </div>
            """
        )

    return f"""
    <section class="card">
        <h2>Infobox</h2>
        <p class="muted">
            Type: {infobox_type}
        </p>

        <div class="info-list">
            {"".join(rows)}
        </div>
    </section>
    """


def _render_sections(
    sections,
) -> str:
    if not sections:
        return ""

    items = []

    for section in sections:
        title = _escape(
            section.get("title")
        )

        content = _escape(
            section.get("content")
        )

        level = _escape(
            section.get("level")
        )

        items.append(
            f"""
            <article class="section-item">
                <div class="section-heading">
                    <h3>{title}</h3>

                    <span class="badge">
                        Level {level}
                    </span>
                </div>

                <p>{content}</p>
            </article>
            """
        )

    return f"""
    <section class="card">
        <h2>Sections</h2>
        {"".join(items)}
    </section>
    """


def _render_tables(
    tables,
) -> str:
    if not tables:
        return ""

    rendered_tables = []

    for index, table in enumerate(
        tables,
        start=1,
    ):
        headers = table.get(
            "headers",
            [],
        )

        rows = table.get(
            "rows",
            [],
        )

        header_html = "".join(
            f"<th>{_escape(header)}</th>"
            for header in headers
        )

        rows_html = []

        for row in rows:
            cells = "".join(
                f"<td>{_escape(cell)}</td>"
                for cell in row
            )

            rows_html.append(
                f"<tr>{cells}</tr>"
            )

        rendered_tables.append(
            f"""
            <div class="table-block">
                <h3>Table {index}</h3>

                <div class="table-scroll">
                    <table>
                        <thead>
                            <tr>
                                {header_html}
                            </tr>
                        </thead>

                        <tbody>
                            {"".join(rows_html)}
                        </tbody>
                    </table>
                </div>
            </div>
            """
        )

    return f"""
    <section class="card">
        <h2>Tables</h2>
        {"".join(rendered_tables)}
    </section>
    """


def _render_images(
    images,
) -> str:
    if not images:
        return ""

    items = []

    for image in images:
        filename = _escape(
            image.get("filename")
        )

        image_url = _escape(
            image.get("url")
        )

        options = image.get(
            "options",
            [],
        )

        options_text = ", ".join(
            str(option)
            for option in options
        )

        if image_url:
            preview = f"""
                <img
                    src="{image_url}"
                    alt="{filename}"
                    loading="lazy"
                >
            """
        else:
            preview = """
                <div class="image-placeholder">
                    Image unavailable
                </div>
            """

        items.append(
            f"""
            <article class="image-item">
                {preview}

                <div class="image-details">
                    <strong>
                        {filename}
                    </strong>

                    <span>
                        {_escape(options_text)}
                    </span>
                </div>
            </article>
            """
        )

    return f"""
    <section class="card">
        <h2>Images</h2>

        <div class="image-list">
            {"".join(items)}
        </div>
    </section>
    """


def render_home() -> str:
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1"
    >

    <title>WikiClean</title>

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 24px;
            font-family:
                system-ui,
                -apple-system,
                BlinkMacSystemFont,
                "Segoe UI",
                sans-serif;
            background: #f5f5f5;
            color: #111;
        }

        main {
            width: 100%;
            max-width: 680px;
            padding: 40px;
            background: #fff;
            border: 1px solid #ddd;
            border-radius: 16px;
        }

        h1 {
            margin: 0 0 8px;
            font-size: 36px;
        }

        p {
            margin: 0 0 28px;
            color: #555;
            line-height: 1.6;
        }

        form {
            display: flex;
            gap: 10px;
        }

        input {
            flex: 1;
            min-width: 0;
            padding: 14px 16px;
            border: 1px solid #bbb;
            border-radius: 10px;
            font: inherit;
        }

        button {
            padding: 14px 20px;
            border: 0;
            border-radius: 10px;
            background: #111;
            color: #fff;
            font: inherit;
            cursor: pointer;
        }

        @media (max-width: 520px) {
            main {
                padding: 28px 20px;
            }

            form {
                flex-direction: column;
            }

            button {
                width: 100%;
            }
        }
    </style>
</head>

<body>
    <main>
        <h1>WikiClean</h1>

        <p>
            Transform Wikipedia articles into clean,
            structured, developer-friendly data.
        </p>

        <form
            action="/web/article"
            method="get"
        >
            <input
                type="text"
                name="q"
                placeholder="Enter a Wikipedia title"
                required
            >

            <button type="submit">
                Clean article
            </button>
        </form>
    </main>
</body>
</html>
"""


def render_article(
    result: dict,
) -> str:
    title = _escape(
        result.get("title")
    )

    summary = _escape(
        result.get("summary")
    )

    infobox_html = _render_infobox(
        result.get("infobox")
    )

    sections_html = _render_sections(
        result.get(
            "sections",
            [],
        )
    )

    tables_html = _render_tables(
        result.get(
            "tables",
            [],
        )
    )

    images_html = _render_images(
        result.get(
            "images",
            [],
        )
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1"
    >

    <title>{title} - WikiClean</title>

    <style>
        * {{
            box-sizing: border-box;
        }}

        body {{
            margin: 0;
            padding: 24px;
            font-family:
                system-ui,
                -apple-system,
                BlinkMacSystemFont,
                "Segoe UI",
                sans-serif;
            background: #f5f5f5;
            color: #111;
        }}

        main {{
            width: 100%;
            max-width: 1000px;
            margin: 0 auto;
        }}

        a {{
            color: #111;
        }}

        .top-link {{
            display: inline-block;
            margin-bottom: 20px;
        }}

        .card {{
            margin-bottom: 20px;
            padding: 28px;
            background: #fff;
            border: 1px solid #ddd;
            border-radius: 16px;
            overflow: hidden;
        }}

        h1 {{
            margin: 0;
            font-size: 38px;
        }}

        h2 {{
            margin: 0 0 20px;
        }}

        h3 {{
            margin: 0;
        }}

        p {{
            line-height: 1.7;
            white-space: pre-wrap;
            overflow-wrap: anywhere;
        }}

        .muted {{
            color: #666;
        }}

        .info-list {{
            display: grid;
            gap: 1px;
            background: #ddd;
            border: 1px solid #ddd;
            border-radius: 10px;
            overflow: hidden;
        }}

        .info-row {{
            display: grid;
            grid-template-columns:
                minmax(120px, 200px)
                1fr;
            gap: 16px;
            padding: 14px;
            background: #fff;
        }}

        .info-row span {{
            overflow-wrap: anywhere;
            white-space: pre-wrap;
        }}

        .section-item {{
            padding: 20px 0;
            border-top: 1px solid #ddd;
        }}

        .section-item:first-of-type {{
            border-top: 0;
            padding-top: 0;
        }}

        .section-heading {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
        }}

        .badge {{
            flex-shrink: 0;
            padding: 5px 9px;
            border-radius: 999px;
            background: #eee;
            color: #555;
            font-size: 12px;
        }}

        .table-block {{
            margin-top: 24px;
        }}

        .table-block:first-of-type {{
            margin-top: 0;
        }}

        .table-scroll {{
            margin-top: 12px;
            overflow-x: auto;
            border: 1px solid #ddd;
            border-radius: 10px;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            min-width: 600px;
        }}

        th,
        td {{
            padding: 12px;
            border-bottom: 1px solid #ddd;
            border-right: 1px solid #ddd;
            text-align: left;
            vertical-align: top;
            overflow-wrap: anywhere;
        }}

        th {{
            background: #f5f5f5;
        }}

        th:last-child,
        td:last-child {{
            border-right: 0;
        }}

        tbody tr:last-child td {{
            border-bottom: 0;
        }}

        .image-list {{
            display: grid;
            grid-template-columns:
                repeat(
                    auto-fill,
                    minmax(220px, 1fr)
                );
            gap: 16px;
        }}

        .image-item {{
            overflow: hidden;
            border: 1px solid #ddd;
            border-radius: 12px;
            background: #fff;
        }}

        .image-item img {{
            display: block;
            width: 100%;
            height: 220px;
            object-fit: contain;
            background: #f5f5f5;
        }}

        .image-placeholder {{
            display: flex;
            align-items: center;
            justify-content: center;
            height: 220px;
            padding: 20px;
            background: #f5f5f5;
            color: #777;
            text-align: center;
        }}

        .image-details {{
            padding: 14px;
        }}

        .image-details strong,
        .image-details span {{
            display: block;
            overflow-wrap: anywhere;
        }}

        .image-details span {{
            margin-top: 6px;
            color: #666;
            font-size: 14px;
        }}

        @media (max-width: 600px) {{
            body {{
                padding: 14px;
            }}

            .card {{
                padding: 20px;
            }}

            h1 {{
                font-size: 30px;
            }}

            .info-row {{
                grid-template-columns: 1fr;
                gap: 6px;
            }}

            .section-heading {{
                align-items: flex-start;
            }}

            .image-list {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>

<body>
    <main>
        <a
            class="top-link"
            href="/web"
        >
            ← Search another article
        </a>

        <section class="card">
            <h1>{title}</h1>
        </section>

        <section class="card">
            <h2>Summary</h2>
            <p>{summary}</p>
        </section>

        {infobox_html}

        {sections_html}

        {tables_html}

        {images_html}
    </main>
</body>
</html>
"""