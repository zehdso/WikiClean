import json


def format_output(data: dict, output_format: str = "json") -> str:
    output_format = output_format.strip().lower()

    if output_format == "json":
        return json.dumps(data, indent=2, ensure_ascii=False)

    if output_format == "text":
        return to_text(data)

    if output_format == "markdown":
        return to_markdown(data)

    raise ValueError(
        "Unsupported format. Choose: json, text, or markdown."
    )


def to_text(data: dict) -> str:
    lines = [data.get("title", "")]

    if "summary" in data:
        lines.extend(["", data["summary"]])

    if "results" in data:
        for result in data["results"]:
            section = result["section"]
            lines.extend([
                "",
                section["title"],
                section["content"],
            ])

    if "section" in data:
        section = data["section"]
        lines.extend([
            "",
            section["title"],
            section["content"],
        ])

    return "\n".join(lines)


def to_markdown(data: dict) -> str:
    lines = [f'# {data.get("title", "")}']

    if "summary" in data:
        lines.extend(["", data["summary"]])

    if "results" in data:
        for result in data["results"]:
            section = result["section"]
            level = section.get("level", 1) + 1

            lines.extend([
                "",
                f'{"#" * level} {section["title"]}',
                "",
                section["content"],
            ])

    if "section" in data:
        section = data["section"]
        level = section.get("level", 1) + 1

        lines.extend([
            "",
            f'{"#" * level} {section["title"]}',
            "",
            section["content"],
        ])

    return "\n".join(lines)