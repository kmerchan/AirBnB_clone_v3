#!/usr/bin/python3
"""
creates instance of Flask and registers blueprint to instance
"""

from flask import Flask
from flask_cors import CORS
from flask.json import jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, origins="0.0.0.0")
host_var = getenv('HBNB_API_HOST')
port_var = getenv('HBNB_API_PORT')


@app.teardown_appcontext
def teardown(self):
    """
    closes current session through storage.close()
    """
    storage.close()


@app.errorhandler(404)
def not_found(e):
    """
    returns json formatted error
    """
    return jsonify(error='Not found'), 404

if __name__ == "__main__":
    app.run(host=host_var, port=port_var, threaded=True)
