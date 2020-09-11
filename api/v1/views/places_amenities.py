#!/usr/bin/python3
"""
amenities by place related api endpoints
"""

from api.v1.views import app_views
from flask import abort, request
from flask.json import jsonify
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities', strict_slashes=False)
def get_amenities_by_place(place_id=None):
    """
    returns a list of all amenities for a Place
    """
    place = storage.get(Place, place_id)
    res = []
    if place is not None:
        for amenity in place.amenities:
            res.append(amenity.to_dict())
        return jsonify(res)

    abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE'])
def del_place_amentities(place_id=None, amenity_id=None):
    """
    deletes an amentity from place based on ids
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)

    for place_amenity in place.amenities:
        if place_amenity.id == amenity.id:
            place.amenities.remove(amenity)
            storage.save()
            return jsonify({}), 200

    abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['POST'])
def link_amenity_to_place(place_id=None, amenity_id=None):
    """
    links an amenity object for place
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)

    for place_amenity in place.amenities:
        if place_amenity.id == amenity.id:
            return jsonify(amenity.to_dict()), 200

    place.amenities.append(amenity)
    place.save()

    return jsonify(amenity.to_dict()), 201
