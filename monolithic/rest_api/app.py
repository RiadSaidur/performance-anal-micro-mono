import newrelic.agent
newrelic.agent.initialize('newrelic.ini')

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api

from resources.user import SignUp, SignIn
from resources.movie import Movies, AddMovie, EditMovie, RemoveMovie
from resources.rating import RateMovie
from resources.database import db, DbSetup

app = Flask(__name__)
api = Api()

app.config["SECRET_KEY"] = "iC&diiDF^6754rSycvYDFXydhg08uvh"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] =  True
jwt = JWTManager(app)

api.add_resource(SignUp, "/signup")
api.add_resource(SignIn, "/signin")
api.add_resource(Movies, "/movies")
api.add_resource(AddMovie, "/movies")
api.add_resource(EditMovie, "/movies/<int:pk>")
api.add_resource(RemoveMovie, "/movies/<int:pk>")
api.add_resource(RateMovie, "/rating/<int:movie_id>")

if __name__ == "__main__":

    # initialize the database with the app context
    db.init_app(app)

    with app.app_context():
        '''Initialize the database and stored records'''
        DbSetup()

    # initialize the api with the app context
    api.init_app(app)

    # run the server
    app.run(host='0.0.0.0', port=5001, debug=True)
