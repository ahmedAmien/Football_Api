from django.db import models

# Create your models here.

class Seasons(models.Model):
    year = models.PositiveSmallIntegerField()
    
    
class Countries(models.Model):
    name = models.CharField(max_length=125, unique=True)
    code = models.CharField(max_length=3)
    nationality = models.CharField(max_length=125, blank=True, null=True, unique=True)
    flag = models.URLField()
    
class Stadiums(models.Model):
    name = models.CharField(max_length=125)
    country_id = models.ForeignKey(Countries,related_name="stadiums", on_delete=models.RESTRICT, blank=True)
    capacity = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.name}"
  
class Teams(models.Model):
    name = models.CharField(max_length=125)
    country_id = models.ForeignKey(Countries,related_name="teams", on_delete=models.RESTRICT)
    stadiums_id = models.ForeignKey(Stadiums,related_name="teams", blank=True, null=True, on_delete=models.RESTRICT)
    logo = models.URLField(null=True, blank=True)
    national = models.BooleanField()
    founded = models.PositiveSmallIntegerField(null=True, blank=True)

class Leagues(models.Model):
    name = models.CharField(max_length=255)
    logo = models.URLField(null=True, blank=True)
    country_id = models.ForeignKey(Countries,related_name="leagues", on_delete=models.RESTRICT)
    type = models.CharField(max_length=20)
    rank = models.PositiveSmallIntegerField(default=1000)

class LeaguesSeasonsTeams(models.Model):
    leagues_id = models.ForeignKey(Leagues, on_delete=models.RESTRICT, related_name="seasons")
    seasons = models.ForeignKey(Seasons, on_delete=models.RESTRICT, related_name="leagues")
    team_id = models.ManyToManyField(Teams,related_name="leagues")

class LeaguesSeasons(models.Model):
    leagues_id = models.ForeignKey(Leagues, on_delete=models.RESTRICT, related_name="seson")
    seasons = models.ForeignKey(Seasons, on_delete=models.RESTRICT, related_name="leage")

class LeaguesSeasonsTeamss(models.Model):
    LeaguesSeasons = models.ForeignKey(LeaguesSeasons, on_delete=models.RESTRICT, related_name="teams")
    team_id = models.ForeignKey(Teams, on_delete=models.RESTRICT, related_name="leaguess", blank=True, null=True,)
    
class Players(models.Model):
    name = models.CharField(max_length=125)
    first = models.CharField(max_length=100, blank=True, null=True)
    last = models.CharField(max_length=100, blank=True, null=True)
    country_id = models.ForeignKey(Countries,related_name="players", on_delete=models.RESTRICT, blank=True, null=True)
    age = models.CharField(max_length=3, blank=True, null=True)
    height = models.CharField(max_length=10, blank=True, null=True)
    weight = models.CharField(max_length=10, blank=True, null=True)
    birth = models.DateField(blank=True, null=True)
    photo = models.URLField()
    position = models.CharField(max_length=25)
    injured = models.BooleanField(default=False)    
   
   
# class TeamsLeaguesSeasons(models.Model):
#     leagues_id = models.ForeignKey(Leagues, on_delete=models.RESTRICT)
#     team_id = models.ForeignKey(Teams, on_delete=models.RESTRICT, related_name="players")
#     seasons = models.ForeignKey(Seasons, on_delete=models.RESTRICT, related_name="teams")  
    
# class PlayerStatistics(models.Model):
#     team_league_season = models.ForeignKey(TeamsLeaguesSeasons, on_delete=models.RESTRICT, related_name="player_statistics")
#     player_id = models.ForeignKey(Players, on_delete=models.RESTRICT, related_name="player_statistics")
#     appearences = models.PositiveSmallIntegerField(blank=True, null=True)
#     position = models.CharField(max_length=25)
#     rating = models.CharField(max_length=15)
#     number = models.PositiveSmallIntegerField(blank=True, null=True) 
#     captain = models.BooleanField(default=False) 
#     substitutes_in = models.PositiveSmallIntegerField(blank=True, null=True)  
#     substitutes_out = models.PositiveSmallIntegerField(blank=True, null=True)
#     substitutes_bench = models.PositiveSmallIntegerField(blank=True, null=True)
#     shots_total = models.PositiveSmallIntegerField(blank=True, null=True)
#     shots_on = models.PositiveSmallIntegerField(blank=True, null=True)
#     goals_total = models.PositiveSmallIntegerField(blank=True, null=True)
#     goals_conceded = models.PositiveSmallIntegerField(blank=True, null=True)
#     goals_assists = models.PositiveSmallIntegerField(blank=True, null=True)
#     goals_saves = models.PositiveSmallIntegerField(blank=True, null=True)
#     passes_total = models.PositiveSmallIntegerField(blank=True, null=True)
#     passes_key = models.PositiveSmallIntegerField(blank=True, null=True)
#     passes_accuracy = models.PositiveSmallIntegerField(blank=True, null=True)
#     tackles_total = models.PositiveSmallIntegerField(blank=True, null=True)
#     tackles_blocks = models.PositiveSmallIntegerField(blank=True, null=True)
#     tackles_interceptions = models.PositiveSmallIntegerField(blank=True, null=True)
#     duels_total = models.PositiveSmallIntegerField(blank=True, null=True)
#     duels_won = models.PositiveSmallIntegerField(blank=True, null=True)
#     dribbles_attempts = models.PositiveSmallIntegerField(blank=True, null=True)
#     dribbles_success = models.PositiveSmallIntegerField(blank=True, null=True)
#     dribbles_success = models.PositiveSmallIntegerField(blank=True, null=True)
#     fouls_drawn = models.PositiveSmallIntegerField(blank=True, null=True)
#     fouls_committed = models.PositiveSmallIntegerField(blank=True, null=True)
#     cards_yellow = models.PositiveSmallIntegerField(blank=True, null=True)
#     cards_yellowred = models.PositiveSmallIntegerField(blank=True, null=True)
#     cards_red = models.PositiveSmallIntegerField(blank=True, null=True)
#     penalty_won = models.PositiveSmallIntegerField(blank=True, null=True)
#     penalty_commited = models.PositiveSmallIntegerField(blank=True, null=True)
#     penalty_scored = models.PositiveSmallIntegerField(blank=True, null=True)
#     penalty_missed = models.PositiveSmallIntegerField(blank=True, null=True)
#     penalty_saved = models.PositiveSmallIntegerField(blank=True, null=True)
