import sqlite3
import os

conn = sqlite3.connect(os.path.abspath('db.sqlite'))
cur = conn.cursor()

def get_regions():
    stmt = "Select * from regions"
    cur.execute(stmt)
    return cur.fetchall()

def get_locations(region_id):
    stmt = "SELECT cities.uid as uid, cities.cname as city " \
           "FROM cities JOIN regions ON cities.region_id = regions.uid WHERE region_id = ?"
    cur.execute(stmt, (region_id,))
    return cur.fetchall()

def save_comment(data):
    pass

def save_user(data):
    pass