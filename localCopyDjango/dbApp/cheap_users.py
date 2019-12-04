from polls.models import User, Restaurant
from polls import helper

database = r"\Users\Marcus Cooney\Desktop\CS411\rf2\localCopyDjango\dbApp\db.sqlite3"

conn = helper.create_connection(database)
if conn is None:
    print("no conn established")

sql = '''SELECT r.price_tier, COUNT(DISTINCT u.user_name) AS TotalUsers
    FROM polls_user u JOIN polls_restaurant r ON u.favorite_restaurant = r.restaurant_name
    GROUP BY r.price_tier'''

cur = conn.cursor()
cur.execute(sql,)
rows = cur.fetchall()
print(rows)

conn.close()
