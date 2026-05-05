from flask import render_template, request, jsonify, current_app
from app.main import bp


class NewsAPI:
    """Per-request NewsAPI client to avoid singleton issues"""
    def __init__(self, api_key):
        from newsapi import NewsApiClient
        self.client = NewsApiClient(api_key=api_key)

    def get_top_headlines(self, category='general', language='en', country='gb'):
        return self.client.get_top_headlines(category=category, language=language, country=country)


def get_news_client():
    """Get fresh NewsAPI client for current request"""
    import os
    key = os.environ.get('NEWSAPI_KEY')
    if not key:
        raise RuntimeError('NEWSAPI_KEY environment variable is not set')
    # Debug: log that we got a key
    current_app.logger.info(f"NEWSAPI_KEY loaded (length: {len(key)} chars)")
    return NewsAPI(key)


# Debug endpoint to test NewsAPI directly
@bp.route('/debug-newsapi', methods=['GET'])
def debug_newsapi():
    client = get_news_client()
    result = client.get_top_headlines(category='technology', language='en', country='us')
    return jsonify({'status': 'ok', 'data': result})


@bp.route('/', methods=['GET'])
@bp.route('/index', methods=['GET'])
def index():
    client = get_news_client()
    # Try multiple categories - pick first one that returns results
    for category, country in [('technology', 'us'), ('business', 'us'), ('general', 'gb')]:
        resp = client.get_top_headlines(category=category, language='en', country=country)
        if isinstance(resp, dict) and 'articles' in resp:
            articles = resp['articles']
            current_app.logger.info(f"Fetched {len(articles)} articles from {category} ({country})")
            break
        elif isinstance(resp, dict) and 'error' in resp:
            current_app.logger.warning(f"{category}/{country} error: {resp['error']}, trying next...")
    else:
        # All failed - return empty list
        articles = []

    page = request.args.get('page', 1, type=int)
    # Add a test article for debugging when API returns no results
    sample_article = {'title': 'TEST: This is a sample article (API returned empty)', 'content': 'This is sample content to verify templates work.', 'url': 'https://example.com', 'source': {'name': 'Example'}, 'author': 'Test', 'urlToImage': None, 'publishedAt': '2026-05-04T10:00:00Z'}
    test_articles = [sample_article] if not articles else articles
    # Pagination not yet implemented (remove once models.py is wired up)
    return render_template('index.html', title='Home', articles=test_articles)

