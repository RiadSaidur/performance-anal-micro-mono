from datetime import datetime
from flask import request, jsonify
from flask_restful import Resource

from .database import MovieDAO
from .database import RatingDAO

# initialize the Movie database access object
movieDao = MovieDAO()

class Movies(Resource):
    '''Application resource to handle retrieving movie operations'''
    def get(self):
        '''Request method for retreiving movie object from the database.'''
        movies = movieDao.get_movies()
        rating_dao = RatingDAO()

        for movie in movies:
            movie.rating = rating_dao.get_rating(movie.id)

        return jsonify({
            'movies': [result.serialized for result in movies]
        })


class AddMovie(Resource):
    '''Application resource to handle add movie operations'''
    def post(self):
        '''Request method for adding a movie object to the database'''
        data = request.json
        title = data['title']
        released = datetime.strptime(data['released'], "%m-%d-%Y")
        movie = {"title": title, "released": released}

        if not movieDao.add_movie(title, released):
            return jsonify({"error": "could not add movie"})

        return jsonify(movie)


class EditMovie(Resource):
    '''Application Resource to handle update movie operations'''
    def put(self, pk):
        '''Request method for updating a database movie object'''
        data = request.json

        title = data['title']
        released = datetime.strptime(data['released'], "%m-%d-%Y")

        if not movieDao.update_movie(pk, title, released):
            return jsonify({"error": "could not update movie"})

        return jsonify(data)


class RemoveMovie(Resource):
    '''Application Resource to handle delete movie operations'''
    def delete(self, pk):
        '''Request method for deleting a movie object from the database'''
        if not movieDao.delete_movie(pk):
            return jsonify({"error": "could not delete movie"})

        return "Deleted", 200
