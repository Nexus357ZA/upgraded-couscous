from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app

from app.models import Article
from app.main import bp

@bp.route('/', methods=['GET'])
@bp.route('/index', methods=['GET'])
def index():

    articles = Article()
    page = request.args.get('page', 1, type=int)

    next_url = url_for('main.index', page=articles.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.index', page=articles.prev_num) \
        if posts.has_prev else None

    return render_template('index.html', title=_('Home'),
                           articles=articles.items, next_url=next_url,
                           prev_url=prev_url)