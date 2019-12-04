import csv
from polls.models import Restaurant_Reviews, Cuisine_Tags

with open('new_results.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        tag_string = row['categories']
        temp_list = tag_string.split(',')
        temp_models = []
        for tag in temp_list:
            c = Cuisine_Tags(tag_name=tag)
            temp_models.append(c)
        r = Restaurant_Reviews(restaurant_name=row['business_name'],location=row['address'],avg_rating=0.0,review_list=[],tag_list=temp_models,review_count=0,rating_sum=0.0)
        r.save()
