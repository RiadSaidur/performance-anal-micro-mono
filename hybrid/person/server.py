from flask import Flask, send_from_directory
from flask_restful import Api

from app.routes.person_routes import Person

app = Flask(__name__)
api = Api(app)

_UPLOAD_FOLDER = 'uploads'

api.add_resource(Person, '/upload')

@app.route('/uploads/<path:filename>')
def serve_static(filename):
    return send_from_directory(_UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    # run the server
    app.run(host='0.0.0.0', port=8000, debug=True)
