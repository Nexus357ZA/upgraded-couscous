from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app


#from app.models import Article
from app.main import bp
from newsapi import NewsApiClient
import os

@bp.route('/', methods=['GET'])
@bp.route('/index', methods=['GET'])
def index():
    newsapi = NewsApiClient(api_key=os.environ.get('NEWSAPI_KEY'))
    top_headlines = newsapi.get_top_headlines(
        category='general',
        language='en',
        country='gb'
    )

    articles = top_headlines['articles']
    page = request.args.get('page', 1, type=int)

    #next_url = url_for('main.index', page=articles.next_num) \
    #    if articles.has_next else None
    #prev_url = url_for('main.index', page=articles.prev_num) \
    #    if articles.has_prev else None

    return render_template('index.html', title='Home',
                           articles=articles)

