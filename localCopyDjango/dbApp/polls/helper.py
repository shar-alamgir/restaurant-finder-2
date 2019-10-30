import sqlite3
from sqlite3 import Error
from .models import User
import pdb

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

def insertRestaurant(conn, restaurant_name, location, price_tier, rating):
    sql = ''' INSERT INTO polls_restaurant(restaurant_name, location, price_tier, rating)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    task = (restaurant_name, location, price_tier, rating)
    cur.execute(sql, task)
    retValue = cur.lastrowid
    conn.commit()
    conn.close()
    return retValue

def deleteEntity(conn, table, id):
    sql = "DELETE FROM %s WHERE id = %d" % (table, id)
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    conn.close()
    return 0

def searchRestaurant(conn, searchString):
    sql = ''' SELECT id, restaurant_name
    FROM polls_restaurant
    WHERE restaurant_name LIKE ?
    ORDER BY restaurant_name ASC '''
    cur = conn.cursor()
    args = searchString + '%'
    cur.execute(sql, (args,))
    rows = cur.fetchall()
    conn.close()
    return rows

def updateUser(conn, user_id, user_name, location, favorite_restaurant):
    sql = 'UPDATE polls_user SET user_name = ?, location = ?, favorite_restaurant = ? WHERE id = ?'
    cur = conn.cursor()
    cur.execute(sql, (str(user_name), str(location), str(favorite_restaurant), int(user_id)),)
    conn.commit()
    conn.close()
    return user_id

def updateRestaurant(conn, restaurant_id, restaurant_name, location, price_tier):
    sql = 'UPDATE polls_restaurant SET restaurant_name = ?, location = ?, price_tier = ? WHERE id = ?'
    cur = conn.cursor()
    cur.execute(sql, (str(restaurant_name), str(location), str(price_tier), int(restaurant_id)),)
    conn.commit()
    conn.close()
    return restaurant_id

def getParameter(conn, param, table, id):
    sql = 'SELECT %s FROM %s WHERE id = %d' %(param, table, id)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()[0]
    return rows

def notValid(param, paramName):
    if paramName == 'price_tier':
        for currChar in param:
            if currChar != '$':
                return True
        return False
    if paramName == 'rating':
        count = 0
        tmp = str(param)
        for currChar in tmp:
            if currChar != '.' and (currChar < '0' or currChar > '9'):
                return True
            if currChar == '.':
                count += 1
        if count > 1:
            return True
        return param > 5
