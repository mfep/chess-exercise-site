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

DEFAULT_BOARD_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
CUSTOM_BOARD_FEN = 'rnbqkbnr/pppppppp/5q2/8/8/5P2/PPPPP1PP/RNBQKBNR w KQkq - 0 1'
FOOLS_MATE_MOVES = 'f3,e5,g4,Qh4#'
NON_CHECKMATE_MOVES = 'Nc3,d5,Ne4,dxe4'
CUSTOM_MOVES = 'g4,Qh4#'

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


class ExercisesTestCase(ResourcesApiTestCase):
    url = '/api/exercises/'

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
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data.decode('utf-8'))
        self.assertDictEqual(data, {
            'items': [{
                'headline': 'Easy one',
                'author': 'Mystery',
                '@controls': {
                    'self': {
                        'href': '/api/exercises/1/'
                    },
                    'profile': {
                        'href': '/profiles/exercise-profile/'
                    }
                }
            }, {
                'headline': 'Easier one',
                'author': 'Mystery',
                '@controls': {
                    'self': {
                        'href': '/api/exercises/2/'
                    },
                    'profile': {
                        'href': '/profiles/exercise-profile/'
                    }
                }
            }, {
                'headline': 'Tough',
                'author': 'Koodari',
                '@controls': {
                    'self': {
                        'href': '/api/exercises/3/'
                    },
                    'profile': {
                        'href': '/profiles/exercise-profile/'
                    }
                }
            }],
            '@namespaces': {
                'chessapi': {
                    'name': '/api/link-relations/'
                }
            },
            '@controls': {
                'self': {
                    'href': '/api/exercises/'
                },
                'chessapi:add-exercise': {
                    'method': 'POST',
                    'schema': {
                        'properties': {
                            'about': {
                                'description': 'Exercise description',
                                'type': 'string',
                                'title': 'About'
                            },
                            'initial-state': {
                                'description': 'FEN code of the initial board state',
                                'type': 'string',
                                'title': 'Initial state'
                            },
                            'list-moves': {
                                'description': 'PGN code movelist of the exercise solution',
                                'type': 'string',
                                'title': 'List of moves'
                            },
                            'author-email': {
                                'description': 'The author\'s email address. Used for authentication.',
                                'type': 'string',
                                'title': 'Author Email'
                            },
                            'headline': {
                                'description': 'Exercise title',
                                'type': 'string',
                                'title': 'Headline'
                            },
                            'author': {
                                'description': 'Submitter of the exercise',
                                'type': 'string',
                                'title': 'Author'
                            }
                        },
                        'required': ['headline', 'intial-state', 'list-moves', 'author', 'author-email'],
                        'type': 'object'
                    },
                    'encoding': 'json',
                    'title': 'Submit a new exercise',
                    'href': '/api/exercises/'
                },
                'chessapi:users-all': {
                    'method': 'GET',
                    'href': '/api/users/'
                },
                'profile': {
                    'href': '/profiles/exercise-profile/'
                }
            }
        })


if __name__ == '__main__':
    print('Start running tests')
    unittest.main()
