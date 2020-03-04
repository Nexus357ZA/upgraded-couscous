from flask import Flask, request, current_app
from flask_bootstrap import Bootstrap
from config import Config
from flask_sqlalchemy import SQLAlchemy
from newsapi import NewsApiClient
import os

bootstrap = Bootstrap()
#db = SQLAlchemy()
newsapi = NewsApiClient(api_key=os.environ.get('NEWSAPI_KEY'))


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    #db.init_app(app)
    bootstrap.init_app(app)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app