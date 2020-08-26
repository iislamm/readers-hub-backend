from ..db import db


class Review(db.Model):
    uid = db.Column(db.ForeignKey('user.uid'), primary_key=True)
    book_id = db.Column(db.ForeignKey('book.id'), primary_key=True)
    rate = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String())

    def insert(self):
        db.session.add(self)
        db.session.commit()
