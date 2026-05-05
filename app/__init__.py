from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from config import Config
from flask_sqlalchemy import SQLAlchemy


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db = SQLAlchemy()
    bootstrap = Bootstrap()

    bootstrap.init_app(app)
    db.init_app(app)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app
