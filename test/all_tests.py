"""
Created on 24.02.2018
Provides functionality to run all tests at once.
@author: lorinc

"""

import unittest

from test.database_api_tests_user import UserDbApiTestCase
from test.database_api_tests_exercise import ExerciseApiDbTestCase

if __name__ == '__main__':
    suite = unittest.TestSuite((
        unittest.defaultTestLoader.loadTestsFromTestCase(UserDbApiTestCase),
        unittest.defaultTestLoader.loadTestsFromTestCase(ExerciseApiDbTestCase)
    ))
    unittest.main()
