"""
Created on 08.04.2018
Defines the REST resources used by the API.
@author: lorinc

"""
import json
import chess.pgn, chess
from io import StringIO
from flask import Flask, request, Response, g, _request_ctx_stack
from flask_restful import Resource, Api
from chessApi import database

MASON = 'application/vnd.mason+json'
JSON = 'application/json'
EXERCISE_PROFILE = '/profiles/exercise-profile/'
ERROR_PROFILE = '/profiles/error-profile'
LINK_RELATIONS = '/api/link-relations/'

app = Flask(__name__)
app.debug = True
app.config.update({'Engine': database.Engine()})
api = Api(app)


class ChessApiObject(dict):
    def __init__(self, self_href, profile, add_namespace=True, **kwargs):
        super(ChessApiObject, self).__init__(**kwargs)
        if add_namespace:
            self['@namespaces'] = {
                'chessapi': {
                    'name': LINK_RELATIONS
                }
            }
        self['@controls'] = {}
        self.add_control('self', self_href)
        self.add_control('profile', profile)

    def add_control(self, name, href, method = None):
        self['@controls'][name] = {
            'href': href
        }
        if method:
            self['@controls'][name]['method'] = method

    def add_add_exercise_control(self):
        self['@controls']['chessapi:add-exercise'] = {
            'title': 'Submit a new exercise',
            'href': api.url_for(Exercises),
            'encoding': 'json',
            'method': 'POST',
            'schema': {
                'type': 'object',
                'properties': {
                    'headline': {
                        'title': 'Headline',
                        'description': 'Exercise title',
                        'type': 'string'
                    },
                    'about': {
                        'title': 'About',
                        'description': 'Exercise description',
                        'type': 'string'
                    },
                    'initial-state': {
                        'title': 'Initial state',
                        'description': 'FEN code of the initial board state',
                        'type': 'string'
                    },
                    'list-moves': {
                        'title': 'List of moves',
                        'description': 'PGN code movelist of the exercise solution',
                        'type': 'string'
                    },
                    'author': {
                        'title': 'Author',
                        'description': 'Submitter of the exercise',
                        'type': 'string'
                    },
                    'author-email': {
                        'title': 'Author Email',
                        'description': 'The author\'s email address. Used for authentication.',
                        'type': 'string'
                    }
                },
                'required': ['headline', 'intial-state', 'list-moves', 'author', 'author-email']
            }
        }

    def add_edit_exercise_control(self, exerciseid):
        self['@controls']['edit'] = {
            'title': 'Edit this exercise',
            'href': api.url_for(Exercise, exerciseid=exerciseid),
            'encoding': 'json',
            'method': 'PUT',
            'schema': {
                'type': 'object',
                'properties': {
                    'headline': {
                        'title': 'Headline',
                        'description': 'Exercise title',
                        'type': 'string'
                    },
                    'about': {
                        'title': 'About',
                        'description': 'Exercise description',
                        'type': 'string'
                    },
                    'initial-state': {
                        'title': 'Initial state',
                        'description': 'FEN code of the initial board state',
                        'type': 'string'
                    },
                    'list-moves': {
                        'title': 'List of moves',
                        'description': 'PGN code movelist of the exercise solution',
                        'type': 'string'
                    },
                    'author-email': {
                        'title': 'Author Email',
                        'description': 'The author\'s email address. Used for authentication.',
                        'type': 'string'
                    }
                },
                'required': ['headline', 'intial-state', 'list-moves', 'author-email']
            }
        }

    def add_solver_control(self, exerciseid):
        self['@controls']['chessapi:exercise-solver'] = {
            'title': 'Exercise Solver',
            'href': api.url_for(Solver, exerciseid=exerciseid)[0:-1]+'{?solution}',
            'method': 'GET',
            'isHrefTemplate': True,
            'schema': {
                'required': ['solution'],
                'type': 'object',
                'properties': {
                    'solution': {
                        'type': 'string',
                        'description': 'PGN code of the proposed solution of the exercise.'
                    }
                }
            }
        }

    def add_users_all_control(self):
        self.add_control('chessapi:users-all', api.url_for(Users), 'GET')


