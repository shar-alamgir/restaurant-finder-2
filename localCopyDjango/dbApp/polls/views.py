from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.template import loader
from django.shortcuts import render, get_object_or_404
from .models import User, Restaurant, Menu, Hours
from django.utils import timezone
import cgi
from . import helper
import pdb

def homeView(request):
    return render(request, 'polls/homeView.html')

def searchView(request):
    return render(request, 'polls/searchView.html')

def searchResultsView(request):
    if request.method == 'POST':
        if request.POST.get('restaurant'):
            database = r"/Users/Shar/djangoInstall/rf2/localCopyDjango/dbApp/db.sqlite3"
            conn = helper.create_connection(database)
            if conn is None:
                return redirect('searchView')
            searchString = request.POST.get('restaurant')
            result = helper.searchRestaurant(conn, searchString)
            context = {'result' : result}
            return render(request, 'polls/searchResultsView.html', context)
        else:
            return redirect('searchView')
    return redirect('searchView')

def userView(request, user_id):
    if request.method == 'POST':
        database = r"/Users/Shar/djangoInstall/rf2/localCopyDjango/dbApp/db.sqlite3"
        conn = helper.create_connection(database)
        if conn is None:
            return 0
        if request.POST.get('update'):
            return redirect('searchView')
        helper.deleteUser(conn, user_id)
        return redirect('polls/userView.html', {'user' : user})
    user = get_object_or_404(User, pk=user_id)
    return render(request, '/userView', {'user' : user})

def allUsersView(request):
    allUsers = User.objects.all()
    context = {'allUsers' : allUsers}
    return render(request, 'polls/allUsersView.html', context)

def restaurantView(request, restaurant_id):
    if request.method == "POST":
        database = r"/Users/Shar/djangoInstall/rf2/localCopyDjango/dbApp/db.sqlite3"
        conn = helper.create_connection(database)
        if conn is None:
            return 0
        if request.POST.get('update'):
            return redirect('/restaurantView.html', {'restaurant' : restaurant})
        helper.deleteRestaurant(conn, restaurant_id)
        return redirect('allRestaurantView')
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    return render(request, 'polls/restaurantView.html', {'restaurant' : restaurant})

def allRestaurantView(request):
    allRest = Restaurant.objects.all()
    context = {'allRest' : allRest}
    return render(request, 'polls/allRestaurantView.html', context)

def insertUserView(request):
    if request.method == 'POST':
        if request.POST.get('user_name'):
            database = r"/Users/Shar/djangoInstall/rf2/localCopyDjango/dbApp/db.sqlite3"
            conn = helper.create_connection(database)
            if conn is None:
                return redirect('homeView')
            user_name = request.POST.get('user_name')
            date_created = timezone.now()
            location = request.POST.get('location')
            favorite_restaurant = request.POST.get('favorite_restaurant')
            user_id = helper.insertUser(conn, user_name, date_created, location, favorite_restaurant)
            user = get_object_or_404(User, pk=user_id)
            return redirect('userView', user_id)
    return redirect('homeView')

def insertRestaurantView(request):
    if request.method == 'POST':
        if request.POST.get('restaurant_name'):
            database = r"/Users/Shar/djangoInstall/rf2/localCopyDjango/dbApp/db.sqlite3"
            conn = helper.create_connection(database)
            if conn is None:
                return redirect('homeView')
            restaurant_name = request.POST.get('restaurant_name')
            location = request.POST.get('location')
            price_tier = request.POST.get('price_tier')
            rating = request.POST.get('rating')
            restaurant_id = helper.insertRestaurant(conn, restaurant_name, location, price_tier, rating)
            restaurant = get_object_or_404(User, pk=restaurant_id)
            return redirect('restaurantView', restaurant_id)
    return redirect('homeView')
