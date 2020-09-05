from ..db import db


class ChallengeParticipants(db.Model):
    challenge_id = db.Column(db.ForeignKey('challenge.id'), primary_key=True)
    user_id = db.Column(db.ForeignKey('user.id'), primary_key=True)
    time_joined = db.Column(db.DateTime(), nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()
