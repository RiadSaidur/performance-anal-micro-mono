import newrelic.agent
newrelic.agent.initialize('newrelic.ini')

from flask import Flask, send_from_directory
from flask_restful import Api

from resources.person import Person

app = Flask(__name__)
api = Api()

api.add_resource(Person, "/upload")

_UPLOAD_FOLDER = 'uploads'

@app.route('/temporary/<filename>')
def uploaded_file(filename):
    return send_from_directory(_UPLOAD_FOLDER, filename)

# Route to serve static files (uploaded images)
@app.route('/uploads/<path:filename>')
def serve_static(filename):
    return send_from_directory(_UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    # initialize the api with the app context
    api.init_app(app)

    # run the server
    app.run(host='0.0.0.0', port=8000, debug=True)
