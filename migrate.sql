-- CREATE TABLES --
CREATE TABLE IF NOT EXISTS users (uid INTEGER PRIMARY KEY AUTOINCREMENT,
  fname VARCHAR(80) NOT NULL , lname VARCHAR(80) NOT NULL , phone INT, email VARCHAR(80), city_id INT NOT NULL,
  FOREIGN KEY (city_id) REFERENCES cities(uid));

CREATE TABLE IF NOT EXISTS regions (uid INTEGER PRIMARY KEY AUTOINCREMENT,
  rname VARCHAR(80) NOT NULL );

CREATE TABLE IF NOT EXISTS cities (uid INTEGER PRIMARY KEY AUTOINCREMENT,
  cname VARCHAR(80), region_id INT NOT NULL, FOREIGN KEY (region_id) REFERENCES regions(uid));

CREATE TABLE IF NOT EXISTS comments (uid INTEGER PRIMARY KEY AUTOINCREMENT,
  text TEXT NOT NULL , user_id INT NOT NULL , FOREIGN KEY (user_id) REFERENCES users(uid));

-- SEED TABLES --
