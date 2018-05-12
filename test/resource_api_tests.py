"""
Created on 09.04.2018
@author: lorinc
"""

import unittest
import json
import flask
import urllib.parse
import chessApi.database as database
import chessApi.resources as resources

DB_PATH = 'db/chessApi_test.db'
ENGINE = database.Engine(DB_PATH)
CONTENT_TYPE = 'Content-Type'
DEFAULT_BOARD_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
CUSTOM_BOARD_FEN = 'rnbqkbnr/pppppppp/5q2/8/8/5P2/PPPPP1PP/RNBQKBNR w KQkq - 0 1'
FOOLS_MATE_MOVES = 'f3,e5,g4,Qh4#'
FOOLS_MATE_MOVES_BEGINNING = 'f3,e5'
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
                        'description': 'comma-separated SAN entries movelist of the exercise solution',
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
EXERCISE_1_AUTHOR_MAIL = 'mystery@mymail.com'
GOT_SOLVER = {
    '@namespaces': {
        'chessapi': {
            'name': '/api/link-relations/'
        }
    },
    '@controls': {
        'up': {
            'href': '/api/exercises/1/'
        },
        'self': {
            'href': '/api/exercises/1/solver/'
        },
        'profile': {
            'href': '/profiles/exercise-profile/'
        }
    },
    'value': 'SOLUTION'
}
GOT_SUBMISSIONS_NONEMPTY = {
    '@controls': {
        'profile': {
            'href': '/profiles/exercise-profile/'
        },
        'up': {
            'href': '/api/users/Mystery/'
        },
        'self': {
            'href': '/api/users/Mystery/submissions/'
        }
    },
    'items': [{
        '@controls': {
            'profile': {
                'href': '/profiles/exercise-profile/'
            },
            'self': {
                'href': '/api/exercises/1/'
            }
        },
        'headline': 'Fool Mate',
        'author': 'Mystery'
    }, {
        '@controls': {
            'profile': {
                'href': '/profiles/exercise-profile/'
            },
            'self': {
                'href': '/api/exercises/2/'
            }
        },
        'headline': 'Fool Mate II',
        'author': 'Mystery'
    }],
    '@namespaces': {
        'chessapi': {
            'name': '/api/link-relations/'
        }
    }
}
GOT_SUBMISSIONS_EMPTY = {
    '@controls': {
        'up': {
            'href': '/api/users/AxelW/'
        },
        'self': {
            'href': '/api/users/AxelW/submissions/'
        },
        'profile': {
            'href': '/profiles/exercise-profile/'
        }
    },
    'items': [],
    '@namespaces': {
        'chessapi': {
            'name': '/api/link-relations/'
        }
    }
}
GOT_USER = {
    "@namespaces": {
        "chessapi": {
            "name": "/api/link-relations/"
        }
    },
    "@controls": {
        "self": {
            "href": "/api/users/Mystery/"
        },
        "collection": {
            "href": "/api/users/"
        },
        "profile": {
            "href": "/profiles/user-profile/"
        },
        "chessapi:delete": {
            "href": "/api/users/Mystery/",
            "method": "DELETE"
        },
        "chessapi:all-exercises": {
            "href": "/api/exercises/"
        },
        "chessapi:user-submission": {
            "href": "/api/users/Mystery/submissions/"
        }
    },
    "nickname": "Mystery",
    "registrationdate": 1362015937
}
MODIFY_USER_VALID_DATA = {
    'nickname': 'chess.com',
    'email': 'chess@gmail.com',
    'former_email': 'mystery@mymail.com'
}


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
         "href": "/profiles/user-profile/"
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
ADDED_USER_LOCATION = 'http://localhost:5000/api/users/Harri/'

resources.app.config['Testing'] = True
resources.app.config['SERVER_NAME'] = 'localhost:5000'
resources.app.config.update({'Engine': ENGINE})
# Other database parameters.
initial_users = 2

