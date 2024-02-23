from django.core.management.base import BaseCommand
from datetime import date, timedelta
from screen.models import Show, Movie, CinemaHall, City

class Command(BaseCommand):
    help = 'Creates show instances for multiple movies, cinema halls, cities, timings, and date range'

    def handle(self, *args, **kwargs):
        # Define movie names, cinema hall names, cities, timings, and date range
        movie_names = ["TENET", "FIFTY SHADES", "JAWAN", "THE BATMAN"]
        cinema_hall_names = ["PVR Amritsar", "PVR Ambala", "PVR Mumbai", "PVR Delhi","PVR Chandigarh"]
        cities = ["Amritsar", "Ambala", "Mumbai", "Delhi","Chandigarh"]
        timings = "9:00 AM"
        start_date = date(2024, 2, 24)
        end_date = date(2024, 2, 28)

        # Iterate over each combination and create Show instances
        for movie_name in movie_names:
            movie = Movie.objects.get(name=movie_name)

            for cinema_hall_name, city_name in zip(cinema_hall_names, cities):
                cinema_hall = CinemaHall.objects.get(name=cinema_hall_name)
                city = City.objects.get(name=city_name)

                current_date = start_date
                while current_date <= end_date:
                    # Create Show instance for the current combination
                    show = Show.objects.create(
                        movie=movie,
                        cinemahall=cinema_hall,
                        city=city,
                        timings=timings,
                        date=current_date,
                        NumOfSeats=200  # Assuming 200 seats available for each show
                    )
                    self.stdout.write(self.style.SUCCESS(f"Show created for {movie_name} at {cinema_hall_name} in {city_name} on {current_date}"))
                    
                    # Move to the next date
                    current_date += timedelta(days=1)
