# populate_seats.py
from django.core.management.base import BaseCommand
from screen.models import CinemaHall, SeatingConfiguration

class Command(BaseCommand):
    help = 'Populate seating configuration for PVR Amritsar'

    def handle(self, *args, **kwargs):
        # Get or create the cinema hall
        cinema_hall, _ = CinemaHall.objects.get_or_create(name="PVR Amritsar")

        # Define seat names and prices
        seat_prices = {
            'A': 150, 'B': 150, 'C': 150, 'D': 150, 'E': 150,
            'F': 170, 'G': 170, 'H': 170, 'I': 200, 'J': 200
        }

        # Populate seating configuration
        for row in 'ABCDEFGHIJ':
            for seat_number in range(1, 11):
                seat_name = f'{row}{seat_number}'
                seat_price = seat_prices.get(row)
                SeatingConfiguration.objects.create(
                    theater=cinema_hall,
                    seat_name=seat_name,
                    seat_price=seat_price
                )

        self.stdout.write(self.style.SUCCESS('Seating configuration populated successfully!'))
