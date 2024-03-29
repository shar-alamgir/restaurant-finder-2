from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.template import loader
from django.shortcuts import render, get_object_or_404
from .models import User, Restaurant, Menu, Hours, Reviews, Restaurant_Reviews
from django.utils import timezone
from datetime import date
import datetime
import cgi
from . import helper
import pdb
import pymongo
from pymongo import MongoClient
import pprint

database = r"\Users\Shar\djangoInstall\rf2\localCopyDjango\dbApp\db.sqlite3"

def homeView(request):
    return render(request, 'polls/homeView.html')

def searchView(request):
    conn = MongoClient('localhost', 27017)
    db = conn["User_Reviews"]
    col = db['polls_restaurant_reviews']
    tags = col.find({}, {"tag_list.tag_name"}).distinct("tag_list.tag_name")
    real_list = []
    for i in tags:
        real_list.append(i)
    real_list.sort()
    context = {"tags" : real_list}
    conn.close()
    return render(request, 'polls/searchView.html', context)

def searchResultsView(request):
    if request.method == 'POST':
        if request.POST.get('restaurant'):
            conn = helper.create_connection(database)
            if conn is None:
                return redirect('searchView')
            searchString = request.POST.get('restaurant').strip()
            result = helper.searchRestaurant(conn, searchString)
            context = {'result' : result}
            return render(request, 'polls/searchResultsView.html', context)
        else: #restaurant recommendation AF1
            conn = helper.create_connection(database)
            if conn is None:
                return redirect('searchView')
            #select all cuisines as one list
            cuisines = request.POST.getlist('cuisines')
            price = request.POST.get('price')
            rating = request.POST.get('rating')
            #only read the location if they checked the box
            if request.POST.get('locationCheck'):
                location = request.POST.get('location')
            else:
                location = None

            #not sure if i can call this once for the entire cuisine list or if i should iterate through the list
            result, checkedRestaurant = helper.recommendRestaurant(conn, cuisines, price, rating, location)
            context = {'afresult' : result, "checkedOrNot": checkedRestaurant}
            return render(request, 'polls/searchResultsView.html', context)

            #return this for now until function works
            # return redirect('searchView')
    return redirect('searchView')

def userView(request, user_id):

    # if request.method == 'POST':
    #     database = r"/Users/vincentnguyen/rf2/localCopyDjango/dbApp/db.sqlite3"
    #     conn = helper.create_connection(database)
    #     if conn is None:
    #         return 0
    #     if request.POST.get('update'):
    #         if request.POST.get('user_name') != '':
    #             user_name = request.POST.get('user_name')
    #         else :
    #             user_name = helper.getParameter(conn, 'user_name', 'polls_user', user_id)[0]
    #
    #         if request.POST.get('location') != '':
    #             location = request.POST.get('location')
    #         else :
    #             location = helper.getParameter(conn, 'location', 'polls_user', user_id)[0]
    #         if request.POST.get('favorite_restaurant') != '':
    #             favorite_restaurant = request.POST.get('favorite_restaurant')
    #         else :
    #             favorite_restaurant = helper.getParameter(conn, 'favorite_restaurant', 'polls_user', user_id)[0]
    #         helper.updateUser(conn, user_id, user_name, location, favorite_restaurant)
    #         user = get_object_or_404(User, pk=user_id)
    #         return render(request, 'polls/userView.html', {'user' : user})
    #     helper.deleteEntity(conn, 'polls_user', user_id)
    #     return redirect('allUsersView')
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'polls/userView.html', {'user' : user})

def personalUserView(request, user_id):
    if request.method == 'POST':
        conn = helper.create_connection(database)
        if conn is None:
            return 0
        if request.POST.get('update'):
            if request.POST.get('user_name') != '':
                user_name = request.POST.get('user_name')
            else :
                user_name = helper.getParameter(conn, 'user_name', 'polls_user', user_id)[0]

            if request.POST.get('location') != '':
                location = request.POST.get('location')
            else :
                location = helper.getParameter(conn, 'location', 'polls_user', user_id)[0]
            if request.POST.get('favorite_restaurant') != '':
                favorite_restaurant = request.POST.get('favorite_restaurant')
            else :
                favorite_restaurant = helper.getParameter(conn, 'favorite_restaurant', 'polls_user', user_id)[0]
            helper.updateUser(conn, user_id, user_name, location, favorite_restaurant)
            user = get_object_or_404(User, pk=user_id)
            return render(request, 'polls/personalUserView.html', {'user' : user})
        helper.deleteEntity(conn, 'polls_user', user_id)
        return redirect('allUsersView')
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'polls/personalUserView.html', {'user' : user})

def allUsersView(request):
    allUsers = User.objects.all()
    context = {'allUsers' : allUsers}
    return render(request, 'polls/allUsersView.html', context)

