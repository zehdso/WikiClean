import re


def extract_metadata(article: dict) -> dict:
    texts = [article.get("summary", "")]

    for section in article.get("sections", []):
        texts.append(section.get("content", ""))

    full_text = "\n".join(texts)

    sentences = re.split(r"(?<=[.!?])\s+", full_text)

    years = []
    numbers = []

    for sentence in sentences:
        found_years = re.findall(
            r"\b(?:1[0-9]{3}|20[0-9]{2}|2100)\b",
            sentence,
        )

        found_numbers = re.findall(
            r"\b\d+(?:\.\d+)?(?:%|K)?\b",
            sentence,
        )

        for year in found_years:
            years.append({
                "value": year,
                "context": sentence.strip(),
            })

        for number in found_numbers:
            if number not in found_years:
                numbers.append({
                    "value": number,
                    "context": sentence.strip(),
                })

    return {
        "pageid": article.get("pageid"),
        "url": article.get("url"),
        "years": years,
        "numbers": numbers,
    }