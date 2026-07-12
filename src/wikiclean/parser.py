import re


def parse_article(article: dict) -> dict:
    text = article.get("text", "")

    # Split Wikipedia text by section headings like:
    # == History == or === Background ===
    parts = re.split(r"\n(={2,6})\s*(.*?)\s*\1\n", text)

    summary = parts[0].strip()
    sections = []

    # Each section produces: heading markers, title, content
    for i in range(1, len(parts), 3):
        level_marks = parts[i]
        title = parts[i + 1].strip()
        content = parts[i + 2].strip()

        sections.append({
            "title": title,
            "level": len(level_marks) - 1,
            "content": content,
        })

    return {
        "title": article.get("title"),
        "pageid": article.get("pageid"),
        "url": article.get("url"),
        "summary": summary,
        "sections": sections,
    }


if __name__ == "__main__":
    from fetch import fetch_article

    article = fetch_article("Holi")
    parsed = parse_article(article)

    print("Title:", parsed["title"])
    print("Summary:", parsed["summary"])
    print("\nSections:")

    for section in parsed["sections"]:
        print(
            f'{"  " * (section["level"] - 1)}'
            f'- {section["title"]}'
        )