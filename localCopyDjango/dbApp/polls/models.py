import datetime
from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class User(models.Model):
    def __str__(self):
        return self.user_name
    user_name = models.CharField(max_length=50, primary_key=True, unique=True)
    date_created = models.DateTimeField('date created')
    location = models.CharField(max_length=50)
    favorite_restaurant = models.CharField(max_length=50)

class Restaurant(models.Model):
    def __str__(self):
        return self.restaurant_name
    restaurant_name = models.CharField(max_length=50, primary_key=True)
    location = models.CharField(max_length=50)
    # only one primary key in sqlite
    price_tier = models.CharField(max_length=4)
    rating = models.IntegerField(default=0)
    # hours is a separate table
    # cuisine tags, reviews is NoSQL
class Menu(models.Model):
    def __str__(self):
        return self.restaurant_name
    restuarant_name = models.ForeignKey('Restaurant', on_delete=models.CASCADE)
    food_type = models.CharField(max_length=20)
    dietary_restrictions = models.CharField(max_length=50)
    price = models.IntegerField(default=0,
        validators=[MaxValueValidator(1), MinValueValidator(10)])

class Hours(models.Model):
    def __str__(self):
        return self.restuarant_name
    restuarant_name = models.ForeignKey('Restaurant', on_delete=models.CASCADE)
    m_open = models.CharField(max_length=8)
    m_close = models.CharField(max_length=8)
    t_open = models.CharField(max_length=8)
    t_close = models.CharField(max_length=8)
    w_open = models.CharField(max_length=8)
    w_close = models.CharField(max_length=8)
    th_open = models.CharField(max_length=8)
    th_close = models.CharField(max_length=8)
    f_open = models.CharField(max_length=8)
    f_close = models.CharField(max_length=8)
    sa_open = models.CharField(max_length=8)
    sa_close = models.CharField(max_length=8)
    su_open = models.CharField(max_length=8)
    su_close = models.CharField(max_length=8)
