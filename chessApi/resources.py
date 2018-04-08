"""
Created on 08.04.2018
Defines the REST resources used by the API.
@author: lorinc

"""
import json
from flask import Flask, request, Response, g, _request_ctx_stack
from flask_restful import Resource, Api
from chessApi import database

MASON = 'application/vnd.mason+json'
JSON = 'application/json'
ERROR_PROFILE = '/profiles/error-profile'
LINK_RELATIONS = '/api/link-relations/'

app = Flask(__name__)
app.debug = True
app.config.update({'Engine': database.Engine()})
api = Api(app)


class ChessApiObject(dict):
    def __init__(self, **kwargs):
        super(ChessApiObject, self).__init__(**kwargs)
        self['@namespaces'] = {
            'chessapi': {
                'name': LINK_RELATIONS
            }
        }


def create_error_response(status_code, title, message=None):
    """
    Creates a: py: class:`flask.Response` instance when sending back an
    HTTP error response

    : param integer status_code: The HTTP status code of the response
    : param str title: A short description of the problem
    : param message: A long description of the problem
    : rtype:: py: class:`flask.Response`
    """

    resource_url = None
    ctx = _request_ctx_stack.top
    if ctx is not None:
        resource_url = request.path
    envelope = {
        'resource_url': resource_url,
        '@error': {
            '@message': title,
            '@messages': [message]
        }
    }
    return Response(json.dumps(envelope), status_code, mimetype=MASON+';'+ERROR_PROFILE)


@app.errorhandler(400)
def resource_not_found(error):
    return create_error_response(400, "Malformed input format",
                                 "The format of the input is incorrect")


@app.errorhandler(404)
def resource_not_found(error):
    return create_error_response(404, "Resource not found",
                                 "This resource url does not exit")


@app.errorhandler(500)
def unknown_error(error):
    return create_error_response(500, "Internal error",
                                 "The system has failed. Please, contact the administrator")


@app.before_request
def connect_db():
    """
    Creates a database connection before the request is proccessed.

    The connection is stored in the application context variable flask.g .
    Hence it is accessible from the request object.
    """

    g.con = app.config["Engine"].connect()


@app.teardown_request
def close_connection(exc):
    """
    Closes the database connection
    Check if the connection is created. It migth be exception appear before
    the connection is created.
    """

    if hasattr(g, "con"):
        g.con.close()


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