class ResourcesApiTestCase(unittest.TestCase):
    """
    Common TestCase methods setup, teardown and convenience methods.
    """
    @classmethod
    def setUpClass(cls):
        """
        Creates the database structure. Removes any pre-existing database file.
        """
        print('Testing ', cls.__name__)
        ENGINE.remove_database()
        ENGINE.create_tables()

    @classmethod
    def tearDownClass(cls):
        """
        Removes the database file.
        """
        print('Testing ended for ', cls.__name__)
        ENGINE.remove_database()

    def setUp(self):
        """
        Populates the database.
        """
        ENGINE.populate_tables()
        self.app_context = resources.app.app_context()
        self.app_context.push()
        self.client = resources.app.test_client()

    def tearDown(self):
        """
        Removes all records from the database.
        """
        ENGINE.clear()
        self.app_context.pop()

    def _assertErrorMessage(self, resp, code, message):
        """
        Convenience method for asserting on MASON responses of 40X status codes.
        :param resp: flask.Response object
        :param code: HTTP status code to expect
        :param message: Error message to expect
        """
        self.assertEqual(code, resp.status_code)
        data = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(message, data['@error']['@message'])


class ExercisesTestCase(ResourcesApiTestCase):
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
        url = '/api/exercises/'
        with resources.app.test_request_context(url):
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
        """Check if error code is correct when Content-Type is not set. Displays error code 415"""
        print('(' + self.test_add_exercise_not_json.__name__ + ')', self.test_add_exercise_not_json.__doc__)
        resp = self.client.post(resources.api.url_for(resources.Exercises),
                                data=json.dumps(ADD_EXERCISE_VALID_DATA))
        self._assertErrorMessage(resp, 415, 'Wrong request format')

    def test_add_exercise_missing_fields(self):
        """Check if error code is correct when not all fields are provided in request. Displays error code 400."""
        print('(' + self.test_add_exercise_missing_fields.__name__ + ')', self.test_add_exercise_missing_fields.__doc__)
        request_data = ADD_EXERCISE_VALID_DATA.copy()
        request_data.pop('author')
        resp = self.client.post(resources.api.url_for(resources.Exercises),
                                headers={CONTENT_TYPE: resources.JSON},
                                data=json.dumps(request_data))
        self._assertErrorMessage(resp, 400, 'Missing fields')

    def test_add_exercise_existing_title(self):
        """Check if error code is correct when an existing exercise name is provided. Displays error code 409."""
        print('(' + self.test_add_exercise_existing_title.__name__ + ')', self.test_add_exercise_existing_title.__doc__)
        request_data = ADD_EXERCISE_VALID_DATA.copy()
        request_data['headline'] = 'Fool Mate'
        resp = self.client.post(resources.api.url_for(resources.Exercises),
                                headers={CONTENT_TYPE: resources.JSON},
                                data=json.dumps(request_data))
        self._assertErrorMessage(resp, 409, 'Existing exercise headline')

    def test_add_exercise_not_existing_user(self):
        """Check if error code is correct when a non-existing username is provided. Displays error code 404."""
        print('(' + self.test_add_exercise_not_existing_user.__name__ + ')',
              self.test_add_exercise_not_existing_user.__doc__)
        request_data = ADD_EXERCISE_VALID_DATA.copy()
        request_data['author'] = 'Animal'
        resp = self.client.post(resources.api.url_for(resources.Exercises),
                                headers={CONTENT_TYPE: resources.JSON},
                                data=json.dumps(request_data))
        self._assertErrorMessage(resp, 404, 'User does not exist')

    def test_add_exercise_invalid_email(self):
        """Check if error code is correct when the provided email does not match the one in the database.
         Displays error code 401."""
        print('(' + self.test_add_exercise_invalid_email.__name__ + ')', self.test_add_exercise_invalid_email.__doc__)
        request_data = ADD_EXERCISE_VALID_DATA.copy()
        request_data['author-email'] = 'hacker@mymail.com'
        resp = self.client.post(resources.api.url_for(resources.Exercises),
                                headers={CONTENT_TYPE: resources.JSON},
                                data=json.dumps(request_data))
        self._assertErrorMessage(resp, 401, 'Wrong authentication')

    def test_add_exercise_invalid_chess_data(self):
        """Check if error code is correct when invalid chess data is sent. Displays error code 400."""
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
        """Checks if error message is correct when trying to modify non-existing exercise. Displays error code 404."""
        print('(' + self.test_modify_exercise_non_existing.__name__ + ')',
              self.test_modify_exercise_non_existing.__doc__)
        exercise_id = 100
        resp = self.client.put(resources.api.url_for(resources.Exercise, exerciseid=exercise_id),
                               headers={CONTENT_TYPE: resources.JSON},
                               data=json.dumps(MODIFY_EXERCISE_VALID_DATA))
        self._assertErrorMessage(resp, 404, 'Exercise does not exist')

    def test_modify_exercise_not_json(self):
        """Checks if error message is correct when request format is not set. Displays error code 415."""
        print('(' + self.test_modify_exercise_not_json.__name__ + ')', self.test_modify_exercise_not_json.__doc__)
        exercise_id = 1
        resp = self.client.put(resources.api.url_for(resources.Exercise, exerciseid=exercise_id),
                               data=json.dumps(MODIFY_EXERCISE_VALID_DATA))
        self._assertErrorMessage(resp, 415, 'Wrong request format')

    def test_modify_exercise_missing_fields(self):
        """Checks if error message is correct when required fields are missing from the request body. Error code 400."""
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
        """Checks if error message is correct when trying to set the exercise headline to an existing one.
         Error code 409."""
        print('(' + self.test_modify_exercise_existing_title.__name__ + ')',
              self.test_modify_exercise_existing_title.__doc__)
        request_data = MODIFY_EXERCISE_VALID_DATA.copy()
        request_data['headline'] = 'Simple bishop'
        exercise_id = 1
        resp = self.client.put(resources.api.url_for(resources.Exercise, exerciseid=exercise_id),
                               headers={CONTENT_TYPE: resources.JSON},
                               data=json.dumps(request_data))
        self._assertErrorMessage(resp, 409, 'Existing exercise headline')

    def test_modify_exercise_invalid_email(self):
        """Checks if error message is correct when the provided user's email does
         not match the one in the database. Error code 401."""
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
        """Checks if error message is correct when the provided chess data is not valid. Displays error code 400."""
        print('(' + self.test_modify_exercise_invalid_chess_data.__name__ + ')',
              self.test_modify_exercise_invalid_chess_data.__doc__)
        request_data = MODIFY_EXERCISE_VALID_DATA.copy()
        request_data['list-moves'] = NON_CHECKMATE_MOVES
        exercise_id = 1
        resp = self.client.put(resources.api.url_for(resources.Exercise, exerciseid=exercise_id),
                               headers={CONTENT_TYPE: resources.JSON},
                               data=json.dumps(request_data))
        self._assertErrorMessage(resp, 400, 'Invalid chess data')

    def test_delete_exercise(self):
        """Checks if exercises can be deleted. Displays error code 404."""
        print('(' + self.test_delete_exercise.__name__ + ')', self.test_delete_exercise.__doc__)
        exercise_id = 1
        resp = self.client.delete(resources.api.url_for(resources.Exercise, exerciseid=exercise_id)
                                  + '?author_email=mystery%40mymail.com')
        self.assertEqual(204, resp.status_code)
        resp = self.client.get(resources.api.url_for(resources.Exercise, exerciseid=exercise_id))
        self._assertErrorMessage(resp, 404, 'Exercise does not exist')

    def test_delete_exercise_non_existing(self):
        """Checks if error message is correct when a non-existing exercise is tried to be deleted.
         Displays error code 404."""
        print('(' + self.test_delete_exercise_non_existing.__name__ + ')',
              self.test_delete_exercise_non_existing.__doc__)
        exercise_id = 100
        resp = self.client.delete(resources.api.url_for(resources.Exercise, exerciseid=exercise_id)
                                  + '?author_email=mystery%40mymail.com')
        self._assertErrorMessage(resp, 404, 'Exercise does not exist')

    def test_delete_exercise_invalid_email(self):
        """Checks if error message is correct when an exercise is to be deleted with an invalid author email.
         Displays error code 401."""
        print('(' + self.test_delete_exercise_invalid_email.__name__ + ')',
              self.test_delete_exercise_invalid_email.__doc__)
        exercise_id = 1
        resp = self.client.delete(resources.api.url_for(resources.Exercise, exerciseid=exercise_id)
                                  + '?author_email=hacker%40mymail.com')
        self._assertErrorMessage(resp, 401, 'Wrong authentication')

    def test_solver_value_solution(self):
        """Checks solver module if the result is correct for identical strings"""
        print('(' + self.test_solver_value_solution.__name__ + ')', self.test_solver_value_solution.__doc__)
        self.assertEqual(resources.SOLVER_SOLUTION,
                         resources._compare_exercise_solution(FOOLS_MATE_MOVES, FOOLS_MATE_MOVES))

    def test_solver_value_partial(self):
        """Checks solver module if the result is correct for beginning substring"""
        print('(' + self.test_solver_value_partial.__name__ + ')', self.test_solver_value_partial.__doc__)
        self.assertEqual(resources.SOLVER_PARTIAL,
                         resources._compare_exercise_solution(FOOLS_MATE_MOVES, FOOLS_MATE_MOVES_BEGINNING))

    def test_solver_value_wrong(self):
        """Checks solver module if the result is correct for entirely different string"""
        print('(' + self.test_solver_value_wrong.__name__ + ')', self.test_solver_value_wrong.__doc__)
        self.assertEqual(resources.SOLVER_WRONG,
                         resources._compare_exercise_solution(FOOLS_MATE_MOVES, NON_CHECKMATE_MOVES))

    def test_get_solver(self):
        """Checks if solver GET works"""
        print('(' + self.test_get_solver.__name__ + ')', self.test_get_solver.__doc__)
        exercise_id = 1
        resp = self.client.get(resources.api.url_for(resources.Solver, exerciseid=exercise_id) +
                               '?solution='+urllib.parse.quote_plus(FOOLS_MATE_MOVES))
        self.assertEqual(200, resp.status_code)
        self.assertDictEqual(GOT_SOLVER, json.loads(resp.data.decode('utf-8')))

    def test_get_solver_non_existing(self):
        """Checks error message when trying to access a non-existing exercise's solver. Displays error code 404."""
        print('(' + self.test_get_solver_non_existing.__name__ + ')', self.test_get_solver_non_existing.__doc__)
        exercise_id = 100
        resp = self.client.get(resources.api.url_for(resources.Solver, exerciseid=exercise_id) +
                               '?solution='+urllib.parse.quote_plus(FOOLS_MATE_MOVES))
        self._assertErrorMessage(resp, 404, 'Exercise does not exist')

    def test_get_solver_no_query(self):
        """Checks error message when no solution query is provided. Displays error code 400."""
        print('(' + self.test_get_solver_no_query.__name__ + ')', self.test_get_solver_no_query.__doc__)
        exercise_id = 1
        resp = self.client.get(resources.api.url_for(resources.Solver, exerciseid=exercise_id))
        self._assertErrorMessage(resp, 400, 'Bad query')

    def test_get_solver_nonsense_query(self):
        """Checks error message when the provided query string is nonsense. Displays error code 400."""
        print('(' + self.test_get_solver_nonsense_query.__name__ + ')', self.test_get_solver_nonsense_query.__doc__)
        exercise_id = 1
        resp = self.client.get(resources.api.url_for(resources.Solver, exerciseid=exercise_id) +
                               '?solution='+urllib.parse.quote_plus("dksajakldjs"))
        self._assertErrorMessage(resp, 400, 'Bad query')


