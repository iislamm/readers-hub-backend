from ..db import db


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    authors = db.Column(db.String(), nullable=False)
    goodreads_average_rating = db.Column(db.Float)
    average_rating = db.Column(db.Float)
    isbn = db.Column(db.String(), unique=True, nullable=False)
    isbn13 = db.Column(db.String(), unique=True, nullable=False)
    language_code = db.Column(db.String())
    num_pages = db.Column(db.Integer, nullable=False)
    ratings_count = db.Column(db.Integer, nullable=False, default=0)
    goodreads_ratings_count = db.Column(db.Integer)
    goodreads_text_reviews_count = db.Column(db.Integer)
    reviews = db.relationship('Review', backref='book')
    progress = db.relationship('ReadingProgress', backref='book')

    def insert(self):
        db.session.add(self)
        db.session.commit()
