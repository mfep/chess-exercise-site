Dependencies
------------

- sqlite3 : standard, executable provided
- unittest : standard

Populating the database
-----------------------

Python interpreter opened at project root:
```python
import chessApi.database as db
engine = db.Engine('db/myDatabase.db') # default database is 'db/chessApi.db'
engine.create_tables() # loads schema from 'db/chessApi_schema_dump.sql' by default
engine.populate_tables() # loads data dump from 'db/chessApi_data_dump.sql' by default
```

Running the tests
-----------------
In the project root folder:

To run the database unit tests (database populated automatically)

- `python -m test.database_api_tests_exercise`
- `python -m test.database_api_tests_user`