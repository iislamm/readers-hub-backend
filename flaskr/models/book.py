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

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'authors': self.authors,
            'goodreads_average_rating': self.goodreads_average_rating,
            'average_rating': self.average_rating,
            'isbn': self.isbn,
            'isbn13': self.isbn13,
            'language_code': self.language_code,
            'num_pages': self.num_pages,
            'ratings_count': self.ratings_count,
            'goodreads_ratings_count': self.goodreads_ratings_count,
            'goodreads_text_reviews_count': self.goodreads_text_reviews_count,
            'reviews': self.reviews
        }
