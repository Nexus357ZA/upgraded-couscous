import os
from app import create_app


def main():
    """Run the Flask development server."""
    app = create_app()
    port = int(os.environ.get('PORT', 8080))
    debug = os.environ.get('FLASK_ENV', 'production') == 'development' or \
            os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)


if __name__ == '__main__':
    main()
