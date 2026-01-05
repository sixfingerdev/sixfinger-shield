#!/usr/bin/env python3
"""
Run the Flask application
"""
import os
from app.main import create_app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
