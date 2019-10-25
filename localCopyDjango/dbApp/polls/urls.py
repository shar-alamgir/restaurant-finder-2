from django.urls import path

from . import views

app_name = ''
urlpatterns = [
    path('', views.homeView, name='homeView'),
    path('<int:user_id>/', views.userView, name='userView'),
    path('allUsersView/', views.allUsersView, name='allUsersView'),
    path('<int:restaurant_id>/restaurantView', views.restaurantView, name='restaurantView'),
    path('newUser', views.newUser, name='newUser'),
]
