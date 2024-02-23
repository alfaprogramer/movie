from django.contrib import admin
from .models import Actor, Movie, City, CinemaHall, Show, Language, Aged

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


@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ('movie', 'cinemahall', 'city' , 'timings','date','NumOfSeats')




 

