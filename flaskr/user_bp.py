from flask import Blueprint, jsonify, abort
from .auth.auth import requires_auth
from .models.list import List
from .models.challenge import Challenge

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/<int:user_id>/lists')
@requires_auth()
def get_user_lists(payload, user_id):
    if payload['id'] != user_id:
        return abort(403)

    lists = [li.to_dict() for li in List.query.filter_by(owner_id=user_id)]

    return jsonify({'lists': lists})


@bp.route('/<int:user_id>/challenges')
@requires_auth()
def get_user_challenges(payload, user_id):
    if payload['id'] != user_id:
        return abort(403)

    challenges = [c.to_dict()
                  for c in Challenge.query.filter_by(creator_id=user_id)]
    return jsonify({'challenges': challenges})
