from difflib import get_close_matches


def find_section(sections: list, option: str):
    option = option.strip().lower()

    # Exact match first
    for section in sections:
        if section["title"].lower() == option:
            return section, False

    # Fuzzy match for typos
    section_names = [section["title"].lower() for section in sections]

    matches = get_close_matches(
        option,
        section_names,
        n=1,
        cutoff=0.6,
    )

    if matches:
        matched_name = matches[0]

        for section in sections:
            if section["title"].lower() == matched_name:
                return section, True

    return None, False


def filter_article(article: dict, option: str):
    option = option.strip()

    if option.lower() == "all":
        return article

    if option.lower() == "summary":
        return {
            "title": article["title"],
            "summary": article["summary"],
        }

    # Split multiple requests by commas
    requested_options = [
        item.strip()
        for item in option.split(",")
        if item.strip()
    ]

    results = []

    for requested in requested_options:
        section, fuzzy_matched = find_section(
            article["sections"],
            requested,
        )

        if section:
            result = {
                "requested": requested,
                "section": section,
            }

            if fuzzy_matched:
                result["matched"] = section["title"]

            results.append(result)

    if not results:
        return None

    return {
        "title": article["title"],
        "results": results,
    }