#!/usr/bin/env python3
"""
creates route /status for blueprint object app_views
"""

from flask.json import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', strict_slashes=False)
def show_status():
    """
    returns JSON: "status": "OK"
    """
    return jsonify(status='OK')


@app_views.route('/stats', strict_slashes=False)
def show_stats():
    """
    Retrieves number of objects by type
    """
    stats = {'amenities': storage.count(Amenity),
             'cities': storage.count(City),
             'places': storage.count(Place),
             'reviews': storage.count(Review),
             'states': storage.count(State),
             'users': storage.count(User)}

    return jsonify(stats)
