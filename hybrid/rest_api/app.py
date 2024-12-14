import newrelic.agent
newrelic.agent.initialize('newrelic.ini')

from flask import Flask
from flask_restful import Api

from resources.person import Person

app = Flask(__name__)
api = Api()

api.add_resource(Person, "/upload")

if __name__ == "__main__":
    # initialize the api with the app context
    api.init_app(app)

    # run the server
    app.run(host='0.0.0.0', port=8079, debug=True)
