from flask import request
from flask_restful import Resource
import requests
import logging

person_endpoint = 'http://172.19.0.2:9000/upload'
faceRecogniton_endpoint = 'http://172.19.0.3:8000/find'

# person_endpoint = 'http://0.0.0.0:5000/upload'
# faceRecogniton_endpoint = 'http://0.0.0.0:8000/find'

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class Person(Resource):
    def post(self):
        if 'file' not in request.files:
            return {'error': 'No file part'}, 400

        file = request.files['file']

        try:
            response = requests.post(person_endpoint, files={'file': (file.filename, file.read())})
            
            if response.status_code != 200:
                return response.json(), response.status_code
        except Exception as e:
            logging.info(e)
            return {'error': str(e)}, 500
        
        response_data = response.json()

        missingPersonData = {
            'url': response_data['url'],
            'face': response_data['face']
        }

        response = requests.post(faceRecogniton_endpoint, json=missingPersonData)

        return response.json(), response.status_code