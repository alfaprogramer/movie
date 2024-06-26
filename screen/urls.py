from django.contrib import admin
from django.urls import path , include
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  path('',views.index,name="index"),
  path('get_cities/', views.get_cities, name='get_cities'),
  path('get_movies/<str:city>/', views.get_movies, name='get_movies'),
  path('get_movies_by_age_rating/<str:city>/<str:age_rating>/', views.get_movies_by_age_rating, name='get_movies_by_age_rating'),
  path('get_movies_by_language/<str:city>/<str:language>/', views.get_movies_by_language, name='get_movies_by_language'),
  path('search_movies/<str:query>/<str:city_name>/', views.search_movies, name='search_movies'),
  path('movie-details/<str:movie_name>/', views.movie_details, name='movie_details'),

  
  path('shows/<str:movie_name>/', views.shows, name='shows'),
  path('shows/<str:movie_name>/filter/<str:selected_date>/', views.filter_shows_by_date, name='filter_shows_by_date'),
path('seats/',views.seats, name='seats' ) ,
path('seats2/',views.seats2, name="seats2"),
 path('book', views.book, name="book"),
path('submit-form/', views.submit_form, name='submit_form'),
path('api/seats/', views.get_selected_seats, name='get_selected_seats'),
path('api/seats2/', views.get_selected_seats, name='get_selected_seats2'),
] 

# Serve uploaded media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
