"""
Created on 08.04.2018
Defines the REST resources used by the API.
@author: lorinc

"""
import json
import chess.pgn, chess
from flask import Flask, request, Response, g, _request_ctx_stack, redirect
from flask_restful import Resource, Api
from chessApi import database

APIARY_PROJECT = 'https://communitychess.docs.apiary.io'
APIARY_PROFILES = APIARY_PROJECT + '/#reference/profiles/'
APIARY_RELATIONS = APIARY_PROJECT + '/#reference/link-relations/'
MASON = 'application/vnd.mason+json'
JSON = 'application/json'
EXERCISE_PROFILE = '/profiles/exercise-profile/'
ERROR_PROFILE = '/profiles/error-profile/'
LINK_RELATIONS = '/api/link-relations/'
USER_PROFILE = "/profiles/user-profile/"
SOLVER_SOLUTION = 'SOLUTION'
SOLVER_PARTIAL = 'PARTIAL'
SOLVER_WRONG = 'WRONG'

app = Flask(__name__)
app.debug = True
app.config.update({'Engine': database.Engine()})
api = Api(app)


class ChessApiObject(dict):
    """
    A convenience class that provides shorthands to add hypermedia-specific
    key-value pairs to a dictionary object. The used hypermedia format is MASON.
    The class can be used for constructing the response bodies for the REST
    resource requests.
    """
    def __init__(self, self_href, profile, add_namespace=True, **kwargs):
        """
        On initialization some MASON fields can be added to the dictionary.
        :param self_href: The url of the resource.
        :param profile: The profile associated with the resource.
        :param add_namespace: Wheter add the default namespace defined by `LINK_RELATIONS`
        :param kwargs: Additional dictionary arguments.
        """
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
        """
        Add another MASON @control object to the dictionary.
        :param name: Name of the control.
        :param href: Url of the control.
        :param method: Optional. HTTP method of the control.
        """
        self['@controls'][name] = {
            'href': href
        }
        if method:
            self['@controls'][name]['method'] = method

    def add_add_exercise_control(self):
        """
        Shorthand for adding the chessapi:add-exercise control to the object.
        """
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
        """
        Shorthand for adding the edit control to the object.
        """
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
        """
        Shorthand for adding the chessapi:exercise-solver control to the object.
        """
        self['@controls']['chessapi:exercise-solver'] = {
            'title': 'Exercise Solver',
            'href': api.url_for(Solver, exerciseid=exerciseid)[0:-1] + '{?solution}',
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
        """
        Shorthand for adding the chessapi:users-all control to the object.
        """
        self.add_control('chessapi:users-all', api.url_for(Users), 'GET')


def _check_existing_nickname(nickname):
    """
    Checks if a user with a given nickname is present in the database or not.
    :param nickname: The nickname to be checked.
    :return: `True` if the user with the nickname is present.
    """
    return g.con.get_user(nickname) is not None


def _check_author_email(nickname, submitted_mail):
    """
    Checks if the given email address matches the one in the database.
    :param nickname: The user's nickname whose email address is being checked.
    :param submitted_mail: The email address which needs to be checked if it's the same as in the db.
    :return: `True` if the submitted email address matches the one in the database.
    """
    user = g.con.get_user(nickname)
    return user['email'] == submitted_mail


def _check_chess_data(initial_state, list_moves, checkmate_needed=True):
    """
    Checks if a given initial board state and a list of SAN moves is valid with the rules of chess.
    :param initial_state: FEN string of the initial board state.
    :param list_moves: Comma-separated list of SAN moves.
    :param checkmate_needed: Wheter it's required to have a checkmate at the end of the moves or not.
    :return: `True` if the provided data is valid chess-wise.
    """
    # TODO weiping : update documentation. we're not using PGN anymore, but a simpler notation
    # which consists of comma-separated SAN entries
    # to be updated:
    #   - confluence
    #   - apairy
    #   - response dictioanries
    #   - testing dictionaries
    try:
        # check if initial state is valid
        board = chess.Board(initial_state)
        # test the list of moves
        moves = list_moves.split(',')
        for san_move in moves:
            board.push_san(san_move)
    except ValueError:
        return False
    # valid exercise ends with checkmate
    return not checkmate_needed or board.is_checkmate()


def _check_free_exercise_title(title):
    """
    Checks if the given exercise headline exists already in the database.
    :param title: The headline string to be checked.
    :return: `True` if the given headline does not exist in the database.
    """
    exercises_db = g.con.get_exercises()
    return not any(map(lambda ex: ex['title'] == title, exercises_db))


def _compare_exercise_solution(solution, proposed):
    """
    Compares a proposed solution string with the actual solution of the exercise.
    :param solution: The 'real' solution of the exercise.
    :param proposed: The proposed solution.
    :return: `SOLVER_SOLUTION` if the proposed solution is the actual solution.
        `SOLVER_PARTIAL` if the proposed solution is the beginning of the actual solution.
        `SOLVER_WRONG` otherwise.
    """
    if solution == proposed:
        return SOLVER_SOLUTION
    if solution.find(proposed) == 0:
        return SOLVER_PARTIAL
    return SOLVER_WRONG


def _create_exercise_items_list(exercises_db):
    """
    From a list of exercises fetched from the database creates a list of exercise object which can be returned
    by the API.
    :param exercises_db: The list of exercises fetched from the database.
    :return: The list of exercises as hypermedia objects (MASON).
    """
    items = []
    if not exercises_db:
        return items
    for exercise_db in exercises_db:
        ex = ChessApiObject(api.url_for(Exercise, exerciseid=exercise_db['exercise_id']), EXERCISE_PROFILE, False)
        ex['headline'] = exercise_db['title']
        ex['author'] = exercise_db['author']
        items.append(ex)
    return items


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
    return Response(json.dumps(envelope), status_code, mimetype=MASON + ';' + ERROR_PROFILE)


def _check_free_user_nickname(nickname):
    """
    Checks if the given exercise headline exists already in the database.
    :param title: The headline string to be checked.
    :return: `True` if the given headline does not exist in the database.
    """
    user_db = g.con.get_users()
    return not any(map(lambda ex: ex['nickname'] == nickname, user_db))


BAD_JSON_RESP = create_error_response(400, 'Wrong request format', JSON + ' is required')
EXISTING_TITLE_RESP = create_error_response(400, 'Existing exercise headline',
                                            'The provided headline already exists in the database')
EXISTING_NICKNAME_RESP = create_error_response(400, 'Existing nickname headline',
                                            'The provided nickname already exists in the database.')
MISSING_USER_RESP = create_error_response(404, 'User not found',
                                          'The provided nickname does not exist in the database.')
WRONG_AUTH_RESP = create_error_response(401, 'Wrong authentication',
                                        'The provided email address does not match the one in the database.')
INVALID_CHESS_DATA_RESP = create_error_response(400,
                                                'Invalid chess data', 'Provided initial board state should be '
                                                'valid FEN code. List of moves should be comma separated SAN codes. '
                                                'The exercise should end with checkmate.')
BAD_SOLUTION_QUERY = create_error_response(400, 'Bad query',
                                           'Provide a valid comma separated SAN movelist as a query. '
                                           'Consider the initial state of the board.')
DB_PROBLEM_RESP = create_error_response(500, 'Problem with the database', 'Cannot access database')


def missing_exercise_response(exerciseid):
    return create_error_response(404, 'Exercise does not exist', 'There is no exercise with id ' + exerciseid)


def existing_nickname_response(nickname):
    return create_error_response(404, 'Nickname exist', 'Choose another nickname' + nickname)


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
    # TODO weiping
    # - code
    # - docstrings
    # - tests
    # - check if the error responses are present in apiary
    def get(self):
        pass

    def post(self):
        pass


class User(Resource):
    # TODO antonio
    # - code
    # - docstrings
    # - tests
    # - check if the error responses are present in apiary
    """
        User Resource.
    """

    def get(self, nickname):
        """
           Get basic information of a user:

           INPUT PARAMETER:
          : param str nickname: Nickname of the required user.

           OUTPUT:
            * Return 200 if the nickname exists.
            * Return 404 if the nickname is not stored in the system.

           RESPONSE ENTITY BODY:

           * Media type : application/vnd.mason+json
           * Profile : application/vnd.mason+json

           Link relations used: self, collection, user-public.

           Semantic descriptors used: nickname and registrationdate
        """
        user_db = g.con.get_user(nickname)
        if not user_db:
            return create_error_response(404, 'Non existing resource',
                                         'There is no user with this nickname ' + nickname)

        regdate = user_db['registrationdate']
        nickname = user_db['nickname']

        envelope = ChessApiObject(api.url_for(User, nickname=nickname), USER_PROFILE, registrationdate=regdate, nickname=nickname)
        envelope.add_control("profile", USER_PROFILE)
        envelope.add_control("collection", href=api.url_for(Users))
        envelope.add_control("self", href=api.url_for(User, nickname=nickname))
        envelope.add_control("chessapi:user-submission", href=api.url_for(Submissions, nickname=nickname))
        envelope.add_control("chessapi:all-exercises", href=api.url_for(Exercises))
        envelope.add_control("chessapi:delete", api.url_for(User, nickname=nickname), "DELETE")
        string_data = json.dumps(envelope)
        return Response(string_data, 200, mimetype=MASON + ';' + USER_PROFILE)

    def put(self, nickname):
        # Check if the user exists
        if not g.con.get_user(nickname):
            return existing_nickname_response(nickname)

        # Check if the requested data is valid JSON
        if JSON != request.headers.get('Content-Type'):
            return BAD_JSON_RESP
        request_body = request.get_json(force=True)

        # extract fields
        try:
            nickname = request_body['nickname']
            email = request_body['email']
            former_ermail = request_body['former_email']
        except KeyError:
            return create_error_response(400, 'Missing fields',
                                         'Be sure you to fill the nickname field,'
                                         'email and former email field.')
        # check if the user exists

        # check if the email addresses match

        # check if new nickname exists already
        if not _check_free_user_nickname(nickname):
               return EXISTING_NICKNAME_RESP

        if nickname != g.con.modify_user(nickname, email):
            return DB_PROBLEM_RESP
        return Response(status=204)

    def delete(self, nickname):
        """
               Delete a user in the system.

              : param str nickname: Nickname of the required user.

               RESPONSE STATUS CODE:
                * If the user is deleted returns 204.
                * If the nickname does not exist return 404
               """
        if g.con.delete_user(nickname):
            return "", 204
        else:
            return create_error_response(404, "Unknown nickname",
                                         "There is no a user with nickname %s" % nickname
                                         )

class Submissions(Resource):
    """
    Resource that represents a list of exercises submitted by a particular user.
    """
    def get(self, nickname):
        """
        Implementation of the response to a GET request to a Submissions resource.
        The returned list of items is empty if there is no exercises submitted by the user.
        The format of the list is defined in `_create_exercise_items_list` function.
        HTTP status codes:
            200 - the list of exercises is returned correctly
            404 - the user with `nickname` does not exist
            500 - database error
        :param nickname: The nickname of the user.
        :return: flask.Response of the status code and response body.
        """
        # check if user exists
        if not g.con.get_user(nickname):
            return MISSING_USER_RESP

        # create and add controls to the envelope
        envelope = ChessApiObject(api.url_for(Submissions, nickname=nickname), EXERCISE_PROFILE)
        envelope.add_control('up', api.url_for(User, nickname=nickname))

        # get list of exercises submitted by the user with `nickname`
        exercises_db = g.con.get_exercises(nickname)
        envelope['items'] = _create_exercise_items_list(exercises_db)

        # response
        return Response(json.dumps(envelope), 200, mimetype=MASON+';'+EXERCISE_PROFILE)


class Exercises(Resource):
    """
    Resource that represents the list of chess exercises.
    """
    def get(self):
        """
        Implmentation of the response to a GET request to the Exercises resource.
        Returns empty list when there's no exercises in the database.
        HTTP status codes:
            200 - the list of exercises retrieved correctly
            500 - database error
        :return: flask.Response of the status code and response body.
        """
        # create envelope and add controls to it
        envelope = ChessApiObject(api.url_for(Exercises), EXERCISE_PROFILE)
        envelope.add_add_exercise_control()
        envelope.add_users_all_control()

        # get the list of exercises from the database and add them to the envelope - with a minimal format
        exercises_from_db = g.con.get_exercises()
        items = _create_exercise_items_list(exercises_from_db)

        envelope['items'] = items
        return Response(json.dumps(envelope), 200, mimetype=MASON + ';' + EXERCISE_PROFILE)

    def post(self):
        """
        Implementation of the addition of a new exercise to the database via POST HTTP request.
        HTTP status codes:
            201 - the new exercise has been created correctly.
            400 - the Content-Type of the request is not JSON
            400 - some required fields are missing from the request body
            400 - the exercise title is already taken
            401 - the email address of the author does not match the email address in the database
            404 - the user with the given nickname does not exist
            500 - database error
        :return: flask.Response of the status code.
        """
        # Check if json
        if JSON != request.headers.get('Content-Type', ''):
            return BAD_JSON_RESP
        request_body = request.get_json(force=True)

        # check if has every required field
        try:
            headline = request_body['headline']
            author = request_body['author']
            author_email = request_body['author-email']
            initial_state = request_body['initial-state']
            list_moves = request_body['list-moves']
        except KeyError:
            return create_error_response(400, 'Missing fields',
                                         'Be sure you include exercise headline,'
                                         'author, author-mail, initial-state and list-moves.')

        # about is not required
        about = request_body.get('about')

        # check if exercise title exists already
        if not _check_free_exercise_title(headline):
            return EXISTING_TITLE_RESP

        # check if nickname exists
        if not _check_existing_nickname(author):
            return MISSING_USER_RESP

        # validate author
        if not _check_author_email(author, author_email):
            return WRONG_AUTH_RESP

        # check if sent data is valid chess-wise
        if not _check_chess_data(initial_state, list_moves):
            return INVALID_CHESS_DATA_RESP

        # everything is ok - add the exercise to the database
        new_id = g.con.create_exercise(headline, about, author, initial_state, list_moves)
        if not new_id:
            return DB_PROBLEM_RESP
        url = api.url_for(Exercise, exerciseid=new_id)
        return Response(status=201, headers={'Location': url})


class Exercise(Resource):
    """
    Resource representation of the chess exercises.
    """
    def get(self, exerciseid):
        """
        Implementation of the response to a GET request to the Exercise resource.
        HTTP status codes:
            200 - the exercise data is retrieved correctly
            404 - the exercise with the given id does not exist
            500 - database error
        :param exerciseid: the identifier number of the exercise
        :return: flask.Response of the status code and response body.
        """
        # fetch exercise from database
        exercise_db = g.con.get_exercise(exerciseid)
        if not exercise_db:
            return missing_exercise_response(exerciseid)

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

        return Response(json.dumps(envelope), 200, mimetype=MASON + ';' + EXERCISE_PROFILE)

    def put(self, exerciseid):
        """
        Implementation of modifying an exercise via a PUT request.
        HTTP status codes:
            204 - the exercise has been correctly modified
            400 - the Content-Type of the request is not JSON
            400 - some required fields are missing from the request body
            400 - the new exercise title is already taken
            401 - the provided email address of the user does not match the one in the database
            404 - the exercise with the given id does not exist
            500 - database error
        :param exerciseid: the identifier number of the exercise
        :return: flask.Response of the status code and response body.
        """
        # check if the exercise exists
        if not g.con.get_exercise(exerciseid):
            return missing_exercise_response(exerciseid)

        # check if the request data is valid JSON
        if JSON != request.headers.get('Content-Type'):
            return BAD_JSON_RESP
        request_body = request.get_json(force=True)

        # extract fields
        try:
            headline = request_body['headline']
            initial_state = request_body['initial-state']
            list_moves = request_body['list-moves']
            author_email = request_body['author-email']
        except KeyError:
            return create_error_response(400, 'Missing fields',
                                         'Be sure you include exercise headline,'
                                         'author-mail, initial-state and list-moves.')
        # about is not required
        about = request_body.get('about')
        author = g.con.get_exercise(exerciseid)['author']

        # check if exercise title exists already
        if not _check_free_exercise_title(headline):
            return EXISTING_TITLE_RESP

        # validate author
        if not _check_author_email(author, author_email):
            return WRONG_AUTH_RESP

        # check if sent data is valid chess-wise
        if not _check_chess_data(initial_state, list_moves):
            return INVALID_CHESS_DATA_RESP

        if exerciseid != g.con.modify_exercise(exerciseid, headline, about, initial_state, list_moves):
            return DB_PROBLEM_RESP
        return Response(status=204)

    def delete(self, exerciseid):
        """
        Implementation of deleting an exercise via a DELETE HTTP request.
        The email address of the author is required for authentication purposes as an url query.
        HTTP status codes:
            204 - the exercise has been successfully deleted
            401 - the provided email address does not match the one in the database
            404 - the exercise with the given id does not exist
            500 - database error
        :param exerciseid: the identifier number of the exercise
        :return: flask.Response of the status code and response body.
        """
        # check if exercise exists
        exercise_db = g.con.get_exercise(exerciseid)
        if not exercise_db:
            return missing_exercise_response(exerciseid)

        # check that the provided email matches the one in the database
        query_email = request.args.get('author_email')
        if not _check_author_email(exercise_db['author'], query_email):
            return WRONG_AUTH_RESP

        # delete exercise from db
        if not g.con.delete_exercise(exerciseid):
            return DB_PROBLEM_RESP
        return Response(status=204)


class Solver(Resource):
    """
    Resource representation of the exercise solver.
    """
    def get(self, exerciseid):
        """
        Performs the response to the GET request to the Solver resource.
        A query string containing a comma-separated list of SAN moves has to be provided.
        The returned data's `value` field reports if the query is the solution, part of the solution or invalid.
        HTTP status codes:
            200 - the solver data returned correctly
            400 - the provided solution query is not a valid SAN movelist for the current exercise
            404 - the exercise with the given id does not exist
            500 - database error
        :param exerciseid: the identifier number of the exercise
        :return: flask.Response of the status code and response body.
        """
        # check if exercise exists
        exercise_db = g.con.get_exercise(exerciseid)
        if not exercise_db:
            return missing_exercise_response(exerciseid)

        # fetch the query list-moves
        proposed_solution = request.args.get('solution')

        # check if the query is valid for the board
        if not _check_chess_data(exercise_db['initial_state'], proposed_solution, False):
            return BAD_SOLUTION_QUERY

        # compare query with real solution
        result = _compare_exercise_solution(exercise_db['list_moves'], proposed_solution)

        # create and return the envelope object
        envelope = ChessApiObject(api.url_for(Solver, exerciseid=exerciseid), EXERCISE_PROFILE)
        envelope.add_control('up', api.url_for(Exercise, exerciseid=exerciseid))
        envelope['value'] = result
        return Response(json.dumps(envelope), 200, mimetype=MASON+';'+EXERCISE_PROFILE)


@app.route('/api/profiles/<profile_name>/')
def redirect_to_profile(profile_name):
    return redirect(APIARY_PROFILES + profile_name)


@app.route('/api/link-relations/<rel_name>/')
def redirect_to_rels(rel_name):
    return redirect(APIARY_RELATIONS + rel_name)


api.add_resource(Users, "/api/users/", endpoint="users")
api.add_resource(User, "/api/users/<nickname>/", endpoint="user")
api.add_resource(Submissions, "/api/users/<nickname>/submissions/", endpoint="submissions")
api.add_resource(Exercises, "/api/exercises/", endpoint="exercises")
api.add_resource(Exercise, "/api/exercises/<exerciseid>/", endpoint="exercise")
api.add_resource(Solver, "/api/exercises/<exerciseid>/solver/", endpoint="solver")

if __name__ == '__main__':
    app.run(debug=True)
