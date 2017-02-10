import sqlite3
import os

conn = sqlite3.connect(os.path.abspath('db.sqlite'))
cur = conn.cursor()

def get_regions():
    stmt = "SELECT * FROM regions"
    cur.execute(stmt)
    return cur.fetchall()

def get_locations(region_id):
    stmt = "SELECT cities.uid as uid, cities.cname as city " \
           "FROM cities JOIN regions ON cities.region_id = regions.uid WHERE region_id = ?"
    cur.execute(stmt, (region_id,))
    return cur.fetchall()

def save_comment(user_id, comment):
    # TODO:: Триггер на проверку уникальности пользователя.
    # Если пользователь с таким email существует, вернуть его id
    stmt = "INSERT INTO comments (text, user_id) VALUES (?, ?)"
    try:
        cur.execute(stmt, (comment, user_id))
        conn.commit()
        return cur.lastrowid
    except sqlite3.IntegrityError as e:
        print(e.args)
        BaseException("Error occured, while saving new comment")

def save_user(data):
    stmt = "INSERT INTO users (fname,lname,phone,email,city_id) VALUES (?, ?, ?, ?, ?)"
    try:
        cur.execute(stmt, (data['first_name'], data['last_name'],data['phone'],data['email'], data['city']))
        conn.commit()
        return cur.lastrowid
    except sqlite3.IntegrityError as e:
        print(e.args)
        raise BaseException("Error occured, while saving new user")

def get_comments():
    stmt = """
    SELECT
      comments.uid,
      comments.text as comment,
      users.fname,
      users.lname
    FROM comments JOIN users ON comments.user_id = users.uid"""
    cur.execute(stmt)
    return cur.fetchall()

def delete_comment(uid):
    stmt = "DELETE FROM comments WHERE uid=?"
    try:
        cur.execute(stmt, (uid,))
        conn.commit()
        return True
    except sqlite3.DatabaseError:
        pass

def get_region_stats():
    stmt = """
    SELECT * FROM (
      SELECT region, COUNT(region) as comments FROM (
        SELECT
          regions.rname AS region,
          cities.cname  AS city,
          comments.text AS comment,
          users.fname   AS user
        FROM comments
          JOIN users ON comments.user_id = users.uid
          JOIN cities ON users.city_id = cities.uid
          JOIN regions ON cities.region_id = regions.uid
      ) GROUP BY region
    ) WHERE comments > 1"""
    cur.execute(stmt)
    return cur.fetchall()

def get_city_stats():
    pass