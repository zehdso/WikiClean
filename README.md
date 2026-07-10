# WikiClean

Transform Wikipedia articles into clean, structured, developer-friendly data.

WikiClean accepts either a Wikipedia URL or an article title and extracts clean information such as summaries, sections, infoboxes, references, tables, images, and statistics.

## Features

- Search by article title
- Parse Wikipedia URLs
- Clean wiki markup
- Extract plain text
- Structured JSON output
- Markdown export
- HTML export
- Section extraction
- Infobox extraction
- Statistics (words, characters, reading time)
- Optional citation removal
- Developer-friendly API
- CLI support

## Example

Input

```text
Holi
```

or

```text
https://en.wikipedia.org/wiki/Holi
```

Output

```json
{
  "title": "Holi",
  "summary": "...",
  "sections": [...],
  "infobox": {...}
}
```

## Roadmap

- [ ] Search articles
- [ ] Parse wiki pages
- [ ] Extract clean text
- [ ] JSON output
- [ ] Filters
- [ ] REST API
- [ ] CLI
- [ ] Web interface

## License

MIT