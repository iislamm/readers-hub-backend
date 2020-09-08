from flask import Blueprint, request, jsonify, escape, abort
from .auth.auth import requires_auth
from .models.challenge import Challenge, ChallengeType
from .models.challenge_participants import ChallengeParticipants
from datetime import datetime

bp = Blueprint('challenges', __name__, url_prefix='/challenges')


@bp.route('/', methods=['POST'])
@requires_auth()
def add_challenge(payload):
    request_data = request.get_json()
    challenge_name = escape(request_data['name'])
    new_challenge = Challenge(name=challenge_name, creator_id=payload['id'], start_time=request_data['start_time'],
                              end_time=request_data['end_time'], target_books_count=request_data['target_books'],
                              challenge_type=ChallengeType(request_data['challenge_type']).name)
    new_challenge.insert()

    return jsonify({'challenge': new_challenge.to_dict()})


@bp.route('/<int:challenge_id>/join', methods=['POST'])
@requires_auth()
def join_challenge(payload, challenge_id):
    challenge = Challenge.query.get(challenge_id)
    if challenge is None:
        return abort(404)

    if challenge.challenge_type != ChallengeType.public:
        return abort(403)

    challenge_participant = ChallengeParticipants.query.filter_by(
        user_id=payload['id'], challenge_id=challenge_id)

    if challenge_participant:
        return abort(403)

    new_challenge_participant = ChallengeParticipants(
        challenge_id=challenge_id, user_id=payload['id'], time_joined=datetime.now())
    new_challenge_participant.insert()

    return jsonify({
        'uid': new_challenge_participant.user_id,
        'challenge_id': new_challenge_participant.challenge_id
    })


@bp.route('/<int:challenge_id>')
@requires_auth()
def get_challenge(payload, challenge_id):
    challenge = Challenge.query.get(challenge_id)
    if challenge is None:
        return abort(404)

    challenge_dict = challenge.to_dict()

    if payload['id'] not in challenge_dict['participants'] and challenge_dict['creator_id'] != payload['id']:
        return abort(403)

    return jsonify({'challenge': challenge.to_dict()})
