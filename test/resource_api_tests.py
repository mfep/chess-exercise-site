"""
Created on 09.04.2018
@author: lorinc
"""

import unittest
import json
import flask
import chessApi.database as database
import chessApi.resources as resources

DB_PATH = 'db/chessApi_test.db'
ENGINE = database.Engine(DB_PATH)
CONTENT_TYPE = 'Content-Type'
DEFAULT_BOARD_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
CUSTOM_BOARD_FEN = 'rnbqkbnr/pppppppp/5q2/8/8/5P2/PPPPP1PP/RNBQKBNR w KQkq - 0 1'
FOOLS_MATE_MOVES = 'f3,e5,g4,Qh4#'
NON_CHECKMATE_MOVES = 'Nc3,d5,Ne4,dxe4'
CUSTOM_MOVES = 'g4,Qh4#'
GOT_EXERCISES = {
    '@controls': {
        'chessapi:users-all': {
            'method': 'GET',
            'href': '/api/users/'
        },
        'profile': {
            'href': '/profiles/exercise-profile/'
        },
        'self': {
            'href': '/api/exercises/'
        },
        'chessapi:add-exercise': {
            'schema': {
                'type': 'object',
                'properties': {
                    'headline': {
                        'type': 'string',
                        'title': 'Headline',
                        'description': 'Exercise title'
                    },
                    'list-moves': {
                        'type': 'string',
                        'title': 'List of moves',
                        'description': 'PGN code movelist of the exercise solution'
                    },
                    'initial-state': {
                        'type': 'string',
                        'title': 'Initial state',
                        'description': 'FEN code of the initial board state'
                    },
                    'about': {
                        'type': 'string',
                        'title': 'About',
                        'description': 'Exercise description'
                    },
                    'author-email': {
                        'type': 'string',
                        'title': 'Author Email',
                        'description': 'The author\'s email address. Used for authentication.'
                    },
                    'author': {
                        'type': 'string',
                        'title': 'Author',
                        'description': 'Submitter of the exercise'
                    }
                },
                'required': ['headline', 'intial-state', 'list-moves', 'author', 'author-email']
            },
            'method': 'POST',
            'encoding': 'json',
            'title': 'Submit a new exercise',
            'href': '/api/exercises/'
        }
    },
    '@namespaces': {
        'chessapi': {
            'name': '/api/link-relations/'
        }
    },
    'items': [{
        'headline': 'Fool Mate',
        '@controls': {
            'profile': {
                'href': '/profiles/exercise-profile/'
            },
            'self': {
                'href': '/api/exercises/1/'
            }
        },
        'author': 'Mystery'
    }, {
        'headline': 'Fool Mate II',
        '@controls': {
            'profile': {
                'href': '/profiles/exercise-profile/'
            },
            'self': {
                'href': '/api/exercises/2/'
            }
        },
        'author': 'Mystery'
    }, {
        'headline': 'Simple bishop',
        '@controls': {
            'profile': {
                'href': '/profiles/exercise-profile/'
            },
            'self': {
                'href': '/api/exercises/3/'
            }
        },
        'author': 'Koodari'
    }]
}
ADD_EXERCISE_VALID_DATA = {
  'headline': 'Newly added',
  'about': 'No need for description',
  'author': 'AxelW',
  'author-email': 'axelw@mymail.com',
  'initial-state': 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',
  'list-moves': 'f3,e5,g4,Qh4#'
}
ADDED_EXERCISE_LOCATION = 'http://localhost:5000/api/exercises/4/'
GOT_EXERCISE = {
    '@namespaces': {
        'chessapi': {
            'name': '/api/link-relations/'
        }
    },
    'initial-state': 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',
    'dateCreated': 1519061565,
    'about': 'The quickest checkmate available.',
    'author': 'Mystery',
    'list-moves': 'f3,e5,g4,Qh4#',
    '@controls': {
        'collection': {
            'href': '/api/exercises/'
        },
        'chessapi:delete': {
            'method': 'DELETE',
            'href': '/api/exercises/1/'
        },
        'author': {
            'href': '/api/users/Mystery/'
        },
        'self': {
            'href': '/api/exercises/1/'
        },
        'edit': {
            'schema': {
                'required': ['headline', 'intial-state', 'list-moves', 'author-email'],
                'type': 'object',
                'properties': {
                    'initial-state': {
                        'type': 'string',
                        'description': 'FEN code of the initial board state',
                        'title': 'Initial state'
                    },
                    'author-email': {
                        'type': 'string',
                        'description': 'The author\'s email address. Used for authentication.',
                        'title': 'Author Email'
                    },
                    'headline': {
                        'type': 'string',
                        'description': 'Exercise title',
                        'title': 'Headline'
                    },
                    'about': {
                        'type': 'string',
                        'description': 'Exercise description',
                        'title': 'About'
                    },
                    'list-moves': {
                        'type': 'string',
                        'description': 'PGN code movelist of the exercise solution',
                        'title': 'List of moves'
                    }
                }
            },
            'encoding': 'json',
            'method': 'PUT',
            'href': '/api/exercises/1/',
            'title': 'Edit this exercise'
        },
        'profile': {
            'href': '/profiles/exercise-profile/'
        },
        'chessapi:exercise-solver': {
            'schema': {
                'type': 'object',
                'required': ['solution'],
                'properties': {
                    'solution': {
                        'type': 'string',
                        'description': 'PGN code of the proposed solution of the exercise.'
                    }
                }
            },
            'isHrefTemplate': True,
            'method': 'GET',
            'href': '/api/exercises/1/solver{?solution}',
            'title': 'Exercise Solver'
        }
    },
    'headline': 'Fool Mate'
}
MODIFY_EXERCISE_VALID_DATA = {
    'headline': 'from chess.com',
    'about': 'No need for description',
    'author-email': 'mystery@mymail.com',
    'initial-state': 'r1bq1bkr/ppp3pp/2n5/3Qp3/2B5/8/PPPP1PPP/RNBQK1NR b KQkq - 0 1',
    'list-moves': 'Qxd5,Bxd5+,Be6,Bxe6#'
}

