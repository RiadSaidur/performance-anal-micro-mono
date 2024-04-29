from flask import request
from flask_restful import Resource
import requests
import logging

# person_endpoint = 'http://172.19.0.2:9000'
faceRecogniton_endpoint = 'http://localhost/find'

person_endpoint = 'http://192.168.0.114:9000'
# faceRecogniton_endpoint = 'http://0.0.0.0:8000/find'

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class Person(Resource):
    def post(self):
        if 'file' not in request.files:
            print(request.files)
            return {'error': 'No file part'}, 400

        file = request.files['file']

        try:
            response = requests.post(person_endpoint+'/upload', files={'file': (file.filename, file.read())})
            
            if response.status_code != 200:
                return response.json(), response.status_code
        
            response_data = response.json()

            missingPersonData = {
                'url': response_data['url'],
                'face': response_data['face']
            }

            print(missingPersonData)

            response = requests.post(faceRecogniton_endpoint, json=missingPersonData)

            # delete image from person server
            delete_response = requests.delete(person_endpoint+'/delete/'+str(response_data['face']))

            return response.json(), response.status_code
        except Exception as e:
            logging.info(e)
            return {'error': str(e)}, 500