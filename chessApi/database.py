"""
Created on 19.02.2018
Provides the database API to access the forum persistent data.
@author: lorinc

"""

from datetime import datetime
import sqlite3
import os
import time

DEFAULT_DB_PATH = 'db/chessApi.db'
DEFAULT_SCHEMA = "db/chessApi_schema_dump.sql"
DEFAULT_DATA_DUMP = "db/chessApi_data_dump.sql"


class Engine(object):
    """
    Abstraction of the database.

    It includes tools to create, configure,
    populate and connect to the sqlite file. You can access the Connection
    instance, and hence, to the database interface itself using the method
    :py:meth:`connection`.

    :Example:

    >>> engine = Engine()
    >>> con = engine.connect()

    :param db_path: The path of the database file (always with respect to the
        calling script. If not specified, the Engine will use the file located
        at *db/chessApi.db*

    """

    def __init__(self, db_path=None):
        super(Engine, self).__init__()
        if db_path is not None:
            self.db_path = db_path
        else:
            self.db_path = DEFAULT_DB_PATH

    def connect(self):
        """
        Creates a connection to the database.

        :return: A Connection instance
        :rtype: Connection

        """
        return Connection(self.db_path)

    def remove_database(self):
        """
        Removes the database file from the filesystem.

        """
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def clear(self):
        """
        Purge the database removing all records from the tables. However,
        it keeps the database schema (meaning the table structure)

        """
        keys_on = 'PRAGMA foreign_keys = ON'
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        cur.execute(keys_on)
        with con:
            cur = con.cursor()
            cur.execute("DELETE FROM exercises")
            cur.execute("DELETE FROM users")

    def create_tables(self, schema=None):
        """
        Create programmatically the tables from a schema file.

        :param schema: path to the .sql schema file. If this parmeter is
            None, then *db/chessApi_schema_dump.sql* is utilized.

        """
        con = sqlite3.connect(self.db_path)
        if schema is None:
            schema = DEFAULT_SCHEMA
        try:
            with open(schema, encoding="utf-8") as f:
                sql = f.read()
                cur = con.cursor()
                cur.executescript(sql)
        finally:
            con.close()

    def populate_tables(self, dump=None):
        """
        Populate programmatically the tables from a dump file.

        :param dump:  path to the .sql dump file. If this parmeter is
            None, then *db/forum_data_dump.sql* is utilized.

        """
        keys_on = 'PRAGMA foreign_keys = ON'
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        cur.execute(keys_on)
        if dump is None:
            dump = DEFAULT_DATA_DUMP
        with open(dump, encoding="utf-8") as f:
            sql = f.read()
            cur = con.cursor()
            cur.executescript(sql)


