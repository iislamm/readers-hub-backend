from flask import Blueprint, request, jsonify, abort
from .models.book import Book
from .models.reading_progress import ReadingProgress
from .models.review import Review
from .auth.auth import requires_auth
from .db import db

bp = Blueprint('books', __name__, url_prefix='/books')


@bp.route('/search')
def search_books():
    query = request.args['q']
    result = Book.query.filter(Book.title.ilike('%{}%'.format(query))).all()
    books = [b.to_dict() for b in result]
    return jsonify({'books': books})


@bp.route('/<int:book_id>')
def get_book(book_id):
    book = Book.query.get(book_id)
    if book is None:
        return abort(404)

    return jsonify({'book': book.to_dict()})


@bp.route('/<int:book_id>/progress', methods=['PUT'])
@requires_auth()
def update_book_progress(payload, book_id):
    request_data = request.get_json()

    if request_data['progress'] > 100 or request_data['progress'] < 0:
        return abort(400)

    book = Book.query.get(book_id)
    if book is None:
        return abort(404)

    new_progress = ReadingProgress(
        user_id=payload['id'], book_id=book_id, progress=request_data['progress'])
    db.session.add(new_progress)
    db.session.commit()

    return jsonify({
        'book_id': book_id,
        'uid': payload['id'],
        'progress': new_progress.progress
    })


@bp.route('/<int:book_id>/reviews', methods=['POST'])
@requires_auth()
def add_book_review(payload, book_id):
    book = Book.query.get(book_id)
    if book is None:
        return abort(404)

    request_data = request.get_json()
    if request_data['rating'] is None:
        return abort(400)

    new_review = Review(user_id=payload.id, book_id=book_id,
                        rate=request_data['rating'])

    if request_data['comment'] is not None:
        new_review.comment = request_data['comment']

    db.session.add(new_review)
    db.session.commit()

    response_body = {
        "book_id": book_id,
        "uid": payload.id,
        "review": {
            "rating": new_review.rate,
            "comment": new_review.comment
        }
    }

    return jsonify(response_body)
