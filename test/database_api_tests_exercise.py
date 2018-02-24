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
EXERCISE2_MODIFIED = {
    'exercise_id': 2,
    'user_id': 1,
    'title': 'Modified Title',
    'description': 'Description',
    'sub_date': 1443827483,
    'initial_state': 'asd',
    'list_moves': 'dsa'

}

EXERCISE3_create = {
    'exercise_id': 4,
    'user_id': 1,
    'title': 'New Exercise',
    'description': 'Description new',
    'initial_state': 'new state',
    'list_moves': 'new new'
}


class ExerciseApiDbTestCase(unittest.TestCase):
    """Test cases for the Exercise related methods."""
    @classmethod
    def setUpClass(cls):
        """ Creates the database structure. Removes first any preexisting
            database file
        """
        print("Testing ", cls.__name__)
        ENGINE.remove_database()
        ENGINE.create_tables()

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

    def _get_exercise_table_row_count(self):
        """Returns the number of rows currently in exercises table."""
        keys_on = 'PRAGMA foreign_keys = ON'
        query1 = 'SELECT * FROM exercises'
        con = self.connection.con
        with con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute(keys_on)
            cur.execute(query1)
            exercises = cur.fetchall()
            return len(exercises)

    def test_exercise_table_created(self):
        """Checks if exercises table has been created with 3 rows."""
        print('('+self.test_exercise_table_created.__name__+')',
              self.test_exercise_table_created.__doc__)

        self.assertEqual(self._get_exercise_table_row_count(), INITIAL_EXERCISE_SIZE)

    def test_exercise_get_valid(self):
        """Checks if existing exercise row is returned correctly"""
        print('('+self.test_exercise_get_valid.__name__+')',
              self.test_exercise_get_valid.__doc__)

        exercise = self.connection.get_exercise(1)
        self.assertDictEqual(exercise, EXERCISE1)

    def test_exercise_get_invalid(self):
        """Checks if None is returned for non-existing exercise"""
        print('('+self.test_exercise_get_invalid.__name__+')',
              self.test_exercise_get_invalid.__doc__)

        self.assertIsNone(self.connection.get_exercise(100))

    def test_exercise_delete_valid(self):
        """Checks if an existing exercise can be deleted"""
        print('('+self.test_exercise_delete_valid.__name__+')',
              self.test_exercise_delete_valid.__doc__)

        self.assertTrue(self.connection.delete_exercise(2))
        self.assertIsNone(self.connection.get_exercise(2))
        self.assertEqual(self._get_exercise_table_row_count(), INITIAL_EXERCISE_SIZE-1)

    def test_exercise_delete_invalid(self):
        """Checks when a non-existing exercise is to be deleted, the return value is False"""
        print('('+self.test_exercise_delete_invalid.__name__+')',
              self.test_exercise_delete_invalid.__doc__)

        self.assertFalse(self.connection.delete_exercise(100))

    def test_exercise_modify_valid(self):
        """Checks if an existing exercise can be modified"""
        print('(' + self.test_exercise_modify_valid.__name__ + ')',
              self.test_exercise_modify_valid.__doc__)

        value = self.connection.modify_exercise(2, "Modified Title", "Description", "asd", "dsa")
        self.assertEqual(value, 2)
        self.assertDictEqual(self.connection.get_exercise(2), EXERCISE2_MODIFIED)

    def test_exercise_modify_invalid(self):
        """Checks when a non-existing exercise is to be modified, the retun value is False"""
        print('(' + self.test_exercise_modify_invalid.__name__ + ')',
              self.test_exercise_modify_invalid.__doc__)

        self.assertFalse(self.connection.modify_exercise(200, "zvc", "fasd", "dsa", "Asd"))

    def test_exercise_create_valid(self):
        """Checks if an exercise can be created"""
        print('(' + self.test_exercise_create_valid.__name__ + ')',
              self.test_exercise_create_valid.__doc__)

        exercise = self.connection.create_exercise("New Exercise", "Description new", "Mystery", "new state", "new new")
        self.assertEqual(exercise, 4)
        self.assertDictContainsSubset(EXERCISE3_create, self.connection.get_exercise(4))


if __name__ == '__main__':
    print('Start running user tests')
    unittest.main()
