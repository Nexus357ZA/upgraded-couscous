from flask import current_app, url_for
import json
from app import db


class Article(db.Model):
    #TODO - This is just a skeleton
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(160))
    author = db.Column(db.String(160))
    title = db.Column(db.String(160))
    description = db.Column(db.String(160))
    url = db.Column(db.String())
    urlToImage = db.Column(db.String())
    publishedAt = db.Column(db.String(160))
    content = db.Column(db.String())

    def __repr__(self):
        return '<Article {}>'.format(self.title)