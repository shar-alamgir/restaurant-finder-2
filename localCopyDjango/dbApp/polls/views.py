from django.shortcuts import render
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

def userView(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'polls/userView.html', {'user' : user})

def allUsersView(request):
    allUsers = User.objects.all()
    context = {'allUsers' : allUsers}
    return render(request, 'polls/allUsersView.html', context)

def restaurantView(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    return render(request, 'polls/restaurantView.html', {'restaurant' : restaurant})

def allRestaurantView(request):
    allRest = Restaurant.objects.all()
    context = {'allRest' : allRest}
    return render(request, 'polls/allRestaurantView.html', context)

def userView(request):
    pdb.set_trace()
    if request.method == 'POST':
        form = cgi.FieldStorage()
        if request.POST.get('user_name'):
            database = r"/Users/vincentnguyen/rf2/localCopyDjango/dbApp/db.sqlite3"
            conn = helper.create_connection(database)
            if conn is None:
                return render(request, 'polls/homeView.html')
            user_name = form.getvalue('user_name')
            date_created = timezone.now()
            location = user_name = form.getvalue('location')
            favorite_restaurant = form.getvalue('favorite_restaurant')
            user_id = helper.insertUser(conn, user_name, date_created, location, favorite_restaurant)
            user = get_object_or_404(User, pk=user_id)
            return render(request, 'polls/userView.html', {'user' : user})
    return render(request, 'polls/homeView.html')
