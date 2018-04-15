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
                        'description': 'comma-separated SAN entries movelist of the exercise solution'
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

GOT_USERS = {
   "@namespaces": {
      "chessapi": {
         "name": "/api/link-relations/"
      }
   },
   "@controls": {
      "self": {
         "href": "/api/users/"
      },
      "profile": {
         "href":"/profiles/user-profile/"
      },
      "chessapi:users-all": {
         "href": "/api/users/",
         "method": "GET"
      },
      "chessapi:add-user": {
         "title": "Add a new user",
         "href": "/api/users/",
         "encoding": "json",
         "method": "POST",
         "schema": {
            "type": "object",
            "properties": {
               "nickname": {
                  "title": "Nickname",
                  "description": " Unique id string of the user",
                  "type": "string"
               },
               "email": {
                  "title": "Email address",
                  "description": "email address of the user.",
                  "type": "string"
               }
            },
            "required": [
               "nickname",
               "email"
            ]
         }
      }
   },
   "items": [
      {
         "nickname": "Mystery",
         "registrationdate": 1362015937,
         "@controls": {
            "self": {
               "href": "/api/users/Mystery/"
            },
            "profile": {
               "href": "/profiles/user-profile/"
            }
         }
      },
      {
         "nickname": "AxelW",
         "registrationdate": 1357724086,
         "@controls": {
            "self": {
               "href": "/api/users/AxelW/"
            },
            "profile": {
               "href": "/profiles/user-profile/"
            }
         }
      },
      {
         "nickname": "LinuxPenguin",
         "registrationdate": 1362012937,
         "@controls": {
            "self": {
               "href": "/api/users/LinuxPenguin/"
            },
            "profile": {
               "href": "/profiles/user-profile/"
            }
         }
      },
      {
         "nickname": "Koodari",
         "registrationdate": 1389260086,
         "@controls": {
            "self": {
               "href": "/api/users/Koodari/"
            },
            "profile": {
               "href": "/profiles/user-profile/"
            }
         }
      },
      {
         "nickname": "HockeyFan",
         "registrationdate": 1394357686,
         "@controls": {
            "self": {
               "href": "/api/users/HockeyFan/"
            },
            "profile": {
               "href": "/profiles/user-profile/"
            }
         }
      }
   ]
}
ADD_USER_VALID_DATA = {
  'nickname': 'Harri',
  'email': 'Harri@gmail.com'
}
ADDED_USER_LOCATION = 'http://localhost:5000/api/user/harri/'

resources.app.config['Testing'] = True
resources.app.config['SERVER_NAME'] = 'localhost:5000'
resources.app.config.update({'Engine': ENGINE})
# Other database parameters.
initial_users = 2

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
        self.assertEqual(resp.status_code, code)
        data = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(data['@error']['@message'], message)


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
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers.get(CONTENT_TYPE), resources.MASON + ';' + resources.EXERCISE_PROFILE)
        data = json.loads(resp.data.decode('utf-8'))
        self.assertDictEqual(data, GOT_EXERCISES)

    def test_add_exercise_valid(self):
        """Check if valid exercise data can be added"""
        print('(' + self.test_add_exercise_valid.__name__ + ')', self.test_add_exercise_valid.__doc__)
        resp = self.client.post(resources.api.url_for(resources.Exercises),
                                headers={CONTENT_TYPE: resources.JSON},
                                data=json.dumps(ADD_EXERCISE_VALID_DATA))
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.headers.get('Location'), ADDED_EXERCISE_LOCATION)

    def test_add_exercise_not_json(self):
        """Check if error code is correct when Content-Type is not set"""
        print('(' + self.test_add_exercise_not_json.__name__ + ')', self.test_add_exercise_not_json.__doc__)
        resp = self.client.post(resources.api.url_for(resources.Exercises),
                                data=json.dumps(ADD_EXERCISE_VALID_DATA))
        self._assertErrorMessage(resp, 415, 'Wrong request format')

    def test_add_exercise_missing_fields(self):
        """Check if error code is correct when not all fields are provided in request"""
        print('(' + self.test_add_exercise_missing_fields.__name__ + ')', self.test_add_exercise_missing_fields.__doc__)
        request_data = ADD_EXERCISE_VALID_DATA.copy()
        request_data.pop('author')
        resp = self.client.post(resources.api.url_for(resources.Exercises),
                                headers={CONTENT_TYPE: resources.JSON},
                                data=json.dumps(request_data))
        self._assertErrorMessage(resp, 400, 'Wrong request format')

    def test_add_exercise_existing_title(self):
        """Check if error code is correct when an existing exercise name is provided"""
        print('(' + self.test_add_exercise_existing_title.__name__ + ')', self.test_add_exercise_existing_title.__doc__)
        request_data = ADD_EXERCISE_VALID_DATA.copy()
        request_data['headline'] = 'Fool Mate'
        resp = self.client.post(resources.api.url_for(resources.Exercises),
                                headers={CONTENT_TYPE: resources.JSON},
                                data=json.dumps(request_data))
        self._assertErrorMessage(resp, 409, 'Existing exercise headline')

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
        self._assertErrorMessage(resp, 400, 'Wrong request format')


class UsersTestCase (ResourcesApiTestCase):
    url = "/api/users/"

    def test_url(self):
        """Checks that the URL points to the right resource"""
        print('('+self.test_url.__name__+')', self.test_url.__doc__)
        with resources.app.test_request_context(self.url):
            rule = flask.request.url_rule
            view_point = resources.app.view_functions[rule.endpoint].view_class
            self.assertEqual(view_point, resources.Users)

    def test_get_users(self):
        """Checks if exercises GET request works correctly"""
        print('(' + self.test_get_users.__name__ + ')', self.test_get_users.__doc__)
        resp = self.client.get(flask.url_for('users'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers.get(CONTENT_TYPE), resources.MASON + ';' + resources.USER_PROFILE)
        data = json.loads(resp.data.decode('utf-8'))
        self.assertDictEqual(data, GOT_USERS)


if __name__ == '__main__':
    print('Start running tests')
    unittest.main()