def _check_existing_nickname(nickname):
    return g.con.get_user(nickname) is not None


def _check_author_email(nickname, submitted_mail):
    user = g.con.get_user(nickname)
    return user['email'] == submitted_mail


def _check_chess_data(initial_state, list_moves):
    # TODO test this with real data
    try:
        board = chess.Board(initial_state)
    except ValueError:
        return False
    pgn_stream = StringIO(list_moves)
    game = chess.pgn.read_game(pgn_stream)
    if not game:
        return False
    for move in game.main_line():
        board.push(move)
    return board.is_checkmate()


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
        # create envelope and add controls to it
        envelope = ChessApiObject(api.url_for(Exercises), EXERCISE_PROFILE)
        envelope.add_add_exercise_control()
        envelope.add_users_all_control()

        # get the list of exercises from the database and add them to the envelope - with a minimal format
        exercises_from_db = g.con.get_exercises()
        items = []
        for exercise_db in exercises_from_db:
            ex = ChessApiObject(api.url_for(Exercise, exerciseid=exercise_db['exercise_id']), EXERCISE_PROFILE, False)
            ex['headline'] = exercise_db['title']
            ex['author'] = exercise_db['author']
            items.append(ex)

        envelope['items'] = items
        return Response(json.dumps(envelope), 200, mimetype=MASON+';'+EXERCISE_PROFILE)

    def post(self):
        # TODO update error messages in apiary

        # Check if json
        if JSON != request.headers.get('Content-Type',''):
            return create_error_response(400, 'Wrong request format', JSON+' is required')
        request_body = request.get_json(force=True)

        # check if has every required field
        try:
            headline = request_body['headline']
            author = request_body['author']
            author_email = request_body['author-email']
            initial_state = request_body['initial-state']
            list_moves = request_body['list-moves']
        except KeyError:
            return create_error_response(400, 'Wrong request format',
                                         'Be sure you include exercise headline,'
                                         'author, author-mail, initial-state and list-moves.')

        # about is not required
        about = request_body['about'] if 'about' in request_body else None

        # TODO currently exercise name is unique

        # check if nickname exists
        if not _check_existing_nickname(author):
            return create_error_response(404, 'User not found', 'The provided nickname does not exist in the database.')

        # validate author
        if not _check_author_email(author, author_email):
            return create_error_response(401, 'Wrong authentication',
                                         'The provided email address does not match the one in the database.')

        # check if sent data is valid chess-wise
        if not _check_chess_data(initial_state, list_moves):
            return create_error_response(400, 'Wrong request format', 'provided chess data is not valid')

        # everything is ok - add the exercise to the database
        new_id = g.con.create_exercise(headline, about, author, initial_state, list_moves)
        if not new_id:
            return create_error_response(500, 'Problem with the database', 'Cannot access database')
        url = api.url_for(Exercise, exerciseid=new_id)
        return Response(201, headers={'Location': url})


class Exercise(Resource):
    def get(self, exerciseid):
        # fetch exercise from database
        exercise_db = g.con.get_exercise(exerciseid)
        if not exercise_db:
            return create_error_response(404, 'Exercise does not exist', 'There is no exercise with id ' + exerciseid)

        # create envelope and add controls
        url = api.url_for(Exercise, exerciseid=exerciseid)
        envelope = ChessApiObject(url, EXERCISE_PROFILE)
        envelope.add_control('author', api.url_for(User, nickname=exercise_db['author']))
        envelope.add_control('collection', api.url_for(Exercises))
        envelope.add_edit_exercise_control(exerciseid)
        envelope.add_control('chessapi:delete', url, 'DELETE')
        envelope.add_solver_control(exerciseid)
        envelope['initial-state'] = exercise_db['initial_state']
        envelope['list-moves'] = exercise_db['list_moves']
        envelope['author'] = exercise_db['author']
        envelope['dateCreated'] = exercise_db['sub_date']
        envelope['headline'] = exercise_db['title']
        envelope['about'] = exercise_db['description']

        return Response(json.dumps(envelope), 200, mimetype=MASON+';'+EXERCISE_PROFILE)

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