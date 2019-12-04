import sqlite3
import googlemaps
import pymongo
from pymongo import MongoClient
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

def insertRestaurant(conn, restaurant_name, location, price_tier, rating, tagString):
    sql = ''' INSERT INTO polls_restaurant(restaurant_name, location, price_tier, rating)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    task = (restaurant_name, location, price_tier, rating)
    cur.execute(sql, task)
    retValue = cur.lastrowid
    conn.commit()
    conn.close()

    tagList = tagString.split(' ')
    conn = MongoClient('localhost',27017)
    database = 'User_Reviews'
    db = conn[database]
    collection = db['polls_restaurant_reviews']
    collection.insert_one({"restuarant_name":restuarant_name, "location":location, "avg_rating":0, "review_list":[], "tag_list":tagList, "review_count":0, "rating_sum":0})
    conn.close()
    return retValue

# def insertReview(conn, review, name, title, rating, id):
#     sql = ''' INSERT INTO polls_restaurant_reviews() '''


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
        return float(param) > 5.0

def getDistance(userAddr, restAddr):
    gmaps = googlemaps.Client(key='AIzaSyDeOyuHKTRGZr3YzOirYe5Wi1v5IN2ZhE4')
    restObj = gmaps.geocode(restAddr)
    userObj = gmaps.geocode(userAddr)
    restaurantLat = restObj[0]['geometry']['location']['lat']
    restaurantLng = restObj[0]['geometry']['location']['lng']
    userLat = userObj[0]['geometry']['location']['lat']
    userLng = userObj[0]['geometry']['location']['lng']
    travelDistObj = gmaps.distance_matrix((userLat, userLng), (restaurantLat, restaurantLng))
    dist = travelDistObj['rows'][0]['elements'][0]['distance']['text']
    spaceIndex = dist.find(' ')
    dist = dist[0:spaceIndex]
    return dist

#recommendation helper

def recommendRestaurant(conn, cuisines, price, rating, location, extra):
    flag = False
    #perform nosql query to get list of all restaurant_name (s) that have at least one of the cuisine tag
    if cuisines is None:
        sql = 'SELECT id, restaurant_name, location FROM polls_restaurant WHERE'
    else:
        client = MongoClient('localhost',27017)
        database = 'User_Reviews'
        db = client[database]
        collection = db['polls_restaurant_reviews']
        aggList = collection.find({"tag_list.tag_name": {"$in" : cuisines}}, {"id" : 1, "_id": 0})
        idList = []
        for id in aggList:
            idList.append(id["id"])

        idString = "("
        for id in range (len(idList)):
            if (id == len(idList) - 1):
                idString += str(idList[id]) + ")"
            else :
                idString += str(idList[id]) + ", "
        flag = True
        sql = 'SELECT id, restaurant_name, location FROM polls_restaurant WHERE id IN' + idString

    if price is None:
        sql = sql
    else:
        numDollars = len(price)
        neededUnderscores = numDollars - 1
        underscores = "_" * neededUnderscores
        priceString = "$" + underscores
        newPriceString = "'" + priceString + "'"
        if flag is True:
            sql = sql + ' AND price_tier LIKE ' + newPriceString
        else:
            flag = True
            sql = sql + ' price_tier LIKE ' + newPriceString
    if rating is None:
        sql = sql
    else:
        if flag is True:
            sql = sql + ' AND rating >= ' + rating
        else:
            flag = True
            sql = sql + ' rating >= ' + rating

    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()

    dropStatement = 'DROP TABLE IF EXISTS temp'
    if location is None:
        conn.close()
        return rows
    else:
        cur.execute(dropStatement)
        conn.commit()
        newSql = "CREATE TABLE temp (id INTEGER, restaurant_name VARCHAR(30), location VARCHAR(30), distanceToUser float)"
        cur.execute(newSql)
        conn.commit()
        for currRow in rows:
            currDist = float(getDistance(location, currRow[2]))
            alterSql = 'INSERT INTO temp (id, restaurant_name, location, distanceToUser) VALUES (?, ?, ?, ?)'
            task = (currRow[0], currRow[1], currRow[2], currDist)
            cur.execute(alterSql, task)
            conn.commit()
    selectRecs = 'SELECT * FROM temp ORDER BY distanceToUser ASC'
    cur.execute(selectRecs)
    recs = cur.fetchall()

    cur.execute(dropStatement)
    conn.commit()
    conn.close()
    return recs
