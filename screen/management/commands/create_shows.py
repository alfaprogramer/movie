from django.core.management.base import BaseCommand
from datetime import date, timedelta
from screen.models import Show, Movie, CinemaHall, City

class Command(BaseCommand):
    help = 'Creates show instances for multiple movies, cinema halls, cities, timings, date range and price'

    def handle(self, *args, **kwargs):
        # Define movie names, cinema hall names, timings, and date range
        movie_names = ["THE BATMAN"]
        cinema_hall_names = ["PVR Amritsar", "Nexus Mall", "Vr Mall"]
        timings = [
            ["9:00 AM", "10:00 AM", "12:00 PM", "1:30 PM", "4:20 PM", "6:10 PM", "8:05 AM"],
            ["9:00 AM", "10:00 AM", "12:00 PM", "2:30 PM", "4:20 PM"],
            ["9:30 AM", "11:00 AM", "12:30 PM", "3:00 PM", "5:00 PM"]
        ]
        start_date = date(2024, 3, 10)
        end_date = date(2024, 3, 14)

        # Get the City instance for "Amritsar"
        try:
            amritsar_city = City.objects.get(name="Amritsar")
        except City.DoesNotExist:
            self.stdout.write(self.style.ERROR("City 'Amritsar' does not exist in the database."))
            return

        # Iterate over each movie
        for movie_name in movie_names:
            try:
                movie = Movie.objects.get(name=movie_name)
            except Movie.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"Movie '{movie_name}' does not exist. Skipping..."))
                continue

            # Iterate over each cinema hall and timings
            for cinema_hall_name, timing_list in zip(cinema_hall_names, timings):
                try:
                    cinema_hall = CinemaHall.objects.get(name=cinema_hall_name)
                except CinemaHall.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f"Cinema hall '{cinema_hall_name}' does not exist. Skipping..."))
                    continue

                # Iterate over each timing for the current cinema hall
                for timing in timing_list:
                    current_date = start_date
                    # Iterate over the date range
                    while current_date <= end_date:
                        # Create Show instance for the current combination
                        show = Show.objects.create(
                            movie=movie,
                            cinemahall=cinema_hall,
                            city=amritsar_city,  # Assign City instance directly
                            timings=timing,
                            date=current_date,
                            price=170 if cinema_hall_name == "PVR Amritsar" else 150  # Set price based on cinema hall
                        )
                        self.stdout.write(self.style.SUCCESS(f"Show created for '{movie_name}' at '{cinema_hall_name}' in 'Amritsar' on {current_date} at {timing}"))
                        
                        # Move to the next date
                        current_date += timedelta(days=1)
