#!/usr/bin/env python3
"""
creates route /status for blueprint object app_views
"""

from api.v1.views import app_views
import json

@app_views.route('/status', strict_slashes=False)
def show_status():
    """
    returns JSON: "status": "OK"
    """
    # TO DO:
    # Needs to be JSON string - currently working with just regular string
    # Attempting to use json.dumps to save as JSON, but missing positional arg
    # json.dumps('"status": "OK"')
    return ('"status": "OK"')
