from django.shortcuts import render, redirect,get_list_or_404
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from .models import Movie,City,Show,CinemaHall,SeatingConfiguration,Booking
from django.http import JsonResponse,HttpResponse
from django.shortcuts import get_object_or_404
import logging
from django.core.mail import send_mail
from datetime import datetime





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


def shows(request, movie_name):
    selected_city = request.GET.get('city')
    
    shows = Show.objects.filter(movie__name=movie_name, city__name=selected_city)
    dates = shows.values_list('date', flat=True).distinct()
    cinema_halls = CinemaHall.objects.filter(show__in=shows).distinct()
    
    image_url = request.GET.get('image', '')  # Get the image URL from query parameters
    return render(request, 'screen/shows.html', {'movie_name': movie_name, 'shows': shows, 'dates': dates, 'cinema_halls': cinema_halls, 'image_url': image_url})




def filter_shows_by_date(request, movie_name, selected_date):
    selected_city = request.GET.get('city')
    
    # Filter shows based on movie name, city, and selected date
    shows = Show.objects.filter(movie__name=movie_name, city__name=selected_city, date=selected_date)
    
    # Prepare data to be sent as JSON response
    shows_data = list(shows.values())

    response = {
        'movie_name': movie_name,
        'shows': shows_data,
        'selected_date': selected_date,
    }

    return JsonResponse(response)


def seats(request):
    show_id = request.GET.get('show_id')
    cinema_hall_id = request.GET.get('cinema_hall_id')
    movie_name = request.GET.get('movie_name')
    city_name = request.GET.get('city_name')
    image_url = request.GET.get('image')  # Retrieve image URL from request

    # Retrieve show details
    show = Show.objects.get(id=show_id)

    # Retrieve cinema hall details
    cinema_hall = CinemaHall.objects.get(id=cinema_hall_id)

    context = {
        'show': show,
        'cinema_hall': cinema_hall,
        'movie_name': movie_name,
        'city_name': city_name,
        'image_url': image_url,  # Pass image URL to the template
    }

    return render(request, 'screen/seats.html', context)





def seats2(request):
    show_id = request.GET.get('show_id')
    cinema_hall_id = request.GET.get('cinema_hall_id')
    movie_name = request.GET.get('movie_name')
    city_name = request.GET.get('city_name')

    # Retrieve show details
    show = Show.objects.get(id=show_id)

    # Retrieve cinema hall details
    cinema_hall = CinemaHall.objects.get(id=cinema_hall_id)

    context = {
        'show': show,
        'cinema_hall': cinema_hall,
        'movie_name': movie_name,  # Pass movie name
        'city_name': city_name  # Pass city name
    }

    return render(request, 'screen/seats2.html', context)



def book(request):
    show_id = request.GET.get('show_id')
    cinema_hall_id = request.GET.get('cinema_hall_id')
    return render(request, 'screen/book.html', {'show_id': show_id, 'cinema_hall_id': cinema_hall_id})



def submit_form(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        movie = request.POST.get('movie')
        city = request.POST.get('city')
        cinema_hall = request.POST.get('cinemaHall')
        # Parse and format the date correctly
        date_str = request.POST.get('date')
        date = datetime.strptime(date_str, '%B %d, %Y').strftime('%Y-%m-%d')
        show_timings = request.POST.get('showTimings')
        selected_seats = request.POST.get('selectedSeats')
        
        # Extract numeric values for decimal fields
        total_cost = float(request.POST.get('totalCost').replace('₹', '').strip())
        convenience_fee = float(request.POST.get('convenienceFee').replace('₹', '').strip())
        sum_total = float(request.POST.get('sumTotal').replace('₹', '').strip())

        # Save booking details to the database
        booking = Booking.objects.create(
            email=email,
            movie=movie,
            city=city,
            cinema_hall=cinema_hall,
            date=date,
            show_timings=show_timings,
            selected_seats=selected_seats,
            total_cost=total_cost,
            convenience_fee=convenience_fee,
            sum_total=sum_total
        )

        booking.save()



        # Send email confirmation
        send_mail(
            'Booking Confirmation',
            'Your booking details:\nMovie: {}\nCity: {}\nCinema Hall: {}\nDate: {}\nShow Timings: {}\nSelected Seats: {}\nTotal Cost: {}\nConvenience Fee: {}\nSum Total: {}'.format(
                movie, city, cinema_hall, date, show_timings, selected_seats, total_cost, convenience_fee, sum_total
            ),
            'adipayal2@gmail.com',
            [email],
            fail_silently=False,
        )

        return JsonResponse({'success': True})

    return JsonResponse({'success': False})




def get_selected_seats(request):
    show_id = request.GET.get('show_id')
    cinema_hall = request.GET.get('cinema_hall')
    movie_name = request.GET.get('movie_name')
    city_name = request.GET.get('city_name')
    
    # Query the database to get the booked seats for the specified show
    bookings = Booking.objects.filter(
        show_id=show_id,
        cinema_hall=cinema_hall,
        movie=movie_name,
        city=city_name
    )
    
    selected_seats = []
    for booking in bookings:
        selected_seats.extend(booking.selected_seats.split(','))

    return JsonResponse({'selected_seats': selected_seats})

