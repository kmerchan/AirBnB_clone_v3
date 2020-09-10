#!/usr/bin/python3
"""
user related api endpoints
"""

from api.v1.views import app_views
from flask import abort, request
from flask.json import jsonify
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False)
def get_all_users():
    """
    returns a list of all users
    """
    all_users = storage.all(User)
    res = []
    for user in all_users.values():
        res.append(user.to_dict())
    return jsonify(res)


@app_views.route('/users/<user_id>', strict_slashes=False)
def get_user(user_id=None):
    """
    retrieves user object based on user_id
    """
    user = storage.get(User, user_id)
    if user is not None:
        return jsonify(user.to_dict())

    abort(404)


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['DELETE'])
def del_user(user_id):
    """
    deletes a user object
    """
    user = storage.get(User, user_id)
    if user is not None:
        user.delete()
        storage.save()
        return jsonify({}), 200

    abort(404)


@app_views.route('/users', strict_slashes=False,
                 methods=['POST'])
def make_user():
    """
    creates a user object
    """
    json = request.get_json(silent=True)

    if json is None:
        abort(400, 'Not a JSON')

    if 'email' not in json:
        abort(400, 'Missing email')

    if 'password' not in json:
        abort(400, 'Missing password')

    user = User(**json)
    user.save()

    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['PUT'])
def update_user(user_id):
    """
    updates a user object
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    json = request.get_json(silent=True)

    if json is None:
        abort(400, 'Not a JSON')

    for key, value in json.items():
        if key != 'updated_at' and key != 'created_at' \
           and key != 'id' and key != 'email':
            setattr(user, key, value)

    user.save()

    return jsonify(user.to_dict()), 200
