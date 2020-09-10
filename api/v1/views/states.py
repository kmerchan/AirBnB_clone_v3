#!/usr/bin/python3
"""
state related api endpoints
"""

from api.v1.views import app_views
from flask import abort, request
from flask.json import jsonify
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False)
@app_views.route('/states/<state_id>', strict_slashes=False)
def get_states(state_id=None):
    """
    returns a list of all states or one state
    """
    if state_id is None:
        res = []

        for state in storage.all(State).values():
            res.append(state.to_dict())

        return jsonify(res)

    for state in storage.all(State).values():
        if state.id == state_id:
            return jsonify(state.to_dict())

    abort(404)


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['DELETE'])
def del_state(state_id):
    """
    deletes a state object
    """
    for state in storage.all(State).values():
        if state.id == state_id:
            state.delete()
            storage.save()
            return jsonify({}), 200

    abort(404)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def make_state():
    """
    creates a state object
    """
    json = request.get_json(silent=True)

    if json is None:
        abort(400, 'Not a JSON')

    if 'name' not in json:
        abort(400, 'Missing name')

    new = State(**json)
    new.save()

    return jsonify(new.to_dict()), 201


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def update_state(state_id):
    """
    updates a state object
    """
    for state in storage.all(State).values():
        if state.id == state_id:
            json = request.get_json(silent=True)

            if json is None:
                abort(400, 'Not a JSON')

            for key, value in json.items():
                if key != 'updated_at' and key != 'created_at' and key != 'id':
                    setattr(state, key, value)

            state.save()

            return jsonify(state.to_dict()), 200

    abort(404)
