# Tarsier

Tarsier is a Python library for web search and data extraction using headless browsers. It uses crawl4ai to search and extract data from web pages, and stores the results in both Meilisearch and Qdrant for efficient retrieval.

## Features

- Web search using headless browser
- Content extraction from web pages, PDFs, and images
- Support for text and markdown output formats
- Storage in Meilisearch for full-text search
- Vector storage in Qdrant for semantic search
- Docker support for easy deployment

## Installation

### Using Poetry

```bash
poetry install
```

### Using Docker

```bash
docker-compose up -d
```

## Usage

```python
from tarsier import TarsierSearcher

# Initialize the searcher
searcher = TarsierSearcher(
    meili_url="http://localhost:7700",
    qdrant_url="http://localhost:6333"
)

# Search and extract content
results = searcher.search(
    query="your search query",
    output_format="markdown",  # or "text"
    max_results=10
)

# Process results
for result in results:
    print(f"URL: {result['url']}")
    print(f"Content: {result['content']}\n")
```

## Development

1. Clone the repository
2. Install dependencies: `poetry install`
3. Run tests: `poetry run pytest`

## Docker Deployment

1. Build and start the services:
```bash
docker-compose up -d
```

2. Access the services:
- Meilisearch: http://localhost:7700
- Qdrant: http://localhost:6333

## License

MIT License
