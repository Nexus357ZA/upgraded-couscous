from flask import render_template, request, jsonify, current_app
from app.main import bp


class NewsAPI:
    """Per-request NewsAPI client to avoid singleton issues"""
    def __init__(self, api_key):
        from newsapi import NewsApiClient
        self.client = NewsApiClient(api_key=api_key)

    def get_top_headlines(self, category='general', language='en', country='gb'):
        """Fetch top headlines from NewsAPI with fallbacks."""
        return self.client.get_top_headlines(category=category, language=language, country=country)


def get_news_client():
    """Get fresh NewsAPI client for current request"""
    import os
    key = os.environ.get('NEWSAPI_KEY')
    if not key:
        raise RuntimeError('NEWSAPI_KEY environment variable is not set')
    return NewsAPI(key)


# Debug endpoint to test NewsAPI directly
@bp.route('/debug-newsapi', methods=['GET'])
def debug_newsapi():
    """Returns raw NewsAPI response for troubleshooting."""
    client = get_news_client()
    result = client.get_top_headlines(category='technology', language='en', country='us')
    if isinstance(result, dict) and 'error' in result:
        return jsonify({'error': result['error']}), 400
    return jsonify({'status': 'ok', 'data': result})


@bp.route('/', methods=['GET'])
@bp.route('/index', methods=['GET'])
def index():
    """Display news headlines grid."""
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
        # All failed - return empty list (test article shows UI works)
        articles = []

    # Pre-process article content on Python side to avoid Jinja2 filter chain issues with .strip()
    clean_articles = []
    for art in articles:
        raw = art.get('content') or art.get('description', '')
        if raw:
            raw_str = str(raw).replace('\n', ' ').replace('\r', '').strip()[:300]
            if len(str(raw)) > 300:
                raw_str += '...'
            # Add clean_content key for template to use
            art['clean_content'] = raw_str
    return render_template('index.html', title='Home', articles=clean_articles)

