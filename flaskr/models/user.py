from ..db import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    reviews = db.relationship('Review', backref='user')
    progress = db.relationship('ReadingProgress', backref='user')
    challenges = db.relationship('ChallengeParticipants', backref='user')

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }
