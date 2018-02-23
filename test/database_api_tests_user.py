'''
Created on 22.02.2018
@author: weiping

'''
import unittest, sqlite3
from chessApi import database

DB_PATH = 'db/chessApi_test.db'
ENGINE = database.Engine(DB_PATH)

#CONSTANTS DEFINING DIFFERENT USERS
USER1_NICKNAME = 'Mystery'
USER1_ID = 1
USER1 = {'registrationdate': 1362015937, 'nickname': USER1_NICKNAME, 'email': 'mystery@mymail.com'}

USER2_NICKNAME = 'AxelW'
USER2_ID = 2
USER2 = {'registrationdate': 1357724086, 'nickname': USER2_NICKNAME, 'email': 'axelw@mymail.com'}

NEW_USER_NICKNAME = 'sully'
NEW_USER = {'email': 'sully@rda.com'}
          
USER_WRONG_NICKNAME = 'Batty'
INITIAL_SIZE = 5


class UserDBAPITestCase(unittest.TestCase):
    '''
    Test cases for the Users related methods.
    '''
    #INITIATION AND TEARDOWN METHODS
    @classmethod
    def setUpClass(cls):
        ''' Creates the database structure. Removes first any preexisting
            database file
        '''
        print("Testing ", cls.__name__)
        ENGINE.remove_database()
        ENGINE.create_tables()

    @classmethod
    def tearDownClass(cls):
        '''Remove the testing database'''
        print("Testing ENDED for ", cls.__name__)
        ENGINE.remove_database()

    def setUp(self):
        '''
        Populates the database
        '''
        try:
          #This method load the initial values from forum_data_dump.sql
          ENGINE.populate_tables()
          #Creates a Connection instance to use the API
          self.connection = ENGINE.connect()
        except Exception as e: 
        #For instance if there is an error while populating the tables
          ENGINE.clear()


    def tearDown(self):
        '''
        Close underlying connection and remove all records from database
        '''
        self.connection.close()
        ENGINE.clear()

    def test_users_table_created(self):

        print('('+self.test_users_table_created.__name__+')', \
              self.test_users_table_created.__doc__)
        #Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query1 = 'SELECT * FROM users'
        #Connects to the database.
        con = self.connection.con
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)
            #Execute main SQL Statement
            cur.execute(query1)
            users = cur.fetchall()
            #Assert
            self.assertEqual(len(users), INITIAL_SIZE)


    def test_get_user(self):
        '''
        Test get_user with id Mystery and HockeyFan
        '''
        print('('+self.test_get_user.__name__+')', \
              self.test_get_user.__doc__)

        #Test with an existing user
        user = self.connection.get_user(USER1_NICKNAME)
        self.assertDictContainsSubset(user, USER1)
        user = self.connection.get_user(USER2_NICKNAME)
        self.assertDictContainsSubset(user, USER2)

    def test_get_user_noexistingid(self):
        '''
        Test get_user with  msg-200 (no-existing)
        '''
        print('('+self.test_get_user_noexistingid.__name__+')', \
              self.test_get_user_noexistingid.__doc__)

        #Test with an existing user
        user = self.connection.get_user(USER_WRONG_NICKNAME)
        self.assertIsNone(user)

    def test_get_users(self):
        '''
        Test that get_users work correctly and extract required user info
        '''
        print('('+self.test_get_users.__name__+')', \
              self.test_get_users.__doc__)
        users = self.connection.get_users()
        #Check that the size is correct
        self.assertEqual(len(users), INITIAL_SIZE)
        #Iterate throug users and check if the users with USER1_ID and
        #USER2_ID are correct:
        for user in users:
            if user['nickname'] == USER1_NICKNAME:
                self.assertDictContainsSubset(user, USER1)
            elif user['nickname'] == USER2_NICKNAME:
                self.assertDictContainsSubset(user, USER2)

    def test_delete_user(self):
        '''
        Test that the user Mystery is deleted
        '''
        print('('+self.test_delete_user.__name__+')', \
              self.test_delete_user.__doc__)
        resp = self.connection.delete_user(USER1_NICKNAME)
        self.assertTrue(resp)
        #Check that the users has been really deleted throug a get
        resp2 = self.connection.get_user(USER1_NICKNAME)
        self.assertIsNone(resp2)

    def test_delete_user_noexistingnickname(self):
        '''
        Test delete_user with  Batty (no-existing)
        '''
        print('('+self.test_delete_user_noexistingnickname.__name__+')', \
              self.test_delete_user_noexistingnickname.__doc__)
        #Test with an existing user
        resp = self.connection.delete_user(USER_WRONG_NICKNAME)
        self.assertFalse(resp)


    def test_append_user(self):
        '''
        Test that I can add new users
        '''
        print('('+self.test_append_user.__name__+')', \
              self.test_append_user.__doc__)
        nickname = self.connection.append_user(NEW_USER_NICKNAME, NEW_USER)
        self.assertIsNotNone(nickname)
        self.assertEqual(nickname, NEW_USER_NICKNAME)
        #Check that the messages has been really modified through a get
        resp2 = self.connection.get_user(nickname)
        self.assertDictContainsSubset(NEW_USER)
        self.assertDictContainsSubset(NEW_USER)

    def test_append_existing_user(self):
        '''
        Test that I cannot add two users with the same name
        '''
        print('('+self.test_append_existing_user.__name__+')', \
              self.test_append_existing_user.__doc__)
        nickname = self.connection.append_user(USER1_NICKNAME, NEW_USER)
        self.assertIsNone(nickname)


if __name__ == '__main__':
    print('Start running user tests')
    unittest.main()
