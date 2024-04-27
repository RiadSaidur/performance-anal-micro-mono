from datetime import datetime
import os
import sqlalchemy

from models import db
from models import Movie, Rating

class MovieDAO:
    '''
    CRUD methods for movie objects in the database
    '''
    def add_movie(self, title, released):
        '''Add new movie to the database'''
        movie = Movie(title=title, released=released)

        try:
            db.session.add(movie)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
            return False

        return True

    def get_movies(self, movie_id=None):
        '''Read movies from the database based on certain filters'''
        result = None
        try:
            if movie_id is not None:
                result = db.session.query(Movie).get(id)
            elif movie_id is None:
                result = db.session.query(Movie).all()
        except Exception as e:
            print(e)

        return result

    def update_movie(self, movie_id, title, released):
        '''Update a movie record in the database'''
        try:
            movie = db.session.query(Movie).filter(Movie.id == movie_id)
            if movie.first() is not None:
                movie.update({
                    Movie.title: title,
                    Movie.released: released
                })
                db.session.commit()
            else:
                return False
        except AttributeError:
            db.session.rollback()
            return False

        return True

    def delete_movie(self, movie_id):
        '''Remove a movie from the database'''
        try:
            db.session.query(Movie).filter(Movie.id == movie_id).delete()
            db.session.commit()
        except AttributeError:
            db.session.rollback()
            return False

        return True


class RatingDAO:
    '''CRUD methods for rating objects in the database'''
    def add_rating(self, movie_id, user_id, value):
        '''Add new rating to the database'''
        rating = Rating(movie_id=movie_id, user_id=user_id, value=value)

        try:
            db.session.add(rating)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
            return False

        return True

    def get_rating(self, movie_id):
        '''Get the rating score of a particular movie'''
        avg_rating = 0
        scores = None
        try:
            scores = db.session.query(Rating).filter_by(movie_id=movie_id).all()
        except Exception as e:
            print(str(e))

        scores_sum = 0
        for score in scores:
            scores_sum += score.value
        try:
            avg_rating = scores_sum / len(scores)
        except ZeroDivisionError:
            avg_rating = 0

        return avg_rating


class DbSetup():
    '''
    Initialize and set up the database, by creating tables as necessary
    and inserting dummy records as a starting point.
    '''
    movies = [
        {"title": "Avengers: Endgame",
        "released": datetime.strptime("04-22-2019", "%m-%d-%Y")},
        {"title": "Captain America: Civil War",
        "released": datetime.strptime("04-16-2016", "%m-%d-%Y")}
    ]
    ratings = [
        {"movie_id": 1, "username": "john", "value": 5},
        {"movie_id": 1, "username": "jane", "value": 4},
        {"movie_id": 1, "username": "admin", "value": 3},
        {"movie_id": 2, "username": "john", "value": 5},
        {"movie_id": 2, "username": "jane", "value": 4},
        {"movie_id": 2, "username": "admin", "value": 4}
    ]
    
    def __init__(self):
        '''constructor will create all tables for the database.'''
        if not os.path.exists("../database.db"):
            db.create_all()
            self.prepopulate()

    def prepopulate(self):
        '''Add records to the database after intial creation of tables.'''

        # insert into movie
        movie_dao = MovieDAO()
        for movie in self.movies:
            movie_dao.add_movie(movie['title'], movie['released'])

        # insert into rating
        rating_dao = RatingDAO()
        for rating in self.ratings:
            rating_dao.add_rating(rating['movie_id'], rating['username'], rating['value'])
