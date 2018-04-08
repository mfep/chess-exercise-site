"""
Created on 08.04.2018
Defines the REST resources used by the API.
@author: lorinc

"""

from flask import Flask
from flask_restful import Resource, Api
from chessApi import database

app = Flask(__name__)
app.debug = True
app.config.update({'Engine': database.Engine()})
api = Api(app)


class MasonObject(dict):
    def __init__(self, **kwargs):
        super(MasonObject, self).__init__(**kwargs)


class Users(Resource):
    def get(self):
        pass

    def post(self):
        pass


class User(Resource):
    def get(self, nickname):
        pass

    def put(self, nickname):
        pass

    def delete(self, nickname):
        pass


class Submissions(Resource):
    def get(self, nickname):
        pass


class Exercises(Resource):
    def get(self):
        pass

    def post(self):
        pass


class Exercise(Resource):
    def get(self, exerciseid):
        pass

    def put(self, exerciseid):
        pass

    def delete(self, exerciseid):
        pass


class Solver(Resource):
    def get(self, exerciseid, proposed_solution):
        pass


api.add_resource(Users,       "/api/users/", endpoint="users")
api.add_resource(User,        "/api/users/<nickname>/", endpoint="user")
api.add_resource(Submissions, "/api/users/<nickname>/submissions/", endpoint="submissions")
api.add_resource(Exercises,   "/api/exercises/", endpoint="exercises")
api.add_resource(Exercise,    "/api/exercises/<exerciseid>/", endpoint="exercise")
api.add_resource(Solver,      "/api/exercises/<exerciseid>/solver/", endpoint="solver")

if __name__ == '__main__':
    app.run(debug=True)