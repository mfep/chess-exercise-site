"""
Created on 19.02.2018
Provides the database API to access the forum persistent data.
@author: lorinc

"""

import sqlite3
import os
import re

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


    def create_users_table(self):
        '''
        Create the table ``users`` programmatically, without using .sql file.

        Print an error message in the console if it could not be created.

        :return: ``True`` if the table was successfully created or ``False``
            otherwise.

        '''
        keys_on = 'PRAGMA foreign_keys = ON'
        stmnt = 'CREATE TABLE users(user_id INTEGER PRIMARY KEY,\
                                    nickname TEXT UNIQUE, regDate INTEGER,\
                                    email TEXT,\
                                    UNIQUE(user_id, nickname))'
        #Connects to the database. Gets a connection object
        con = sqlite3.connect(self.db_path)
        with con:
            #Get the cursor object.
            #It allows to execute SQL code and traverse the result set
            cur = con.cursor()
            try:
                cur.execute(keys_on)
                #execute the statement
                cur.execute(stmnt)
            except sqlite3.Error as excp:
                print("Error %s:" % excp.args[0])
                return False
        return True


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

    def get_exercise(self, exercise_id):
        """
        Extracts exercise from database.

        :param exercise_id: The identifier number of the message.
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

    def exercise_modify(self, exerciseid, title, description, initial_state, list_moves):
        """
        Modify the title, the description and the editor of the message with id
        ``exerciseid``
        :param str exerciseid: The id of the message to remove. Note that
            messageid is a string with format msg-\d{1,3}
        :param str title: the exercise's title
        :param str description: the exercise's description
        :param str initial_state: The initial state of the pieces on the chess board.
        :param str list_moves: The right list of moves.
        :return: the id of the edited exercise or None if the exercise was
              not found.
        :raises ValueError: if the exerciseid has a wrong format.

                 """
        match = re.match(r'msg-(\d{1,3})', exerciseid)
        if match is None:
            raise ValueError("The exerciseid is malformed")
        exerciseid = int(match.group(1))
        stmnt='UPDATE exercises SET , title=:title , description=:description, initial_state=:initial_state,\
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
            if cur.row_count < 1:
                return None
        return 'msg-%s' %exerciseid

    def exercise_create(self, title, description, creator, initial_state, list_moves):
        """
        :param str title: the exercises's title
        :param str description: the exercises's description
        :param initial_state: The initial state of chess pieces on the board.
        :param list_moves: The right moves which complete the exercise correctly.
        :param creator: the username of the person that created the exercise.
        :return: the id of the created exercise or None if the message was not
            found.
         """
        # SQL Statement for getting the user id
        query1 = 'SELECT user_id from users WHERE nickname = ?'

        # SQL Statement for inserting the data
        stmnt = 'INSERT INTO exercises (user_id,title,description,sub_date,initial_state, \
                                   list_moves) \
                                   VALUES(?,?,?,?,?,?,?,?)'
        user_id = None
        timestamp = sqlite3.time.mktime(sqlite3.datetime.now().timetuple())

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
        pvalue(user_id, title, description, timestamp, initial_state, list_moves)
        # Execute the statement
        cur.execute(stmnt, pvalue)
        self.con.commit()

        # Extract the id of the added message
        lid = cur.lastrowid
        # Return the id in
        return 'msg-' + str(lid) if lid is not None else None
     #ACCESSING THE USER table
    def get_users(self):
        '''
        Extracts all users in the database.

        :return: list of Users of the database. Each user is a dictionary
            that contains two keys: ``nickname``(str) and ``registrationdate``
            (long representing UNIX timestamp). None is returned if the database
            has no users.

        '''
        #Create the SQL Statements
          #SQL Statement for retrieving the users
        query = 'SELECT users.* FROM users'
        #Activate foreign key support
        self.set_foreign_keys_support()
        #Create the cursor
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Execute main SQL Statement
        cur.execute(query)
        #Process the results
        rows = cur.fetchall()
        if rows is None:
            return None
        #Process the response.
        users = []
        for row in rows:
            users.append(self._create_user_list_object(row))
        return users


    def get_user(self, nickname):
        '''
        Extracts all the information of a user.

        :param str nickname: The nickname of the user to search for.
        :return: dictionary with the format provided in the method:
            :py:meth:`_create_user_object`

        '''
        #Create the SQL Statements
          #SQL Statement for retrieving the user given a nickname
        query1 = 'SELECT user_id from users WHERE nickname = ?'
          #SQL Statement for retrieving the user information
        query2 = 'SELECT users.* FROM users\
                  WHERE users.user_id = ? '
          #Variable to be used in the second query.
        user_id = None
        #Activate foreign key support
        self.set_foreign_keys_support()
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Execute SQL Statement to retrieve the id given a nickname
        pvalue = (nickname,)
        cur.execute(query1, pvalue)
        #Extract the user id
        row = cur.fetchone()
        if row is None:
            return None
        user_id = row["user_id"]
        # Execute the SQL Statement to retrieve the user invformation.
        # Create first the valuse
        pvalue = (user_id, )
        #execute the statement
        cur.execute(query2, pvalue)
        #Process the response. Only one posible row is expected.
        row = cur.fetchone()
        return self._create_user_object(row)


    def delete_user(self, nickname):
        '''
        Remove all user information of the user with the nickname passed in as
        argument.

        :param str nickname: The nickname of the user to remove.

        :return: True if the user is deleted, False otherwise.

        '''
        #Create the SQL Statements
          #SQL Statement for deleting the user information
        query = 'DELETE FROM users WHERE nickname = ?'
        #Activate foreign key support
        self.set_foreign_keys_support()
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Execute the statement to delete
        pvalue = (nickname,)
        cur.execute(query, pvalue)
        self.con.commit()
        #Check that it has been deleted
        if cur.rowcount < 1:
            return False
        return True