import os
from flask import request
from flask_restful import Resource
import requests
from werkzeug.utils import secure_filename

faceRecogniton_endpoint = 'http://172.19.0.3:8000/find'
# faceRecogniton_endpoint = 'http://0.0.0.0:8000/find'

class FaceRecognition(Resource):
    _UPLOAD_FOLDER = 'uploads'
    _ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

    def post(self):
        if 'file' not in request.files:
            return {'error': 'No file part'}, 400

        file = request.files['file']
        if file.filename == '':
            return {'error': 'No selected file'}, 400
        if file and self.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(self._UPLOAD_FOLDER, filename)
            file.save(file_path)

            public_url = f'{request.scheme}://{request.host}/temporary/{filename}'

            # Perform face recognition using the saved image
            response = requests.get(f'{faceRecogniton_endpoint}?url={public_url}')

            # Delete the temporarily saved image after processing
            os.remove(file_path)

            return response.json(), response.status_code
        else:
            return {'error': 'Invalid file type'}, 400

    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self._ALLOWED_EXTENSIONS