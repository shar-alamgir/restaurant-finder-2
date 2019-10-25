from django.urls import path

from . import views



#User delete, send to home view in html
#restaurant delete, send to home view in html
app_name = ''
urlpatterns = [
    path('', views.homeView, name='homeView'),
    path('<int:user_id>/', views.userView, name='userView'),
    path('allUsersView/', views.allUsersView, name='allUsersView'),
    path('allRestaurantView/', views.allRestaurantView, name='allRestaurantView'),
    path('<int:restaurant_id>/restaurantView', views.restaurantView, name='restaurantView'),
    path('newUser', views.newUser, name='newUser'),
]
