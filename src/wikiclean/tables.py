import re

from .cleaner import clean_wikitext


def _clean_cell(
    cell: str,
) -> str:
    cell = cell.strip()

    if "|" in cell:
        before, after = cell.split(
            "|",
            1,
        )

        before = before.strip()

        attribute_pattern = re.compile(
            r"""
            ^(?:
                [a-zA-Z_:][-a-zA-Z0-9_:]*
                \s*=
                .+
            )$
            """,
            re.VERBOSE | re.DOTALL,
        )

        if attribute_pattern.match(before):
            cell = after.strip()

    return clean_wikitext(cell)


def _split_cells(
    line: str,
    separator: str,
) -> list[str]:
    return [
        _clean_cell(cell)
        for cell in line.split(separator)
    ]


def extract_tables(
    wikitext: str,
) -> list[dict]:
    if not wikitext:
        return []

    raw_tables = re.findall(
        r"\{\|.*?\n\|\}",
        wikitext,
        flags=re.DOTALL,
    )

    tables = []

    for raw_table in raw_tables:
        headers = []
        rows = []
        current_row = []

        lines = raw_table.splitlines()

        for line in lines[1:-1]:
            line = line.strip()

            if not line:
                continue

            if line.startswith("|-"):
                if current_row:
                    rows.append(current_row)
                    current_row = []

                continue

            if line.startswith("|+"):
                continue

            if line.startswith("!"):
                header_line = line[1:]

                headers.extend(
                    _split_cells(
                        header_line,
                        "!!",
                    )
                )

                continue

            if line.startswith("|"):
                cell_line = line[1:]

                current_row.extend(
                    _split_cells(
                        cell_line,
                        "||",
                    )
                )

        if current_row:
            rows.append(current_row)

        tables.append({
            "headers": headers,
            "rows": rows,
        })

    return tables