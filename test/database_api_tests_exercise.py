"""
Created on 20.02.2018
@author: lorinc

"""

import unittest
import sqlite3
from chessApi import database

DB_PATH = 'db/chessApi_test.db'
ENGINE = database.Engine(DB_PATH)

INITIAL_EXERCISE_SIZE = 3
EXERCISE1 = {
    'exercise_id': 1,
    'user_id': 1,
    'title': 'Easy one',
    'description': 'No need to explain this.',
    'sub_date': 1519061565,
    'initial_state': 'VALIDFENFEN',
    'list_moves': 'VALIDPGNPGN'
}


class ExerciseApiDbTestCase(unittest.TestCase):
    """Test cases for the Exercise related methods."""
    @classmethod
    def tearDownClass(cls):
        """Remove the testing database"""
        print("Testing ENDED for ", cls.__name__)
        ENGINE.remove_database()
        ENGINE.create_tables()

    def setUp(self):
        """Populates the database"""
        ENGINE.populate_tables()
        self.connection = ENGINE.connect()

    def tearDown(self):
        """Close underlying connection and remove all records from database"""
        self.connection.close()
        ENGINE.clear()

    def test_exercise_table_created(self):
        """Checks if exercises table has been created with 3 rows."""
        print('('+self.test_exercise_table_created.__name__+')',
              self.test_exercise_table_created.__doc__)

        keys_on = 'PRAGMA foreign_keys = ON'
        query1 = 'SELECT * FROM exercises'
        con = self.connection.con
        with con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute(keys_on)
            cur.execute(query1)
            exercises = cur.fetchall()
            self.assertEqual(len(exercises), INITIAL_EXERCISE_SIZE)

    def test_exercise_get_valid(self):
        """Checks if existing exercise row is returned correctly"""
        exercise = self.connection.get_exercise(1)
        self.assertDictEqual(exercise, EXERCISE1)

    def test_exercise_get_invalid(self):
        """Checks if None is returned for non-existing exercise"""
        self.assertIsNone(self.connection.get_exercise(5))


if __name__ == '__main__':
    print('Start running user tests')
    unittest.main()
