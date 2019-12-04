from polls.models import User, Restaurant
from polls import helper

database = r"\Users\Marcus Cooney\Desktop\CS411\rf2\localCopyDjango\dbApp\db.sqlite3"

conn = helper.create_connection(database)
if conn is None:
    print("no conn established")

user_rating = 1
user_price = '$$$'

sql = '''SELECT restaurant_name, price_tier, AVG(r1.rating)
FROM polls_user u1 JOIN polls_restaurant r1 ON u1.favorite_restaurant = r1.restaurant_name
GROUP BY r1.restaurant_name, r1.price_tier
HAVING AVG(r1.rating) > ?
INTERSECT
SELECT restaurant_name, price_tier, AVG(r2.rating) AS AvgRating
FROM polls_user u2 JOIN polls_restaurant r2 ON u2.favorite_restaurant = r2.restaurant_name
WHERE r2.price_tier NOT LIKE ? + "%"
GROUP BY r2.restaurant_name, r2.price_tier'''

cur = conn.cursor()
cur.execute(sql, (user_rating, user_price))
rows = cur.fetchall()
print(rows)

conn.close()
