from flask import request, url_for
from flask_restful import Resource
import os
from werkzeug.utils import secure_filename
import uuid
from app.database.person_database import saveImage, saveMissingPersonEncodings
from app.services.faceRecognition_services import findEncodings

_UPLOAD_FOLDER = 'uploads'

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def delete_image(filename):
    image_path = os.path.join(_UPLOAD_FOLDER, filename)
    if os.path.exists(image_path):
        os.remove(image_path)


class Person(Resource):
    def post(self):
        if 'file' not in request.files:
            print(request.files)
            return {'error': 'No file part'}, 400

        file = request.files['file']

        try:
            public_url = None
            unique_filename = None

            if file.filename == '':
                return {'error': 'No selected file'}

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)

                # Generate unique filename
                unique_filename = str(uuid.uuid4())[:8] + '_' + filename

                file.save(os.path.join(_UPLOAD_FOLDER, unique_filename))

                saveImage(unique_filename)

                print(unique_filename)

                public_url = url_for('serve_static', filename=unique_filename, _external=True)

            missingPersonURL = public_url
            missingPersonId = unique_filename

            images = [missingPersonURL]
            encodeList = findEncodings(images)

            delete_image(unique_filename)

            if not encodeList:
              return { "successful": False, "error": "Image not found" }, 404
            
            isSaved = saveMissingPersonEncodings(encodeList, missingPersonId)

            if isSaved:
              return { "successful": True }, 201
            
            return { "successful": False, "error": "Unable to store on Database" }, 500
        except KeyError:
            return { "successful": False, "error": "Invalid arguments" }, 400
        except FileNotFoundError as e:
          return { "successful": False, "error": "Image not found" }, 404
        except Exception as e:
            return {'error': str(e)}, 500