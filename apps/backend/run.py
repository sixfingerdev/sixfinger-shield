#!/usr/bin/env python3
"""
Run the Flask application
"""
import os
from app.main import create_app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    # Use FLASK_DEBUG environment variable (Flask 2.2+)
    debug = os.environ.get('FLASK_DEBUG', '0') == '1'
    app.run(host='0.0.0.0', port=port, debug=debug)