class Connection(object):
    """
    API to access the chessApi database.

    The sqlite3 connection instance is accessible to all the methods of this
    class through the :py:attr:`self.con` attribute.

    An instance of this class should not be instantiated directly using the
    constructor. Instead use the :py:meth:`Engine.connect`.

    Use the method :py:meth:`close` in order to close a connection.
    A :py:class:`Connection` **MUST** always be closed once when it is not going to be
    utilized anymore in order to release internal locks.

    :param db_path: Location of the database file.
    :type db_path: str

    """

    def __init__(self, db_path):
        super(Connection, self).__init__()
        self.con = sqlite3.connect(db_path)
        self._isclosed = False

    def isclosed(self):
        """
        :return: ``True`` if connection has already being closed.

        """
        return self._isclosed

    def close(self):
        """
        Closes the database connection, commiting all changes.

        """
        if self.con and not self._isclosed:
            self.con.commit()
            self.con.close()
            self._isclosed = True

    def set_foreign_keys_support(self):
        """
        Activate the support for foreign keys.

        :return: ``True`` if operation succeed and ``False`` otherwise.

        """
        keys_on = 'PRAGMA foreign_keys = ON'
        try:
            cur = self.con.cursor()
            cur.execute(keys_on)
            return True
        except sqlite3.Error as excp:
            print("Error %s:" % excp.args[0])
            return False

    def _create_user_object(self, row):
        """
        It takes a database Row and transform it into a python dictionary.

        :param row: The row obtained from the database.
        :type row: sqlite3.Row
        :return: a dictionary with the following format:
            where:

            * ``registrationdate``: UNIX timestamp when the user registered in
                                 the system (long integer)
            * ``nickname``: nickname of the user
            * ``email``: current email of the user.

        """
        return {'registrationdate': (row['reg_date']), 'nickname': row['nickname'], 'email': row['email']}

    def _create_user_list_object(self, row):
        """
        :param row: The row obtained from the database.
        :type row: sqlite3.Row
        :return: a dictionary with the keys ``registrationdate`` and
            ``nickname``

        """
        return {'registrationdate': row['reg_date'], 'nickname': row['nickname']}

    def get_exercise(self, exercise_id):
        """
        Extracts exercise from database.

        :param exercise_id: The identifier number of the exercise.
        :return: A dictionary with the exercise data,
            or None if no exercise with that id exists.

        """
        # fetch row
        self.set_foreign_keys_support()
        query = 'SELECT * FROM exercises WHERE exercise_id = ?'
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        pvalue = (exercise_id,)
        cur.execute(query, pvalue)
        row = cur.fetchone()

        # row to dictionary
        return None if not row else {
            'exercise_id': row['exercise_id'],
            'user_id': row['user_id'],
            'title': row['title'],
            'description': row['description'],
            'sub_date': row['sub_date'],
            'initial_state': row['initial_state'],
            'list_moves': row['list_moves']
        }

    def delete_exercise(self, exercise_id):
        """
        Deletes the exercise with the given id.

        :param exercise_id: The id of the exercise to be deleted.
        :return: True if the exercise has been deleted successfully, False otherwise.

        """
        self.set_foreign_keys_support()
        query = 'DELETE FROM exercises WHERE exercise_id = ?'
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        pvalue = (exercise_id,)
        try:
            cur.execute(query, pvalue)
            self.con.commit()
        except sqlite3.Error as e:
            print("Error %s:" % (e.args[0]))
        return bool(cur.rowcount)

    def modify_exercise(self, exerciseid, title, description, initial_state, list_moves):
        """
        Modify the title, the description the initial state of the message with given id.
        ``exerciseid``
        :param int exerciseid: The id of the exercise to modify.
        :param str title: the exercise's new title
        :param str description: the exercise's new description
        :param str initial_state: The initial state of the pieces on the chess board (new).
        :param str list_moves: The right list of moves (new).
        :return: the id of the edited exercise or None if the exercise was not found.
        """
        stmnt = 'UPDATE exercises SET title=:title , description=:description, initial_state=:initial_state,\
         list_moves=:list_moves  WHERE exercise_id=:exercise_id'

        self.set_foreign_keys_support()
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()

        pvalue = {"exercise_id": exerciseid,
                  "title": title,
                  "description": description,
                  "initial_state": initial_state,
                  "list_moves": list_moves}

        try:
            cur.execute(stmnt, pvalue)
            self.con.commit()
        except sqlite3.Error as e:
            print("Error %s:" % (e.args[0]))
        else:
            if cur.rowcount < 1:
                return None
        return exerciseid

    def create_exercise(self, title, description, creator, initial_state, list_moves):
        """
        :param str title: the exercises's title
        :param str description: the exercises's description
        :param str initial_state: The initial state of chess pieces on the board.
        :param str list_moves: The right moves which complete the exercise correctly.
        :param str creator: the username of the person that created the exercise.
        :return: the id of the created exercise or None if the message was not found.
        """
        # SQL Statement for getting the user id
        query1 = 'SELECT user_id from users WHERE nickname = ?'

        # SQL Statement for inserting the data
        stmnt = 'INSERT INTO exercises (user_id,title,description,sub_date,initial_state, list_moves) \
                                   VALUES(?,?,?,?,?,?)'
        user_id = None
        timestamp = time.mktime(datetime.now().timetuple())

        # fetch row
        self.set_foreign_keys_support()
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        pvalue = (creator,)
        cur.execute(query1, pvalue)
        # Extract user id
        row = cur.fetchone()
        if row is not None:
            user_id = row["user_id"]
        # Generate the values for SQL statement
        pvalue = (user_id, title, description, timestamp, initial_state, list_moves)
        # Execute the statement
        cur.execute(stmnt, pvalue)
        self.con.commit()

        # Return the id in
        return cur.lastrowid

    def get_users(self):
        """
        Extracts all users in the database.

        :return: list of Users of the database. Each user is a dictionary
            that contains two keys: ``nickname``(str) and ``registrationdate``
            (long representing UNIX timestamp). None is returned if the database
            has no users.

        """
        # Create the SQL Statements
        # SQL Statement for retrieving the users
        query = 'SELECT users.* FROM users'
        # Activate foreign key support
        self.set_foreign_keys_support()
        # Create the cursor
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        # Execute main SQL Statement
        cur.execute(query)
        # Process the results
        rows = cur.fetchall()
        if rows is None:
            return None
        # Process the response.
        users = []
        for row in rows:
            users.append(self._create_user_list_object(row))
        return users

    def get_user(self, nickname):
        """
        Extracts all the information of a user.

        :param str nickname: The nickname of the user to search for.
        :return: dictionary with the format provided in the method:
            :py:meth:`_create_user_object`

        """
        # Create the SQL Statements
        # SQL Statement for retrieving the user given a nickname
        query1 = 'SELECT user_id from users WHERE nickname = ?'
        # SQL Statement for retrieving the user information
        query2 = 'SELECT users.* FROM users\
                  WHERE users.user_id = ? '
        # Variable to be used in the second query.
        # Activate foreign key support
        self.set_foreign_keys_support()
        # Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        # Execute SQL Statement to retrieve the id given a nickname
        pvalue = (nickname,)
        cur.execute(query1, pvalue)
        # Extract the user id
        row = cur.fetchone()
        if row is None:
            return None
        user_id = row['user_id']
        # Execute the SQL Statement to retrieve the user invformation.
        # Create first the valuse
        pvalue = (user_id,)
        # execute the statement
        cur.execute(query2, pvalue)
        # Process the response. Only one posible row is expected.
        row = cur.fetchone()
        return self._create_user_object(row)

    def delete_user(self, nickname):
        """
        Remove all user information of the user with the nickname passed in as
        argument.

        :param str nickname: The nickname of the user to remove.

        :return: True if the user is deleted, False otherwise.

        """
        # Create the SQL Statements
        # SQL Statement for deleting the user information
        query = 'DELETE FROM users WHERE nickname = ?'
        # Activate foreign key support
        self.set_foreign_keys_support()
        # Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        # Execute the statement to delete
        pvalue = (nickname,)
        cur.execute(query, pvalue)
        self.con.commit()
        # Check that it has been deleted
        if cur.rowcount < 1:
            return False
        return True

    def append_user(self, nickname, email):
        """
        Create a new user in the database.

        :param str nickname: The nickname of the new user
        :param str email: The email address of the new user

        :return: the nickname of the created user or None if the user could not been added to the database.

        """
        # Create the SQL Statements
        # SQL Statement for extracting the userid given a nickname
        query1 = 'SELECT user_id FROM users WHERE nickname = ?'
        # SQL Statement to create the row in  users table
        query2 = 'INSERT INTO users(nickname,reg_date,email)\
                  VALUES(?,?,?)'
        # temporal variables for user table
        # timestamp will be used for reg_date.
        timestamp = int(time.time())

        # Activate foreign key support
        self.set_foreign_keys_support()
        # Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        # Execute the main SQL statement to extract the id associated to a nickname
        pvalue = (nickname,)
        cur.execute(query1, pvalue)
        # No value expected (no other user with that nickname expected)
        row = cur.fetchone()
        # If there is no user add rows in user
        if row is None:
            # Add the row in users table
            # Execute the statement
            pvalue = (nickname, timestamp, email)
            cur.execute(query2, pvalue)
            # Extrat the rowid => user-id

            self.con.commit()

            return nickname

        else:
            return None
