from ..db import db
import enum


class ListType(enum.Enum):
    toRead = 'to-read'
    reading = 'reading'
    read = 'read'
    custom = 'custom'


class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    owner_id = db.Column(db.ForeignKey('user.id'), nullable=False)
    list_type = db.Column(db.Enum(ListType), nullable=False)
    books = db.relationship('ListBooks', backref='list')

    def insert(self):
        db.session.add(self)
        db.session.commit()
