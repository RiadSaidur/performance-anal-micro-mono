from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

db = SQLAlchemy()

class Movie(db.Model):
    '''
    Table movie, for the movie records stored in the database.
    '''
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True, nullable=False)
    released = db.Column(db.Date, nullable=False)
    rating = None

    def __repr__(self):
        return str(self.id) + self.title + self.released

    def __str__(self):
        return f"Movie [{self.id}, {self.title}, {self.released}]"

    @property
    def serialized(self):
        '''Allow for serialization of SQLAlchemy database object'''
        return {
            'id': self.id,
            'title': self.title,
            'Release Year': datetime.strftime(self.released, "%B %d, %Y"),
            'Rating': self.rating
        }

class Rating(db.Model):
    '''
    Table to store rating scores a particular user gives to a
    particular movie.
    '''
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, ForeignKey("movie.id"))
    user_id = db.Column(db.Integer, default=1)
    value = db.Column(db.Integer, nullable=False)
