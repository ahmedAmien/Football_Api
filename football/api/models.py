from django.db import models

# Create your models here.

class Seasons(models.Model):
    year = models.PositiveSmallIntegerField()
    
    
class Countries(models.Model):
    name = models.CharField(max_length=125, unique=True)
    code = models.CharField(max_length=3)
    nationality = models.CharField(max_length=125, null=True, unique=True)
    flag = models.URLField()
    
class Stadiums(models.Model):
    name = models.CharField(max_length=125)
    country_id = models.ForeignKey(Countries,related_name="stadiums", on_delete=models.RESTRICT, blank=True)
    capacity = models.PositiveIntegerField()
  
class Teams(models.Model):
    name = models.CharField(max_length=125)
    country_id = models.ForeignKey(Countries,related_name="teams", on_delete=models.RESTRICT)
    stadiums_id = models.ForeignKey(Stadiums,related_name="teams", null=True, on_delete=models.RESTRICT)
    logo = models.URLField(null=True)
    national = models.BooleanField()
    founded = models.PositiveSmallIntegerField(null=True)

class Leagues(models.Model):
    name = models.CharField(max_length=255)
    logo = models.URLField(null=True)
    country_id = models.ForeignKey(Countries,related_name="leagues", on_delete=models.RESTRICT)
    type = models.CharField(max_length=20)
    rank = models.PositiveSmallIntegerField(default=1000)
    seasons = models.ManyToManyField(Seasons,blank=True, related_name="leagues")
    

class Players(models.Model):
    name = models.CharField(max_length=125)
    first = models.CharField(max_length=100)
    last = models.CharField(max_length=100)
    country_id = models.ForeignKey(Countries,related_name="players", on_delete=models.RESTRICT)
    team_id = models.ForeignKey(Teams,related_name="players", on_delete=models.RESTRICT)
    age = models.CharField(max_length=3, blank=True, null=True)
    height = models.CharField(max_length=10, blank=True, null=True)
    weight = models.CharField(max_length=10, blank=True, null=True)
    photo = models.URLField()
    position = models.CharField(max_length=25)
    injured = models.BooleanField()
    
   