"""
Author: Tony Lee
Description: Class for users of the API, includes admins, registered users, or [guests,]
"""

from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import create_access_token

from .database import UserDAO

userDao = UserDAO()

class Users(Resource):
    '''CRUD methods for user objects in the database'''
    def post(self):
        '''Method route for adding a user to the database for the API'''
        data = request.json
        username = data['username']
        password = data['password']

        if username is None or password is None:
            return "Missing Arguments", 400 # missing arguments
        if userDao.get_user(username) is not None:
            return "User already exists", 400 # existing user

        if not userDao.add_user(username, password):
            return jsonify({"error": "could not add user"})

        return "success", 200
class SignUp(Resource):
    '''CRUD methods for user objects in the database'''
    def post(self):
        '''Method route for adding a user to the database for the API'''
        data = request.json
        username = data['username']
        password = data['password']


        if username is None or password is None:
            return {"error": "Missing Arguments"}, 400
        if userDao.get_user(username) is not None:
            return {"error": "User already exists"}, 400

        user = userDao.add_user(username, password)

        if not user:
            return {"error": "could not add user"}

        token = create_access_token({ 'user_id': user.id })

        return ({"token": token}), 200
    
class SignIn(Resource):
    '''CRUD methods for user objects in the database'''
    def post(self):
        '''Method route for adding a user to the database for the API'''
        data = request.json
        username = data['username']
        password = data['password']

        if username is None or password is None:
            return {"error": "Missing Arguments"}, 400

        user = userDao.get_user(username)
        
        if not user:
            return {"error": "could not find user"}, 404
        
        if not user.verify_password(password):
            return {"error": "invalid username or password"}, 401
        
        token = create_access_token({ 'user_id': user.id })

        return ({"token": token}), 200