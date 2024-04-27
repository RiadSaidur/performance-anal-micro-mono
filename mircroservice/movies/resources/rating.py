from flask import request
from flask_restful import Resource

from .database import RatingDAO

ratingDao = RatingDAO()

class RateMovie(Resource):
    '''CRUD methods for rating objects in the database'''
    def post(self, movie_id):
        '''Route to add a rating for a movie in the database'''
        data = request.json

        value = data['value']
        user_id = data['user_id']

        if not ratingDao.add_rating(movie_id, user_id, value):
            return {"error": "could not rate movie"}, 400

        return "Success", 200
