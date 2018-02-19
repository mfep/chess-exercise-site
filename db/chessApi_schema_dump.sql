PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS users(
  user_id INTEGER PRIMARY KEY AUTOINCREMENT,
  nickname TEXT UNIQUE,
  reg_date INTEGER,
  email TEXT);
CREATE TABLE exercises(
  exercise_id INTEGER PRIMARY KEY,
  user_id INTEGER,
  title TEXT UNIQUE,
  description TEXT,
  sub_date INTEGER,
  initial_state TEXT,
  list_moves TEXT,
  FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE SET NULL);
COMMIT;
PRAGMA foreign_keys=ON;