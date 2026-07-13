import re


def build_section_tree(sections: list) -> list:
    tree = []
    stack = []

    for section in sections:
        node = {
            "title": section["title"],
            "level": section["level"],
            "content": section["content"],
            "children": [],
        }

        while stack and stack[-1]["level"] >= node["level"]:
            stack.pop()

        if stack:
            stack[-1]["children"].append(node)
        else:
            tree.append(node)

        stack.append(node)

    return tree


def parse_article(article: dict) -> dict:
    text = article.get("text", "")

    parts = re.split(
    r"(?:^|\n)(={2,6})\s*(.*?)\s*\1(?:\n|$)",
    text,
)

    summary = parts[0].strip()
    flat_sections = []

    for i in range(1, len(parts), 3):
        level_marks = parts[i]
        title = parts[i + 1].strip()
        content = parts[i + 2].strip()

        flat_sections.append({
            "title": title,
            "level": len(level_marks) - 1,
            "content": content,
        })

    return {
        "title": article.get("title"),
        "pageid": article.get("pageid"),
        "url": article.get("url"),
        "summary": summary,
        "sections": flat_sections,
        "section_tree": build_section_tree(flat_sections),
    }