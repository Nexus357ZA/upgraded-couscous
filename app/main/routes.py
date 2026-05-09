import time
import json
from flask import render_template, request, jsonify, current_app
from app.main import bp
from config import Config


PER_PAGE = 9
CACHE_TTL = 300

CATEGORIES = ['latest', 'technology', 'business', 'general', 'health', 'science', 'entertainment', 'sports']
COUNTRY = 'us'

LANGUAGES = [
    {'code': 'en', 'label': 'English'},
    {'code': 'de', 'label': 'German'},
    {'code': 'es', 'label': 'Spanish'},
    {'code': 'fr', 'label': 'French'},
    {'code': 'it', 'label': 'Italian'},
    {'code': 'nl', 'label': 'Dutch'},
    {'code': 'pt', 'label': 'Portuguese'},
    {'code': 'ru', 'label': 'Russian'},
    {'code': 'zh', 'label': 'Chinese'},
]

DEFAULT_PREFERENCES = {
    'language': 'en',
    'excluded_sources': [],
}


_articles_cache = {}


class NewsAPI:
    def __init__(self, api_key):
        from newsapi import NewsApiClient
        self.client = NewsApiClient(api_key=api_key)

    def get_top_headlines(self, category='general', language='en', country='gb'):
        return self.client.get_top_headlines(category=category, language=language, country=country)

    def get_everything(self, language='en', sort_by='publishedAt', page_size=100):
        return self.client.get_everything(q='news', language=language, sort_by=sort_by, page_size=page_size)


def get_news_client():
    key = Config.NEWSAPI_KEY
    if not key:
        raise RuntimeError('NEWSAPI_KEY is not set. Please set it in project root .env')
    return NewsAPI(key)


def read_preferences(request):
    raw = request.cookies.get('preferences')
    if raw:
        try:
            prefs = json.loads(raw)
            return {**DEFAULT_PREFERENCES, **prefs}
        except (json.JSONDecodeError, TypeError):
            pass
    return dict(DEFAULT_PREFERENCES)


def process_articles(articles):
    for art in articles:
        raw = art.get('content') or art.get('description', '')
        if raw:
            raw_str = str(raw).replace('\n', ' ').replace('\r', '').strip()[:300]
            if len(str(raw)) > 300:
                raw_str += '...'
            art['clean_content'] = raw_str
    return articles


def gather_sources(articles):
    seen = set()
    sources = []
    for art in articles:
        src = art.get('source') or {}
        name = src.get('name') or 'Unknown'
        sid = src.get('id') or name
        if sid not in seen:
            seen.add(sid)
            sources.append({'id': sid, 'name': name})
    return sorted(sources, key=lambda s: s['name'].lower())


def fetch_articles(category='latest', language='en'):
    global _articles_cache
    cache_key = (category, language)
    now = time.time()
    cached = _articles_cache.get(cache_key)
    if cached and now - cached['time'] < CACHE_TTL:
        return cached['articles']

    client = get_news_client()
    if category == 'latest':
        resp = client.get_everything(language=language)
    else:
        resp = client.get_top_headlines(category=category, language=language, country=COUNTRY)
    if isinstance(resp, dict) and 'articles' in resp:
        articles = resp['articles']
        current_app.logger.info(f"Fetched {len(articles)} articles from {category} ({language})")
    elif isinstance(resp, dict) and 'error' in resp:
        current_app.logger.warning(f"{category} error: {resp['error']}")
        articles = []
    else:
        articles = []

    _articles_cache[cache_key] = {'articles': articles, 'time': now}
    return articles


@bp.route('/debug-newsapi', methods=['GET'])
def debug_newsapi():
    client = get_news_client()
    result = client.get_top_headlines(category='technology', language='en', country='us')
    if isinstance(result, dict) and 'error' in result:
        return jsonify({'error': result['error']}), 400
    return jsonify({'status': 'ok', 'data': result})


@bp.route('/api/preferences', methods=['POST'])
def save_preferences():
    data = request.get_json(silent=True) or {}
    prefs = {**DEFAULT_PREFERENCES}
    if data.get('language') in {l['code'] for l in LANGUAGES}:
        prefs['language'] = data['language']
    excluded = data.get('excluded_sources', [])
    if isinstance(excluded, list):
        prefs['excluded_sources'] = excluded
    resp = jsonify({'status': 'ok', 'preferences': prefs})
    resp.set_cookie('preferences', json.dumps(prefs), max_age=31536000, path='/')
    return resp


@bp.route('/api/articles', methods=['GET'])
def api_articles():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', PER_PAGE, type=int)
    category = request.args.get('category', 'latest')
    if category not in CATEGORIES:
        category = 'latest'
    prefs = read_preferences(request)
    articles = fetch_articles(category, prefs['language'])
    excluded = set(prefs.get('excluded_sources', []))
    if excluded:
        articles = [a for a in articles if not (a.get('source') or {}).get('id') in excluded and
                    not (a.get('source') or {}).get('name') in excluded]
    process_articles(articles)
    total = len(articles)
    start = (page - 1) * per_page
    end = start + per_page
    batch = articles[start:end]
    return jsonify({
        'articles': batch,
        'page': page,
        'per_page': per_page,
        'total': total,
        'has_more': end < total,
    })


@bp.route('/', methods=['GET'])
@bp.route('/index', methods=['GET'])
def index():
    category = request.args.get('category', 'latest')
    if category not in CATEGORIES:
        category = 'latest'
    prefs = read_preferences(request)
    articles = fetch_articles(category, prefs['language'])
    excluded = set(prefs.get('excluded_sources', []))
    if excluded:
        articles = [a for a in articles if not (a.get('source') or {}).get('id') in excluded and
                    not (a.get('source') or {}).get('name') in excluded]
    process_articles(articles)
    sources = gather_sources(articles)
    initial = articles[:PER_PAGE]
    return render_template('index.html', title='Home', articles=initial, total=len(articles),
                           categories=CATEGORIES, current_category=category,
                           languages=LANGUAGES, preferences=prefs, sources=sources)

