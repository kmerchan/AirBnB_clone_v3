#!/usr/bin/python3
"""
amenity related api endpoints
"""

from api.v1.views import app_views
from flask import abort, request
from flask.json import jsonify
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False)
@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def get_amenities(amenity_id=None):
    """
    returns a list of all amenities or one amenity
    """
    if amenity_id is None:
        res = []

        for amenity in storage.all(Amenity).values():
            res.append(amenity.to_dict())

        return jsonify(res)

    for amenity in storage.all(Amenity).values():
        if amenity.id == amenity_id:
            return jsonify(amenity.to_dict())

    abort(404)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['DELETE'])
def del_amenity(amenity_id):
    """
    deletes a amenity object
    """
    for amenity in storage.all(Amenity).values():
        if amenity.id == amenity_id:
            amenity.delete()
            storage.save()
            return jsonify({}), 200

    abort(404)


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def make_amenity():
    """
    creates a amenity object
    """
    json = request.get_json(silent=True)

    if json is None:
        abort(400, 'Not a JSON')

    if 'name' not in json:
        abort(400, 'Missing name')

    new = Amenity(**json)
    new.save()

    return jsonify(new.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['PUT'])
def update_amenity(amenity_id):
    """
    updates a amenity object
    """
    for amenity in storage.all(Amenity).values():
        if amenity.id == amenity_id:
            json = request.get_json(silent=True)

            if json is None:
                abort(400, 'Not a JSON')

            for key, value in json.items():
                if key != 'updated_at' and key != 'created_at' and key != 'id':
                    setattr(amenity, key, value)

            amenity.save()

            return jsonify(amenity.to_dict()), 200

    abort(404)
