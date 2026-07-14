import re


def _clean_filename(
    filename: str,
) -> str:
    return filename.strip().replace(
        "_",
        " ",
    )


def _find_image_end(
    wikitext: str,
    start: int,
) -> int | None:
    link_depth = 0
    i = start

    while i < len(wikitext) - 1:
        pair = wikitext[i:i + 2]

        if pair == "[[":
            link_depth += 1
            i += 2
            continue

        if pair == "]]":
            link_depth -= 1
            i += 2

            if link_depth == 0:
                return i

            continue

        i += 1

    return None


def _split_options(
    content: str,
) -> list[str]:
    options = []
    current = []

    link_depth = 0
    template_depth = 0

    i = 0

    while i < len(content):
        pair = content[i:i + 2]

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

        if (
            content[i] == "|"
            and link_depth == 0
            and template_depth == 0
        ):
            option = "".join(
                current
            ).strip()

            if option:
                options.append(option)

            current = []
            i += 1
            continue

        current.append(content[i])
        i += 1

    option = "".join(current).strip()

    if option:
        options.append(option)

    return options


def extract_images(
    wikitext: str,
) -> list[dict]:
    if not wikitext:
        return []

    start_pattern = re.compile(
        r"\[\[\s*(?:File|Image)\s*:",
        re.IGNORECASE,
    )

    images = []
    seen = set()

    position = 0

    while True:
        match = start_pattern.search(
            wikitext,
            position,
        )

        if match is None:
            break

        start = match.start()

        end = _find_image_end(
            wikitext,
            start,
        )

        if end is None:
            break

        raw_image = wikitext[
            start + 2:end - 2
        ]

        if ":" not in raw_image:
            position = end
            continue

        _, content = raw_image.split(
            ":",
            1,
        )

        parts = _split_options(
            content
        )

        if not parts:
            position = end
            continue

        filename = _clean_filename(
            parts[0]
        )

        if not filename:
            position = end
            continue

        key = filename.casefold()

        if key not in seen:
            seen.add(key)

            images.append({
                "filename": filename,
                "options": parts[1:],
            })

        position = end

    return images