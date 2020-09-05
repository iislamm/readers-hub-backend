from flask import Blueprint, request, abort, escape, jsonify
from .auth.auth import requires_auth
from .models.list import List, ListType
from .models.book import Book
from .models.list_books import ListBooks
from .db import db
from datetime import datetime

bp = Blueprint('lists', __name__, url_prefix='/lists')


@bp.route('/', methods=['POST'])
@requires_auth()
def add_list(payload):
    request_data = request.get_json()
    list_name = escape(request_data['name'])
    if list_name is None or len(list_name) < 1:
        return abort(400)

    new_list = List(name=list_name, owner_id=payload['id'],
                    list_type=ListType.custom)
    new_list.insert()

    return jsonify({'list': new_list.to_dict()})


@bp.route('/<int:list_id>', methods=['PATCH'])
@requires_auth()
def update_list(payload, list_id):
    request_data = request.get_json()
    name = escape(request_data['list']['name'])

    current_list = List.query.get(list_id)
    if current_list.owner_id != payload['id']:
        return abort(403)

    current_list.name = name
    db.session.commit()

    return jsonify({'list': current_list.to_dict()})


@bp.route('/<int:list_id>', methods=['DELETE'])
@requires_auth()
def delete_list(payload, list_id):
    current_list = List.query.get(list_id)
    if current_list.owner_id != payload['id']:
        return abort(403)

    db.session.delete(current_list)
    db.session.commit()

    return jsonify({'list_id': list_id})


@bp.route('/<int:list_id>/books')
@requires_auth()
def get_list_books(payload, list_id):
    current_list = List.query.get(list_id)
    if current_list.owner_id != payload['id']:
        return abort(403)

    books = [Book.query.get(b.book_id).to_dict() for b in current_list.books]
    return jsonify({'list_id': list_id, 'books': books})


@bp.route('/<int:list_id>/books', methods=['POST'])
@requires_auth()
def add_list_book(payload, list_id):
    request_data = request.get_json()
    book_id = request_data['book_id']
    if type(book_id) is not int:
        return abort(400)

    current_list = List.query.get(list_id)
    if current_list is None:
        return abort(404)

    if current_list.owner_id != payload['id']:
        return abort(403)

    book = Book.query.get(book_id)
    if book is None:
        return abort(403)

    list_book = ListBooks(list_id=list_id, book_id=book_id,
                          time_added=datetime.now())
    list_book.insert()

    return jsonify({
        'list_id': list_id,
        'book_id': book_id
    })
