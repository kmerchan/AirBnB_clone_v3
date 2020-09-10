#!/usr/bin/python3
"""
city related api endpoints
"""

from api.v1.views import app_views
from flask import abort, request
from flask.json import jsonify
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def get_cities_by_state(state_id=None):
    """
    returns a list of all cities of a state
    """
    all_state = storage.all(State)
    res = []
    if all_state is not {} and state_id is not None:
        for state in all_state.values():
            if state.id == state_id:
                for city in state.cities:
                    res.append(city.to_dict())
                return jsonify(res)

    abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False)
def get_cities(city_id=None):
    """
    retrieves city object based on city_id
    """
    city = storage.get(City, city_id)
    if city is not None:
        return jsonify(city.to_dict())

    abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['DELETE'])
def del_city(city_id):
    """
    deletes a city object
    """
    city = storage.get(City, city_id)
    if city is not None:
        city.delete()
        storage.save()
        return jsonify({}), 200

    abort(404)


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['POST'])
def make_city(state_id=None):
    """
    creates a city object
    """
    json = request.get_json(silent=True)

    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    if json is None:
        abort(400, 'Not a JSON')

    if 'name' not in json:
        abort(400, 'Missing name')

    city = City(**json)
    city.state_id = state_id
    city.save()

    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['PUT'])
def update_city(city_id):
    """
    updates a city object
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    json = request.get_json(silent=True)

    if json is None:
        abort(400, 'Not a JSON')

    for key, value in json.items():
        if key != 'updated_at' and key != 'created_at' \
           and key != 'id' and key != 'state_id':
            setattr(city, key, value)

    city.save()

    return jsonify(city.to_dict()), 200
