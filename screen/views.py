from django.shortcuts import render, redirect,get_list_or_404
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from .models import Movie,City,Show
from django.http import JsonResponse,HttpResponse
from django.shortcuts import get_object_or_404
import logging





def index(request):
    cities = City.objects.all()
    return render(request,"screen/index.html",{
        'cities' :cities
    })

def description(request):
    return render(request,"screen/description.html")

def shows(request):
    return render(request,"screen/shows.html")

def get_cities(request):
    cities = City.objects.all().values('name')
    return JsonResponse(list(cities), safe=False)

def get_movies(request, city):
    current_site = get_current_site(request)
    selected_city = get_object_or_404(City, name=city)
    movies = selected_city.movie.all().values('name', 'image')
    absolute_media_url = f"{request.scheme}://{current_site}{settings.MEDIA_URL}"
    for movie in movies:
        movie['image'] = f"{absolute_media_url}{movie['image']}"
    return JsonResponse(list(movies), safe=False)



def get_movies_by_age_rating(request, city, age_rating):
    current_site = get_current_site(request)
    selected_city = get_object_or_404(City, name=city)
    movies = Movie.objects.filter(city=selected_city, adult_or_underaged__certificate=age_rating).values('name', 'image')
    absolute_media_url = f"{request.scheme}://{current_site}{settings.MEDIA_URL}"
    for movie in movies:
        movie['image'] = f"{absolute_media_url}{movie['image']}"
    return JsonResponse(list(movies), safe=False)



def get_movies_by_language(request, city, language):
    current_site = get_current_site(request)
    selected_city = get_object_or_404(City, name=city)
    movies = Movie.objects.filter(city=selected_city, language__lanName=language).values('name', 'image')
    absolute_media_url = f"{request.scheme}://{current_site}{settings.MEDIA_URL}"
    for movie in movies:
        movie['image'] = f"{absolute_media_url}{movie['image']}"
    return JsonResponse(list(movies), safe=False)



def search_movies(request, query, city_name):
    current_site = get_current_site(request)
    
    # Filter movies by name and city
    movies = Movie.objects.filter(name__icontains=query, city__name=city_name)
    
    if movies.exists():
        # If movies are found, prepare data and return JSON response
        absolute_media_url = f"{request.scheme}://{current_site}{settings.MEDIA_URL}"
        movies_data = [{
            'name': movie.name,
            'image': f"{absolute_media_url}{movie.image}"
        } for movie in movies]
        return JsonResponse(movies_data, safe=False)
    else:
        # If no movies are found, return a message indicating the movie is not running in the city
        return JsonResponse({'message': f"The movie '{query}' is not running in {city_name}."})

def movie_details(request, movie_name):
    try:
        movie = Movie.objects.get(name=movie_name)
        actors = movie.cast.all()
        city = request.GET.get('city', '')  # Get the city from query parameters
        return render(request, "screen/description.html", {'movie': movie, 'actors': actors, 'city': city})
    except Movie.DoesNotExist:
        # Handle case where movie doesn't exist
        return HttpResponse("Movie not found", status=404)


