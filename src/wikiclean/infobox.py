import re


def _find_infobox_end(
    wikitext: str,
    start: int,
) -> int | None:
    depth = 0
    i = start

    while i < len(wikitext) - 1:
        pair = wikitext[i:i + 2]

        if pair == "{{":
            depth += 1
            i += 2
            continue

        if pair == "}}":
            depth -= 1
            i += 2

            if depth == 0:
                return i

            continue

        i += 1

    return None


def _split_fields(
    content: str,
) -> list[str]:
    fields = []
    current = []

    template_depth = 0
    link_depth = 0

    i = 0

    while i < len(content):
        pair = content[i:i + 2]

        if pair == "{{":
            template_depth += 1
            current.append(pair)
            i += 2
            continue

        if pair == "}}" and template_depth > 0:
            template_depth -= 1
            current.append(pair)
            i += 2
            continue

        if pair == "[[":
            link_depth += 1
            current.append(pair)
            i += 2
            continue

        if pair == "]]" and link_depth > 0:
            link_depth -= 1
            current.append(pair)
            i += 2
            continue

        if (
            content[i] == "|"
            and template_depth == 0
            and link_depth == 0
        ):
            field = "".join(current).strip()

            if field:
                fields.append(field)

            current = []
            i += 1
            continue

        current.append(content[i])
        i += 1

    field = "".join(current).strip()

    if field:
        fields.append(field)

    return fields


def extract_infobox(
    wikitext: str,
) -> dict | None:
    if not wikitext:
        return None

    start = re.search(
        r"\{\{\s*Infobox\b",
        wikitext,
        re.IGNORECASE,
    )

    if start is None:
        return None

    position = start.start()

    end = _find_infobox_end(
        wikitext,
        position,
    )

    if end is None:
        return None

    raw_infobox = wikitext[
        position:end
    ]

    inner = raw_infobox[2:-2].strip()

    parts = _split_fields(inner)

    if not parts:
        return None

    header = parts[0].strip()

    infobox_type = re.sub(
        r"^Infobox\s*",
        "",
        header,
        flags=re.IGNORECASE,
    ).strip()

    fields = {}

    for field in parts[1:]:
        if "=" not in field:
            continue

        key, value = field.split(
            "=",
            1,
        )

        key = key.strip()
        value = value.strip()

        if key and value:
            fields[key] = value

    return {
        "type": infobox_type,
        "fields": fields,
    }