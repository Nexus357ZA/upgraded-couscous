# Upgraded Couscous

A Flask-based news aggregator that fetches articles from [NewsAPI](https://newsapi.org/) and displays them in a clean, responsive grid with infinite scrolling.

## Features

- **Latest feed** — Broad news feed via `/v2/everything` endpoint
- **Category browsing** — Technology, Business, General, Health, Science, Entertainment, Sports (via `/v2/top-headlines`)
- **Infinite scrolling** — Loads 9 articles at a time as you scroll
- **User preferences** — Persisted as a cookie:
  - Language selection (9 supported languages)
  - Hide/show individual news sources
- **Responsive design** — CSS Grid layout adapts to screen size
- **Debug endpoint** — `/debug-newsapi` for API troubleshooting

## Prerequisites

- Python 3.14+
- pip or uv (optional, for dependency management)

## Installation

### Using pip

```bash
pip install -r requirements.txt
```

### Using uv (recommended)

```bash
uv sync
```

### Configuration

Create a `.env` file in the project root with your NewsAPI key:

```bash
NEWSAPI_KEY=your_newsapi_api_key_here
```

You can get a free API key from [NewsAPI](https://newsapi.org/register).

## Running the Application

### With pip

```bash
python -m run
```

Or directly:

```bash
cd /Users/stefan/PycharmProjects/upgraded-couscous && python run.py
```

The app will start at `http://localhost:8080` (or PORT if set via environment variable).

### With uv

```bash
uv run run.py
```

## Usage

Once running, visit:

- **Main page**: `http://localhost:8080/` — Displays news articles in a grid
- **Category tabs** — Click a category to filter by topic
- **Preferences** — Click the gear icon to change language or hide sources
- **Infinite scroll** — Scroll down to load more articles
- **Debug endpoint**: `http://localhost:8080/debug-newsapi` — Raw API response for troubleshooting

## API Endpoints

- `GET /` or `GET /index?category=latest` — Main page
- `GET /api/articles?page=1&per_page=9&category=latest` — Paginated JSON for infinite scroll
- `POST /api/preferences` — Save user preferences (JSON body: `{"language":"en","excluded_sources":[]}`)
- `GET /debug-newsapi` — Raw NewsAPI response

## Project Structure

```
upgraded-couscous/
├── app/
│   ├── __init__.py           # Flask app factory
│   ├── errors/                # Error handlers
│   ├── main/                  # Main routes and NewsAPI client
│   │   ├── __init__.py
│   │   └── routes.py          # Route definitions, API, preferences
│   └── models.py              # Article data model
├── app/templates/             # Jinja2 templates
│   ├── base.html              # Base template with navbar
│   ├── index.html             # Home page layout with infinite scroll
│   └── errors/
│       ├── 404.html
│       └── 500.html
├── config.py                  # Configuration classes
├── run.py                     # Application entry point
├── requirements.txt           # Python dependencies
├── pyproject.toml             # Project metadata
├── .env                       # Environment variables (create manually)
└── README.md
```

## Troubleshooting

### No articles appear

If the page shows "No articles found":

1. Check the server logs for API errors
2. Visit `/debug-newsapi` to see raw API response
3. Verify `NEWSAPI_KEY` in `.env` file
4. Wait for rate limit reset (free tier: 100 requests/day)
5. Check your preferences — a language with no articles or all sources hidden will show empty results

### Missing dependencies

```bash
pip install -r requirements.txt
# or
uv sync
```

## License

MIT
