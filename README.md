# WikiClean

Transform Wikipedia articles into clean, structured, developer-friendly data.

WikiClean accepts a Wikipedia article title or URL, fetches the article, cleans the content, parses its sections, and returns structured data through a CLI, Python API, or HTTP API.

## Features

- Fetch articles by Wikipedia title
- Accept Wikipedia article URLs
- Extract clean article summaries
- Extract article sections
- Build hierarchical section trees
- Extract metadata such as years and numbers with context
- Filter content by section
- JSON output
- Plain-text output
- Markdown output
- Command-line interface
- Python API
- HTTP API
- Versioned API routes
- Health endpoint
- Network and error handling
- Automated test suite

## Installation

Clone the repository:

```bash
git clone https://github.com/zehdso/WikiClean.git
cd WikiClean
```

Install the project:

```bash
python -m pip install -e .
```

## CLI Usage

Get the default article summary:

```bash
wikiclean Holi
```

Get a specific section:

```bash
wikiclean Holi --section History
```

Return JSON:

```bash
wikiclean Holi --section History --format json
```

Available output formats:

```text
text
json
markdown
```

You can also run WikiClean without arguments for interactive mode:

```bash
wikiclean
```

## Python API

```python
import wikiclean

result = wikiclean.get(
    "Holi",
    section="History",
    output_format="json",
)

print(result)
```

## HTTP API

Start the server:

```bash
python -m wikiclean.server
```

By default, the API runs at:

```text
http://127.0.0.1:8000
```

### Health Check

```text
GET /health
```

Example response:

```json
{
  "status": "ok"
}
```

### Get an Article

```text
GET /v1/article/Holi
```

### Get a Specific Section

```text
GET /v1/article/Holi?section=History
```

The older route is also supported for backward compatibility:

```text
GET /article/Holi?section=History
```

## Example JSON Response

```json
{
  "title": "Holi",
  "results": [
    {
      "requested": "History",
      "section": {
        "title": "History",
        "level": 1,
        "content": "..."
      }
    }
  ]
}
```

## Metadata

WikiClean can extract years and other numbers together with their surrounding context.

Example:

```json
{
  "years": [
    {
      "value": "1687",
      "context": "..."
    }
  ],
  "numbers": [
    {
      "value": "300",
      "context": "..."
    }
  ]
}
```

## Testing

Run the complete test suite:

```bash
pytest
```

Current test suite:

```text
26 passed
```

## Project Status

WikiClean currently supports:

- [x] Wikipedia article fetching
- [x] Article title and URL input
- [x] Clean text extraction
- [x] Section parsing
- [x] Hierarchical section trees
- [x] Metadata extraction
- [x] Section filtering
- [x] JSON output
- [x] Plain-text output
- [x] Markdown output
- [x] CLI
- [x] Python API
- [x] HTTP API
- [x] Versioned API routes
- [x] Health endpoint
- [x] Automated tests

Future possibilities:

- [ ] Article search
- [ ] Infobox extraction
- [ ] Table extraction
- [ ] Image metadata extraction
- [ ] Web interface

## License

MIT