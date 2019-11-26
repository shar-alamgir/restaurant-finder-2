from django.urls import path

from . import views



#User delete, send to home view in html
#restaurant delete, send to home view in html
app_name = ''
urlpatterns = [
    path('', views.homeView, name='homeView'),
    path('searchView/', views.searchView, name='searchView'),
    path('searchResultsView/', views.searchResultsView, name='searchResultsView'),
    path('<int:user_id>/', views.userView, name='userView'),
    path('<int:user_id>/personalUserView', views.personalUserView, name='personalUserView'),
    path('allUsersView/', views.allUsersView, name='allUsersView'),
    path('allRestaurantView/', views.allRestaurantView, name='allRestaurantView'),
    path('<int:restaurant_id>/restaurantView', views.restaurantView, name='restaurantView'),
    path('insertUserView/', views.insertUserView, name='insertUserView'),
    path('insertRestaurantView/', views.insertRestaurantView, name='insertRestaurantView'),
    path('<int:restaurant_id>/customerView', views.customerView, name='customerView'),
]
