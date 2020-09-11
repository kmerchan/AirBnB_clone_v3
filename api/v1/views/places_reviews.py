#!/usr/bin/python3
"""
reviews related api endpoints
"""

from api.v1.views import app_views
from flask import abort, request
from flask.json import jsonify
from models import storage
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def get_reviews_by_place(place_id=None):
    """
    returns a list of all reviews for a Place
    """
    place = storage.get(Place, place_id)
    res = []
    if place is not None:
        for review in place.reviews:
            res.append(review.to_dict())
        return jsonify(res)

    abort(404)


@app_views.route('/reviews/<review_id>', strict_slashes=False)
def get_review(review_id=None):
    """
    retrieves one review by review_id
    """
    review = storage.get(Review, review_id)
    if review is not None:
        return jsonify(review.to_dict())

    abort(404)


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['DELETE'])
def del_review(review_id=None):
    """
    deletes a review object
    """
    review = storage.get(Review, review_id)
    if review is not None:
        review.delete()
        storage.save()
        return jsonify({}), 200

    abort(404)


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['POST'])
def make_review(place_id=None):
    """
    creates a review object
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    json = request.get_json(silent=True)

    if json is None:
        abort(400, 'Not a JSON')

    if 'user_id' not in json:
        abort(400, 'Missing used_id')

    user = storage.get(User, json.get('user_id'))
    if user is None:
        abort(404)

    if 'text' not in json:
        abort(400, 'Missing text')

    review = Review(**json)
    review.place_id = place_id
    review.save()

    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['PUT'])
def update_review(review_id):
    """
    updates a review object
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    json = request.get_json(silent=True)

    if json is None:
        abort(400, 'Not a JSON')

    for key, value in json.items():
        if key != 'updated_at' and key != 'created_at' and key != 'id' \
           and key != 'user_id' and key != 'place_id':
            setattr(review, key, value)

    review.save()

    return jsonify(review.to_dict()), 200
