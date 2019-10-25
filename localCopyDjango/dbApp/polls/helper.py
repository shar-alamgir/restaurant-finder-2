import sqlite3
from sqlite3 import Error
from .models import User

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def insertUser(conn, user_name, date_created, location, favorite_restaurant):
    sql = ''' INSERT INTO polls_user(user_name, date_created, location, favorite_restaurant)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    task = (user_name, date_created, location, favorite_restaurant)
    cur.execute(sql, task)
    retValue = cur.lastrowid
    conn.commit()
    conn.close()
    return retValue
