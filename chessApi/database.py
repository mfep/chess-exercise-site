# Created on 19.02.2018
# Provides the database API to access the forum persistent data.
# @author: lorinc

import sqlite3
import os

DEFAULT_DB_PATH = 'db/forum.db'
DEFAULT_SCHEMA = "db/forum_schema_dump.sql"
DEFAULT_DATA_DUMP = "db/forum_data_dump.sql"


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
        at *db/forum.db*

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
    #     return Connection(self.db_path)

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
            None, then *db/forum_schema_dump.sql* is utilized.

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
        """
        Create the table ``users`` programmatically, without using .sql file.

        Print an error message in the console if it could not be created.

        :return: ``True`` if the table was successfully created or ``False``
            otherwise.

        """
        keys_on = 'PRAGMA foreign_keys = ON'
        stmnt = 'CREATE TABLE users(' \
                'user_id INTEGER PRIMARY KEY,' \
                'nickname TEXT UNIQUE,' \
                'reg_date INTEGER,' \
                'email TEXT)'
        con = sqlite3.connect(self.db_path)
        with con:
            cur = con.cursor()
            try:
                cur.execute(keys_on)
                cur.execute(stmnt)
            except sqlite3.Error as excp:
                print("Error %s:" % excp.args[0])
                return False
        return True

    def create_exercises_table(self):
        """
        Create the table ``exercises`` programmatically, without using .sql file.

        Print an error message in the console if it could not be created.

        :return: ``True`` if the table was successfully created or ``False``
            otherwise.

        """
        keys_on = 'PRAGMA foreign_keys = ON'
        stmnt = 'CREATE TABLE exercises(' \
                'exercise_id INTEGER PRIMARY KEY,' \
                'user_id INTEGER,' \
                'title TEXT UNIQUE,' \
                'description TEXT,' \
                'sub_date INTEGER,' \
                'initial_state TEXT,' \
                'list_moves TEXT,' \
                'FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE SET NULL )'
        con = sqlite3.connect(self.db_path)
        with con:
            cur = con.cursor()
            try:
                cur.execute(keys_on)
                cur.execute(stmnt)
            except sqlite3.Error as excp:
                print("Error %s:" % excp.args[0])
                return False
        return True
