# WikiClean

Transform Wikipedia articles into clean, structured, developer-friendly data.

WikiClean accepts a Wikipedia article title, search term, or Wikipedia URL, fetches the content, cleans and parses it, and returns structured data through a CLI, Python API, HTTP API, or built-in web interface.

## Web Interface

After starting the WikiClean server, open:

```text
http://127.0.0.1:8000/web
```

> This is a local address and works on the device running WikiClean. A public deployment URL can be added here when WikiClean is hosted online.

The web interface lets users search for Wikipedia articles and view:

- Article summaries
- Infobox data
- Article sections
- Extracted tables
- Wikipedia images

## Features

- Search Wikipedia articles
- Return single or multiple search results
- Control the number of search results
- Fetch articles by title or search term
- Accept Wikipedia article URLs
- Extract clean article summaries
- Extract article sections
- Build hierarchical section trees
- Extract infoboxes
- Handle nested and multiline infobox values
- Extract Wikipedia tables
- Clean table cells and wiki links
- Extract image metadata
- Resolve real Wikimedia image URLs
- Display images in the web interface
- Extract metadata such as years and numbers with context
- Filter content by section
- Clean common Wikipedia markup
- Clean search-result snippets
- JSON output
- Plain-text output
- Markdown output
- Command-line interface
- Python API
- HTTP API
- Built-in web interface
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

## Web Interface

Start the server:

```bash
python -m wikiclean.server
```

Then visit:

```text
http://127.0.0.1:8000/web
```

Enter a Wikipedia article title, such as:

```text
Albert Einstein
```

WikiClean will fetch, parse, clean, and display the article in a structured web page.

## CLI Usage

### Get an Article

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

### Search Wikipedia

Return the first search result:

```bash
wikiclean search "Albert Einstein"
```

Example response:

```json
{
  "title": "Albert Einstein",
  "pageid": 736,
  "snippet": "Albert Einstein was a German-born theoretical physicist..."
}
```

### Multiple Search Results

Use `--limit` to control the number of results:

```bash
wikiclean search "Albert Einstein" --limit 5
```

Example response:

```json
{
  "query": "Albert Einstein",
  "count": 5,
  "results": [
    {
      "title": "Albert Einstein",
      "pageid": 736,
      "snippet": "Albert Einstein was a German-born theoretical physicist..."
    },
    {
      "title": "Hans Albert Einstein",
      "pageid": 1373258,
      "snippet": "Hans Albert Einstein was a Swiss-American engineer..."
    }
  ]
}
```

### Interactive Mode

Run WikiClean without arguments:

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

To retrieve the complete parsed article:

```python
import wikiclean

result = wikiclean.get(
    "Albert Einstein",
    section="all",
)

print(result)
```

The complete article result can include:

```text
title
pageid
url
summary
sections
section_tree
infobox
tables
images
metadata
```

### Infobox Example

```python
result = wikiclean.get(
    "Albert Einstein",
    section="all",
)

print(result["infobox"])
```

Example structure:

```json
{
  "type": "scientist",
  "fields": {
    "image": "Albert Einstein Head cleaned.jpg",
    "birth_place": "Ulm, Kingdom of Württemberg, German Empire",
    "fields": "Physics"
  }
}
```

### Table Example

```python
result = wikiclean.get(
    "List of countries by population (United Nations)",
    section="all",
)

print(result["tables"])
```

Example structure:

```json
[
  {
    "headers": [
      "Country or territory",
      "Population"
    ],
    "rows": [
      [
        "India",
        "1,438,069,596"
      ]
    ]
  }
]
```

### Image Example

```python
result = wikiclean.get(
    "Albert Einstein",
    section="all",
)

print(result["images"][:3])
```

Image results include the filename, Wikipedia image options, and resolved Wikimedia URL when available.

Example structure:

```json
[
  {
    "filename": "Albert Einstein as a child.jpg",
    "options": [
      "thumb",
      "upright=.9"
    ],
    "url": "https://upload.wikimedia.org/..."
  }
]
```

## HTTP API

Start the server:

```bash
python -m wikiclean.server
```

By default, WikiClean runs locally at:

```text
http://127.0.0.1:8000
```

### API Information

```text
GET /
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

### Search Wikipedia

Return the first search result:

```text
GET /v1/search?q=Albert+Einstein
```

Example response:

```json
{
  "title": "Albert Einstein",
  "pageid": 736,
  "snippet": "Albert Einstein was a German-born theoretical physicist..."
}
```

### Multiple Search Results

Use the `limit` parameter:

```text
GET /v1/search?q=Albert+Einstein&limit=5
```

Example response:

```json
{
  "query": "Albert Einstein",
  "count": 5,
  "results": [
    {
      "title": "Albert Einstein",
      "pageid": 736,
      "snippet": "Albert Einstein was a German-born theoretical physicist..."
    },
    {
      "title": "Hans Albert Einstein",
      "pageid": 1373258,
      "snippet": "Hans Albert Einstein was a Swiss-American engineer..."
    }
  ]
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

The older article route is also supported for backward compatibility:

```text
GET /article/Holi?section=History
```

## Example Article Response

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

## Infobox Extraction

WikiClean extracts the first Wikipedia infobox from an article's wikitext.

The infobox parser supports:

- Standard infobox fields
- Nested templates
- Deeply nested templates
- Multiline values
- Wiki links containing pipes
- Case-insensitive infobox detection
- Cleaning of common Wikipedia markup

## Table Extraction

WikiClean extracts Wikipedia wikitable data into structured headers and rows.

Example:

```json
{
  "headers": [
    "Person",
    "Field"
  ],
  "rows": [
    [
      "Einstein",
      "Physics"
    ]
  ]
}
```

Common wiki links, references, HTML tags, comments, and section markers are cleaned from table cells where supported.

## Image Extraction

WikiClean extracts image metadata from Wikipedia article wikitext.

For complete article requests using:

```python
section="all"
```

WikiClean can also resolve extracted filenames to real Wikimedia image URLs.

The built-in web interface displays these images in a responsive gallery.

## Wikitext Cleaning

WikiClean cleans common Wikipedia markup, including:

- HTML comments
- References
- Self-closing references
- Section markers
- Wiki links
- Wiki bold and italic formatting
- HTML tags
- HTML entities
- Non-breaking spaces
- Repeated whitespace

Some complex Wikipedia templates may remain in the output.

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
114 passed
```

## Project Status

WikiClean currently supports:

- [x] Wikipedia article search
- [x] Single search results
- [x] Multiple search results
- [x] Configurable search-result limits
- [x] Wikipedia article fetching
- [x] Article title and URL input
- [x] Clean search snippets
- [x] Clean text extraction
- [x] Section parsing
- [x] Hierarchical section trees
- [x] Infobox extraction
- [x] Nested and multiline infobox values
- [x] Table extraction
- [x] Table cell cleaning
- [x] Image metadata extraction
- [x] Wikimedia image URL resolution
- [x] Common wikitext cleaning
- [x] Metadata extraction
- [x] Section filtering
- [x] JSON output
- [x] Plain-text output
- [x] Markdown output
- [x] CLI
- [x] CLI search command
- [x] CLI multi-result search
- [x] Python API
- [x] HTTP API
- [x] HTTP search endpoint
- [x] HTTP multi-result search
- [x] Versioned API routes
- [x] Health endpoint
- [x] Web interface
- [x] Image gallery
- [x] Network and error handling
- [x] Automated tests

Future possibilities:

- [ ] More advanced Wikipedia template cleaning
- [ ] Improved table parsing for complex tables
- [ ] Image captions and richer image metadata
- [ ] Public web deployment

## License

MIT