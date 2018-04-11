Dependencies
------------

- sqlite3 : standard, executable provided
- unittest : standard
- [python-chess](https://github.com/niklasf/python-chess) : `pip install python-chess`

Populating the database
-----------------------

Python interpreter opened at project root:
```python
import chessApi.database as db
engine = db.Engine('db/myDatabase.db') # default database is 'db/chessApi.db'
engine.create_tables() # loads schema from 'db/chessApi_schema_dump.sql' by default
engine.populate_tables() # loads data dump from 'db/chessApi_data_dump.sql' by default
```

Running the REST API server
---------------------------

In this case, the default database path is used (`./db/chessApi.db`). In the project root folder:
- `python -m chessApi.resources`

Running the tests
-----------------
In the project root folder:

To run **all** tests (database + API)

- `python -m test.all_tests`

To run the database unit tests (database populated automatically)

- `python -m test.database_api_tests_exercise`
- `python -m test.database_api_tests_user`

To run API resource unit tests

- `python -m test.resource_api_tests`