resources.app.config['Testing'] = True
resources.app.config['SERVER_NAME'] = 'localhost:5000'
resources.app.config.update({'Engine': ENGINE})


# TODO document code
class ResourcesApiTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Testing ', cls.__name__)
        ENGINE.remove_database()
        ENGINE.create_tables()

    @classmethod
    def tearDownClass(cls):
        print('Testing ended for ', cls.__name__)
        ENGINE.remove_database()

    def setUp(self):
        ENGINE.populate_tables()
        self.app_context = resources.app.app_context()
        self.app_context.push()
        self.client = resources.app.test_client()

    def tearDown(self):
        ENGINE.clear()
        self.app_context.pop()

    def _assertErrorMessage(self, resp, code, message):
        self.assertEqual(code, resp.status_code)
        data = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(message, data['@error']['@message'])


class ExercisesTestCase(ResourcesApiTestCase):
    url = '/api/exercises/'

    def test_database_contains_valid_chess_data(self):
        """Tests if the default database contains chess data reported as valid"""
        print('(' + self.test_database_contains_valid_chess_data.__name__ + ')',
              self.test_database_contains_valid_chess_data.__doc__)
        engine = database.Engine()
        con = engine.connect()
        for exercise_list_item in con.get_exercises():
            exercise_data = con.get_exercise(exercise_list_item['exercise_id'])
            self.assertTrue(resources._check_chess_data(exercise_data['initial_state'], exercise_data['list_moves']))

    def test_check_chess_data_default_board(self):
        """Tests if checkmate from default board state is reported as correct"""
        print('(' + self.test_check_chess_data_default_board.__name__ + ')',
              self.test_check_chess_data_default_board.__doc__)
        self.assertTrue(resources._check_chess_data(DEFAULT_BOARD_FEN, FOOLS_MATE_MOVES))

    def test_check_chess_data_custom_board(self):
        """Tests if checkmate from custom initial state is reported as correct"""
        print('(' + self.test_check_chess_data_custom_board.__name__ + ')',
              self.test_check_chess_data_custom_board.__doc__)
        self.assertTrue(resources._check_chess_data(CUSTOM_BOARD_FEN, CUSTOM_MOVES))

    def test_check_chess_data_nonsense_board(self):
        """Tests if nonsense board is reported as incorrect"""
        print('(' + self.test_check_chess_data_nonsense_board.__name__ + ')',
              self.test_check_chess_data_nonsense_board.__doc__)
        self.assertFalse(resources._check_chess_data(DEFAULT_BOARD_FEN[3:-2], FOOLS_MATE_MOVES))

    def test_check_chess_data_non_checkmate(self):
        """Tests if an exercise not resulting in checkmate is reported as invalid"""
        print('(' + self.test_check_chess_data_non_checkmate.__name__ + ')',
              self.test_check_chess_data_non_checkmate.__doc__)
        self.assertFalse(resources._check_chess_data(DEFAULT_BOARD_FEN, NON_CHECKMATE_MOVES))

    def test_url(self):
        """Checks that the URL points to the right resource"""
        print('('+self.test_url.__name__+')', self.test_url.__doc__)
        with resources.app.test_request_context(self.url):
            rule = flask.request.url_rule
            view_point = resources.app.view_functions[rule.endpoint].view_class
            self.assertEqual(view_point, resources.Exercises)

    def test_get_exercises(self):
        """Checks if exercises GET request works correctly"""
        print('(' + self.test_get_exercises.__name__ + ')', self.test_get_exercises.__doc__)
        resp = self.client.get(flask.url_for('exercises'))
        self.assertEqual(200, resp.status_code)
        self.assertEqual(resources.MASON + ';' + resources.EXERCISE_PROFILE, resp.headers.get(CONTENT_TYPE))
        data = json.loads(resp.data.decode('utf-8'))
        self.assertDictEqual(data, GOT_EXERCISES)

    def test_add_exercise_valid(self):
        """Check if valid exercise data can be added"""
        print('(' + self.test_add_exercise_valid.__name__ + ')', self.test_add_exercise_valid.__doc__)
        resp = self.client.post(resources.api.url_for(resources.Exercises),
                                headers={CONTENT_TYPE: resources.JSON},
                                data=json.dumps(ADD_EXERCISE_VALID_DATA))
        self.assertEqual(201, resp.status_code)
        self.assertEqual(ADDED_EXERCISE_LOCATION, resp.headers.get('Location'))

    def test_add_exercise_not_json(self):
        """Check if error code is correct when Content-Type is not set"""
        print('(' + self.test_add_exercise_not_json.__name__ + ')', self.test_add_exercise_not_json.__doc__)
        resp = self.client.post(resources.api.url_for(resources.Exercises),
                                data=json.dumps(ADD_EXERCISE_VALID_DATA))
        self._assertErrorMessage(resp, 400, 'Wrong request format')

    def test_add_exercise_missing_fields(self):
        """Check if error code is correct when not all fields are provided in request"""
        print('(' + self.test_add_exercise_missing_fields.__name__ + ')', self.test_add_exercise_missing_fields.__doc__)
        request_data = ADD_EXERCISE_VALID_DATA.copy()
        request_data.pop('author')
        resp = self.client.post(resources.api.url_for(resources.Exercises),
                                headers={CONTENT_TYPE: resources.JSON},
                                data=json.dumps(request_data))
        self._assertErrorMessage(resp, 400, 'Missing fields')

    def test_add_exercise_existing_title(self):
        """Check if error code is correct when an existing exercise name is provided"""
        print('(' + self.test_add_exercise_existing_title.__name__ + ')', self.test_add_exercise_existing_title.__doc__)
        request_data = ADD_EXERCISE_VALID_DATA.copy()
        request_data['headline'] = 'Fool Mate'
        resp = self.client.post(resources.api.url_for(resources.Exercises),
                                headers={CONTENT_TYPE: resources.JSON},
                                data=json.dumps(request_data))
        self._assertErrorMessage(resp, 400, 'Existing exercise headline')

    def test_add_exercise_not_existing_user(self):
        """Check if error code is correct when a non-existing username is provided"""
        print('(' + self.test_add_exercise_not_existing_user.__name__ + ')',
              self.test_add_exercise_not_existing_user.__doc__)
        request_data = ADD_EXERCISE_VALID_DATA.copy()
        request_data['author'] = 'Animal'
        resp = self.client.post(resources.api.url_for(resources.Exercises),
                                headers={CONTENT_TYPE: resources.JSON},
                                data=json.dumps(request_data))
        self._assertErrorMessage(resp, 404, 'User not found')

    def test_add_exercise_invalid_email(self):
        """Check if error code is correct when the provided email does not match the one in the database"""
        print('(' + self.test_add_exercise_invalid_email.__name__ + ')', self.test_add_exercise_invalid_email.__doc__)
        request_data = ADD_EXERCISE_VALID_DATA.copy()
        request_data['author-email'] = 'hacker@mymail.com'
        resp = self.client.post(resources.api.url_for(resources.Exercises),
                                headers={CONTENT_TYPE: resources.JSON},
                                data=json.dumps(request_data))
        self._assertErrorMessage(resp, 401, 'Wrong authentication')

    def test_add_exercise_invalid_chess_data(self):
        """Check if error code is correct when invalid chess data is sent"""
        print('(' + self.test_add_exercise_invalid_chess_data.__name__ + ')',
              self.test_add_exercise_invalid_chess_data.__doc__)
        request_data = ADD_EXERCISE_VALID_DATA.copy()
        request_data['list-moves'] = NON_CHECKMATE_MOVES
        resp = self.client.post(resources.api.url_for(resources.Exercises),
                                headers={CONTENT_TYPE: resources.JSON},
                                data=json.dumps(request_data))
        self._assertErrorMessage(resp, 400, 'Invalid chess data')

    def test_get_exercise(self):
        """Check if exercise data can be retrieved"""
        print('(' + self.test_get_exercise.__name__ + ')', self.test_get_exercise.__doc__)
        resp = self.client.get(resources.api.url_for(resources.Exercise, exerciseid=1))
        self.assertEqual(200, resp.status_code)
        self.assertEqual(resources.MASON + ';' + resources.EXERCISE_PROFILE, resp.headers.get(CONTENT_TYPE))
        data = json.loads(resp.data.decode('utf-8'))
        self.assertDictEqual(GOT_EXERCISE, data)

    def test_get_exercise_non_existing(self):
        """Check error code when 404ing exercise"""
        print('(' + self.test_get_exercise_non_existing.__name__ + ')', self.test_get_exercise_non_existing.__doc__)
        resp = self.client.get(resources.api.url_for(resources.Exercise, exerciseid=100))
        self._assertErrorMessage(resp, 404, 'Exercise does not exist')

    def test_modify_exercise_valid(self):
        """Check if exercise can be modified via PUT request."""
        print('(' + self.test_modify_exercise_valid.__name__ + ')', self.test_modify_exercise_valid.__doc__)
        exercise_id = 1
        resp = self.client.put(resources.api.url_for(resources.Exercise, exerciseid=exercise_id),
                               headers={CONTENT_TYPE: resources.JSON},
                               data=json.dumps(MODIFY_EXERCISE_VALID_DATA))
        self.assertEqual(204, resp.status_code)
        resp = self.client.get(resources.api.url_for(resources.Exercise, exerciseid=exercise_id))
        self.assertEqual(200, resp.status_code)
        data = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(MODIFY_EXERCISE_VALID_DATA['headline'], data['headline'])
        self.assertEqual(MODIFY_EXERCISE_VALID_DATA['about'], data['about'])
        self.assertEqual(MODIFY_EXERCISE_VALID_DATA['list-moves'], data['list-moves'])
        self.assertEqual(MODIFY_EXERCISE_VALID_DATA['initial-state'], data['initial-state'])

    def test_modify_exercise_non_existing(self):
        print('(' + self.test_modify_exercise_non_existing.__name__ + ')',
              self.test_modify_exercise_non_existing.__doc__)
        exercise_id = 100
        resp = self.client.put(resources.api.url_for(resources.Exercise, exerciseid=exercise_id),
                               headers={CONTENT_TYPE: resources.JSON},
                               data=json.dumps(MODIFY_EXERCISE_VALID_DATA))
        self._assertErrorMessage(resp, 404, 'Exercise does not exist')

    def test_modify_exercise_not_json(self):
        print('(' + self.test_modify_exercise_not_json.__name__ + ')', self.test_modify_exercise_not_json.__doc__)
        exercise_id = 1
        resp = self.client.put(resources.api.url_for(resources.Exercise, exerciseid=exercise_id),
                               data=json.dumps(MODIFY_EXERCISE_VALID_DATA))
        self._assertErrorMessage(resp, 400, 'Wrong request format')

    def test_modify_exercise_missing_fields(self):
        print('(' + self.test_modify_exercise_missing_fields.__name__ + ')',
              self.test_modify_exercise_missing_fields.__doc__)
        request_data = MODIFY_EXERCISE_VALID_DATA.copy()
        request_data.pop('headline')
        exercise_id = 1
        resp = self.client.put(resources.api.url_for(resources.Exercise, exerciseid=exercise_id),
                               headers={CONTENT_TYPE: resources.JSON},
                               data=json.dumps(request_data))
        self._assertErrorMessage(resp, 400, 'Missing fields')

    def test_modify_exercise_existing_title(self):
        print('(' + self.test_modify_exercise_existing_title.__name__ + ')',
              self.test_modify_exercise_existing_title.__doc__)
        request_data = MODIFY_EXERCISE_VALID_DATA.copy()
        request_data['headline'] = 'Simple bishop'
        exercise_id = 1
        resp = self.client.put(resources.api.url_for(resources.Exercise, exerciseid=exercise_id),
                               headers={CONTENT_TYPE: resources.JSON},
                               data=json.dumps(request_data))
        self._assertErrorMessage(resp, 400, 'Existing exercise headline')

    def test_modify_exercise_invalid_email(self):
        print('(' + self.test_modify_exercise_invalid_email.__name__ + ')',
              self.test_modify_exercise_invalid_email.__doc__)
        request_data = MODIFY_EXERCISE_VALID_DATA.copy()
        request_data['author-email'] = 'hacker@mymail.com'
        exercise_id = 1
        resp = self.client.put(resources.api.url_for(resources.Exercise, exerciseid=exercise_id),
                               headers={CONTENT_TYPE: resources.JSON},
                               data=json.dumps(request_data))
        self._assertErrorMessage(resp, 401, 'Wrong authentication')

    def test_modify_exercise_invalid_chess_data(self):
        print('(' + self.test_modify_exercise_invalid_chess_data.__name__ + ')',
              self.test_modify_exercise_invalid_chess_data.__doc__)
        request_data = MODIFY_EXERCISE_VALID_DATA.copy()
        request_data['list-moves'] = NON_CHECKMATE_MOVES
        exercise_id = 1
        resp = self.client.put(resources.api.url_for(resources.Exercise, exerciseid=exercise_id),
                               headers={CONTENT_TYPE: resources.JSON},
                               data=json.dumps(request_data))
        self._assertErrorMessage(resp, 400, 'Invalid chess data')


if __name__ == '__main__':
    print('Start running tests')
    unittest.main()