class UsersTestCase(ResourcesApiTestCase):
    def test_url(self):
        """Checks that the URL points to the right resource"""
        print('('+self.test_url.__name__+')', self.test_url.__doc__)
        url = '/api/users/'
        with resources.app.test_request_context(url):
            rule = flask.request.url_rule
            view_point = resources.app.view_functions[rule.endpoint].view_class
            self.assertEqual(view_point, resources.Users)

    def test_get_submissions(self):
        """Checks if user submissions can be retrieved"""
        print('(' + self.test_get_submissions.__name__ + ')', self.test_get_submissions.__doc__)
        nickname = 'Mystery'
        resp = self.client.get(resources.api.url_for(resources.Submissions, nickname=nickname))
        self.assertEqual(200, resp.status_code)
        self.assertDictEqual(GOT_SUBMISSIONS_NONEMPTY, json.loads(resp.data.decode('utf-8')))

    def test_get_submissions_empty(self):
        """Checks if submissions gives result even when there is no exercises submitted by the user"""
        print('(' + self.test_get_submissions_empty.__name__ + ')', self.test_get_submissions_empty.__doc__)
        nickname = 'AxelW'
        resp = self.client.get(resources.api.url_for(resources.Submissions, nickname=nickname))
        self.assertEqual(200, resp.status_code)
        self.assertDictEqual(GOT_SUBMISSIONS_EMPTY, json.loads(resp.data.decode('utf-8')))

    def test_submissions_non_existing(self):
        """Checks error code when requesting submissions of non-existing user. Displays error code 404."""
        print('(' + self.test_submissions_non_existing.__name__ + ')', self.test_submissions_non_existing.__doc__)
        nickname = 'Hacker'
        resp = self.client.get(resources.api.url_for(resources.Submissions, nickname=nickname))
        self._assertErrorMessage(resp, 404, 'User does not exist')

    def test_get_user(self):
        """Check if user data can be retrieved"""
        print('(' + self.test_get_user.__name__ + ')', self.test_get_user.__doc__)
        nickname = 'Mystery'
        resp = self.client.get(resources.api.url_for(resources.User, nickname=nickname))
        self.assertEqual(200, resp.status_code)
        self.assertEqual(resources.MASON + ';' + resources.USER_PROFILE, resp.headers.get(CONTENT_TYPE))
        data = json.loads(resp.data.decode('utf-8'))
        self.assertDictEqual(GOT_USER, data)

    def test_get_user_non_existing(self):
        """Check error code when 404ing user"""
        print('(' + self.test_get_user_non_existing.__name__ + ')', self.test_get_user_non_existing.__doc__)
        nickname = 'Animal'
        resp = self.client.get(resources.api.url_for(resources.User, nickname=nickname))
        self._assertErrorMessage(resp, 404, 'User does not exist')

    def test_modify_user_valid(self):
        """Check if user can be modified via PUT request."""
        print('(' + self.test_modify_user_valid.__name__ + ')', self.test_modify_user_valid.__doc__)
        nickname = 'Mystery'
        resp = self.client.put(resources.api.url_for(resources.User, nickname=nickname),
                               headers={CONTENT_TYPE: resources.JSON},
                               data=json.dumps(MODIFY_USER_VALID_DATA))
        self.assertEqual(204, resp.status_code)
        resp = self.client.get(resources.api.url_for(resources.User, nickname=MODIFY_USER_VALID_DATA['nickname']))
        self.assertEqual(200, resp.status_code)
        data = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(MODIFY_USER_VALID_DATA['nickname'], data['nickname'])

    def test_modify_user_non_existing(self):
        """Checks if error message is correct when trying to modify non-existing user. Displays error code 404."""
        print('(' + self.test_modify_user_non_existing.__name__ + ')', self.test_modify_user_non_existing.__doc__)
        nickname = 'Animal'
        resp = self.client.put(resources.api.url_for(resources.User, nickname=nickname),
                               headers={CONTENT_TYPE: resources.JSON},
                               data=json.dumps(MODIFY_USER_VALID_DATA))
        self._assertErrorMessage(resp, 404, 'User does not exist')

    def test_modify_user_not_json(self):
        """Checks if error message is correct when request format is not set. Displays error code 415."""
        print('(' + self.test_modify_user_not_json.__name__ + ')', self.test_modify_user_not_json.__doc__)
        nickname = 'Mystery'
        resp = self.client.put(resources.api.url_for(resources.User, nickname=nickname),
                               data=json.dumps(MODIFY_USER_VALID_DATA))
        self._assertErrorMessage(resp, 415, 'Wrong request format')

    def test_modify_user_missing_fields(self):
        """Checks if error message is correct when required fields are missing from the request body.
         Displays error code 400."""
        print('(' + self.test_modify_user_missing_fields.__name__ + ')',
              self.test_modify_user_missing_fields.__doc__)
        request_data = MODIFY_USER_VALID_DATA.copy()
        request_data.pop('nickname')
        nickname = 'Mystery'
        resp = self.client.put(resources.api.url_for(resources.User, nickname=nickname),
                               headers={CONTENT_TYPE: resources.JSON},
                               data=json.dumps(request_data))
        self._assertErrorMessage(resp, 400, 'Missing fields')

    def test_modify_user_existing_nickname(self):
        """Checks if error message is correct when trying to set the user nickname to an existing one.
         Displays error code 409."""
        print('(' + self.test_modify_user_existing_nickname.__name__ + ')',
              self.test_modify_user_existing_nickname.__doc__)
        request_data = MODIFY_USER_VALID_DATA.copy()
        request_data['nickname'] = 'AxelW'
        nickname = 'Mystery'
        resp = self.client.put(resources.api.url_for(resources.User, nickname=nickname),
                               headers={CONTENT_TYPE: resources.JSON},
                               data=json.dumps(request_data))
        self._assertErrorMessage(resp, 409, 'Existing nickname')

    def test_modify_user_invalid_email(self):
        """Checks if error message is correct when the provided user's email does not match the one in the database.
          Displays error code 401."""
        print('(' + self.test_modify_user_invalid_email.__name__ + ')', self.test_modify_user_invalid_email.__doc__)
        request_data = MODIFY_USER_VALID_DATA.copy()
        request_data['former_email'] = 'hacker%40mymail.com'
        nickname = 'Mystery'
        resp = self.client.put(resources.api.url_for(resources.User, nickname=nickname),
                               headers={CONTENT_TYPE: resources.JSON},
                               data=json.dumps(request_data))
        self._assertErrorMessage(resp, 401, 'Wrong authentication')

    def test_delete_user(self):
        """Checks if user can be deleted. Displays error code 404."""
        print('(' + self.test_delete_user.__name__ + ')', self.test_delete_user.__doc__)
        nickname = 'Mystery'
        resp = self.client.delete(resources.api.url_for(resources.User, nickname=nickname)
                                  + '?author_email=mystery%40mymail.com')
        self.assertEqual(204, resp.status_code)
        resp = self.client.get(resources.api.url_for(resources.User, nickname=nickname))
        self._assertErrorMessage(resp, 404, 'User does not exist')

    def test_delete_user_non_existing(self):
        """Checks if error message is correct when a non-existing user is tried to be deleted.
        Displays error code 404."""
        print('(' + self.test_delete_user_non_existing.__name__ + ')',
              self.test_delete_user_non_existing.__doc__)
        nickname = 'Animal'
        resp = self.client.delete(resources.api.url_for(resources.User, nickname=nickname)
                                  + '?author_email=animal%40mymail.com')
        self._assertErrorMessage(resp, 404, 'User does not exist')

    def test_delete_user_invalid_email(self):
        """Checks if error message is correct when a user is to be deleted with invalid authentication email.
        Displays error code 404."""
        print('(' + self.test_delete_user_invalid_email.__name__ + ')', self.test_delete_user_invalid_email.__doc__)
        nickname = 'Mystery'
        resp = self.client.delete(resources.api.url_for(resources.User, nickname=nickname)
                                  + '?author_email=animal%40mymail.com')
        self._assertErrorMessage(resp, 401, 'Wrong authentication')

    def test_get_users(self):
        """Checks if users GET request works correctly"""
        print('(' + self.test_get_users.__name__ + ')', self.test_get_users.__doc__)
        resp = self.client.get(flask.url_for('users'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers.get(CONTENT_TYPE), resources.MASON + ';' + resources.USER_PROFILE)
        data = json.loads(resp.data.decode('utf-8'))
        self.assertDictEqual(data, GOT_USERS)

    def test_add_user_valid(self):
        """Check if valid user data can be added"""
        print('(' + self.test_add_user_valid.__name__ + ')', self.test_add_user_valid.__doc__)
        resp = self.client.post(resources.api.url_for(resources.Users),
                                headers={CONTENT_TYPE: resources.JSON},
                                data=json.dumps(ADD_USER_VALID_DATA))
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.headers.get('Location'), ADDED_USER_LOCATION)

    def test_add_user_not_json(self):
        """Check if error code is correct when Content-Type is not set. Displays error code 415."""
        print('(' + self.test_add_user_not_json.__name__ + ')', self.test_add_user_not_json.__doc__)
        resp = self.client.post(resources.api.url_for(resources.Users),
                                data=json.dumps(ADD_USER_VALID_DATA))
        self._assertErrorMessage(resp, 415, 'Wrong request format')

    def test_add_user_missing_fields(self):
        """Check if error code is correct when not all fields are provided in request. Displays error code 400."""
        print('(' + self.test_add_user_missing_fields.__name__ + ')', self.test_add_user_missing_fields.__doc__)
        request_data = ADD_USER_VALID_DATA.copy()
        request_data.pop('nickname')
        resp = self.client.post(resources.api.url_for(resources.Users),
                                headers={CONTENT_TYPE: resources.JSON},
                                data=json.dumps(request_data))
        self._assertErrorMessage(resp, 400, 'Missing fields')

    def test_add_user_existing_nickname(self):
        """Check if error code is correct when an existing user nickname is provided. Displays error code 409."""
        print('(' + self.test_add_user_existing_nickname.__name__ + ')', self.test_add_user_existing_nickname.__doc__)
        request_data = ADD_USER_VALID_DATA.copy()
        request_data['nickname'] = 'Mystery'
        resp = self.client.post(resources.api.url_for(resources.Users),
                                headers={CONTENT_TYPE: resources.JSON},
                                data=json.dumps(request_data))
        self._assertErrorMessage(resp, 409, 'Nickname already exists')


if __name__ == '__main__':
    print('Start running tests')
    unittest.main()
