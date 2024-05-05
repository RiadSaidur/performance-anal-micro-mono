from flask import request
from flask_restful import Resource
import os
import requests

_PERSON_URL = 'http://localhost:8000'

class Person(Resource):
    def post(self):
        if 'file' not in request.files:
            return {"error": "No file part"}, 400
    
        file = request.files['file']

        if file.filename == '':
            return {"error": "No selected file"}, 400
        
        files = {'file': (file.filename, file.read())}
        response = requests.post(_PERSON_URL+'/upload', files=files)

        return response.json(), response.status_code
    