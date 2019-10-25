from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import loader
from django.shortcuts import render, get_object_or_404
from .models import User, Restaurant, Menu, Hours

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

def newUser(request):
    pass