def restaurantView(request, restaurant_id):
    if request.method == "POST":
        conn = helper.create_connection(database)
        if conn is None:
            return 0
        if request.POST.get('update'):
            if request.POST.get('restaurant_name') != '':
                restaurant_name = request.POST.get('restaurant_name')
            else :
                restaurant_name = helper.getParameter(conn, 'restaurant_name', 'polls_restaurant', restaurant_id)[0]

            if request.POST.get('location') != '':
                location = request.POST.get('location')
            else :
                location = helper.getParameter(conn, 'location', 'polls_restaurant', restaurant_id)[0]
            if request.POST.get('price_tier') != '':
                price_tier = request.POST.get('price_tier')
            else :
                price_tier = helper.getParameter(conn, 'price_tier', 'polls_restaurant', restaurant_id)[0]
            helper.updateRestaurant(conn, restaurant_id, restaurant_name, location, price_tier)
            restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
            restaurant_reviews = get_object_or_404(Restaurant_Reviews, pk=restaurant_id)
            return render(request, 'polls/restaurantView.html', {'restaurant' : restaurant, "restaurant_reviews" : restaurant_reviews})
        helper.deleteEntity(conn, 'polls_restaurant', restaurant_id)
        return redirect('allRestaurantView')
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    restaurant_reviews = get_object_or_404(Restaurant_Reviews, pk=restaurant_id)
    return render(request, 'polls/restaurantView.html', {'restaurant' : restaurant, "restaurant_reviews" : restaurant_reviews})

def customerView (request, restaurant_id):
    if request.method == "POST":
        if request.POST.get('write'):
            database = 'User_Reviews'
            name = request.POST.get("user_name")
            title = request.POST.get("review_title")
            text = request.POST.get("review_text")
            rating = request.POST.get("rating")
            if (name == "" or title == "" or text == "" or rating is None):
                return redirect('customerView', restaurant_id)
            try:
                conn = MongoClient('localhost',27017)
            except:
                return 0
            db = conn[database]
            collection = db['polls_restaurant_reviews']
            current_restaurant = collection.find({"id" : restaurant_id})
            for ok in current_restaurant:
                count = ok["review_count"]
                sum = ok["rating_sum"]
            avgRating = (sum + float(rating)) / (count + 1)
            collection.update_one({'id':restaurant_id}, {'$push':{'review_list':{"review_title":title, "user_name": name, "date_written":datetime.datetime.now(), "review_text" : text, "star_rating" : float(rating)}}})
            collection.update_one({'id':restaurant_id}, {"$inc" : {'review_count' : 1, 'rating_sum' : float(rating)}})
            collection.update_one({'id':restaurant_id}, {"$set" : {'avg_rating' : avgRating}})
            conn.close()
            restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
            restaurant_reviews = get_object_or_404(Restaurant_Reviews, pk=restaurant_id)
            return render(request, 'polls/customerView.html', {'restaurant' : restaurant, "restaurant_reviews" : restaurant_reviews})
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    restaurant_reviews = get_object_or_404(Restaurant_Reviews, pk=restaurant_id)
    return render(request, 'polls/customerView.html', {'restaurant' : restaurant, "restaurant_reviews" : restaurant_reviews})
def allRestaurantView(request):
    allRest = Restaurant.objects.all()
    context = {'allRest' : allRest}
    return render(request, 'polls/allRestaurantView.html', context)

def insertUserView(request):
    if request.method == 'POST':
        if request.POST.get('user_name'):
            conn = helper.create_connection(database)
            if conn is None:
                return redirect('homeView')
            user_name = request.POST.get('user_name')
            date_created = timezone.now()
            location = request.POST.get('location')
            favorite_restaurant = request.POST.get('favorite_restaurant')
            user_id = helper.insertUser(conn, user_name, date_created, location, favorite_restaurant)
            user = get_object_or_404(User, pk=user_id)
            return redirect('personalUserView', user_id)
    return redirect('homeView')

def insertRestaurantView(request):
    if request.method == 'POST':
        if request.POST.get('restaurant_name'):
            conn = helper.create_connection(database)
            if conn is None:
                return redirect('homeView')
            restaurant_name = request.POST.get('restaurant_name')
            location = request.POST.get('location')
            price_tier = request.POST.get('price_tier')
            tagString = request.POST.getlist('cuisines')
            if helper.notValid(price_tier.strip(), 'price_tier'):
                return redirect('homeView')
            rating = request.POST.get('rating')
            if helper.notValid(rating, 'rating'):
                return redirect('homeView')
            restaurant_id = helper.insertRestaurant(conn, restaurant_name, location, price_tier, rating, tagString)
            return redirect('restaurantView', restaurant_id)
    return redirect('homeView')
