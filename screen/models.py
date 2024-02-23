from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from datetime import date



class Actor(models.Model):
      name = models.CharField(max_length=100)
      image = models.ImageField(upload_to='actors/')
      google_url = models.URLField(blank=True)

      def __str__(self):
        return self.name
    

class Language(models.Model):
    lanName=models.CharField(max_length=50) 

    def __str__(self):
        return self.lanName   

class Aged(models.Model):
    certificate=models.CharField(max_length=50) 

    def __str__(self):
        return self.certificate


class Movie(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='movies/')
    description = models.TextField()
    cast = models.ManyToManyField(Actor)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    adult_or_underaged = models.ForeignKey(Aged, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=100)
    movie = models.ManyToManyField(Movie, blank=True)

    def __str__(self):
       
        return self.name

class CinemaHall(models.Model):
    name = models.CharField(max_length=200)
    city = models.ForeignKey(City, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name 



class Show(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    cinemahall = models.ForeignKey(CinemaHall, on_delete=models.CASCADE, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    timings = models.CharField(max_length=100)
    date = models.DateField(default=date.today)
    NumOfSeats = models.BigIntegerField(default=200)

    def __str__(self):
        return f"{self.movie.name} - {self.cinemahall.name} - {self.timings} - {self.date} - {self.NumOfSeats}"
    












