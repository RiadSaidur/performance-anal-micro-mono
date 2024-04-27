from flask import Flask
from flask_restful import Api

from app.routes.faceRecognition_routes import FaceRecognition

app = Flask(__name__)
api = Api(app)

api.add_resource(FaceRecognition, '/find/')

if __name__ == "__main__":
    # run the server
    app.run(host='0.0.0.0', port=8000, debug=True)