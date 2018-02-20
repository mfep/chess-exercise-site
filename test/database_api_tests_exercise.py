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


if __name__ == '__main__':
    print('Start running user tests')
    unittest.main()
