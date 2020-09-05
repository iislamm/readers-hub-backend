from ..db import db
import enum


class ChallengeType(enum.Enum):
    public = 'public'
    private = 'private'


class Challenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    creator_id = db.Column(db.ForeignKey('user.id'), nullable=False)
    start_time = db.Column(db.DateTime(), nullable=False)
    end_time = db.Column(db.DateTime(), nullable=False)
    target_books_count = db.Column(db.Integer, nullable=False)
    challenge_type = db.Column(db.Enum(ChallengeType), nullable=False)
    participants = db.relationship('ChallengeParticipants', backref='challenge')

    def insert(self):
        db.session.add(self)
        db.session.commit()
