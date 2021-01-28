"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

import flask
from flask import Flask, request, jsonify
import sqlite3
app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app


@app.route('/')
def home():
    """Renders a home page."""
    return '''<h1>Test API mini dataguru</h1>
   <p> prototype API for manupulating data using flask and sqlite.</p>'''




if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
