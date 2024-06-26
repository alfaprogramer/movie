from django.contrib import admin
from .models import Actor, Movie, City, CinemaHall, Show, Language, Aged,SeatingConfiguration,Booking

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('name','google_url')

@admin.register(Language)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('lanName',)


@admin.register(Aged)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('certificate',)        

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('name', 'language', 'adult_or_underaged')

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(CinemaHall)
class CinemaHallAdmin(admin.ModelAdmin):
    list_display = ('name', 'city')

@admin.register(SeatingConfiguration)
class SeatingConfiguration(admin.ModelAdmin):
    list_display=('theater','seat_name', 'seat_price')

@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ('movie', 'cinemahall', 'city' , 'timings','date','minP','avgP','maxP')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('movie', 'city', 'cinema_hall_id', 'date', 'show_timings', 'selected_seats', 'total_cost', 'convenience_fee', 'sum_total')


 

