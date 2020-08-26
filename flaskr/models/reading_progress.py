from ..db import db


class ReadingProgress(db.Model):
    uid = db.Column(db.ForeignKey('user.uid'), primary_key=True)
    book_id = db.Column(db.ForeignKey('book.id'), primary_key=True)
    progress = db.Column(db.Integer, nullable=True, default=0)

    def insert(self):
        db.session.add(self)
        db.session.commit()
