# Upgraded Couscous

A Flask-based news aggregator that fetches top headlines from [NewsAPI](https://newsapi.org/) and displays them in a clean, responsive web interface.

## Features

- Fetches real-time news headlines from multiple categories (Technology, Business, General)
- Multiple fallback sources for reliability
- Responsive design with Bootstrap 3 styling
- Debug mode with embedded test articles when API returns empty results
- Health check endpoint (`/debug-newsapi`) to verify API connectivity

## Prerequisites

- Python 3.8+
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

- **Main page**: `http://localhost:8080/` - Displays news headlines
- **Debug endpoint**: `http://localhost:8080/debug-newsapi` - Returns raw API response for troubleshooting

## Project Structure

```
upgraded-couscous/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── errors/               # Error handlers
│   ├── main/                 # Main routes and NewsAPI client
│   │   ├── __init__.py
│   │   └── routes.py         # Route definitions
│   └── models.py             # Database models (optional)
├── app/templates/            # Jinja2 templates
│   ├── base.html            # Base template with navbar
│   ├── index.html           # Home page layout
│   └── _article.html        # Article card component
├── config.py                 # Configuration classes
├── run.py                    # Application entry point
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (create manually)
└── README.md
```

## Troubleshooting

### No articles appear

If you see the sample test article ("TEST: This is a sample article"), your NewsAPI key may be invalid or rate-limited.

1. Check the server logs for API errors
2. Visit `/debug-newsapi` to see raw API response
3. Verify `NEWSAPI_KEY` in `.env` file
4. Wait for rate limit reset (free tier: 100 requests/day)

### Missing dependencies

```bash
pip install -r requirements.txt
# or
uv sync
```

## License

MIT
