from flask import current_app, url_for
import json


class Article():
    """News article model for storing news (SQLAlchemy wired up in create_app())"""
    def __init__(self, source='', author=None, title='', description=None,
                 url='', urlToImage=None, publishedAt=None, content=None):
        self.source = source
        self.author = author
        self.title = title
        self.description = description
        self.url = url
        self.urlToImage = urlToImage
        self.publishedAt = publishedAt
        self.content = content

    def __repr__(self):
        return f'<Article {self.title}>'