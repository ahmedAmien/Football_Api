from django.contrib import admin
from .models import Seasons, Countries, Stadiums, Teams, Leagues, Players, LeaguesSeasonsTeams, LeaguesSeasons, LeaguesSeasonsTeamss  


admin.site.register(Seasons)
admin.site.register(Countries)
admin.site.register(Stadiums)
admin.site.register(Teams)
admin.site.register(Leagues)
admin.site.register(Players)
admin.site.register(LeaguesSeasonsTeams)
admin.site.register(LeaguesSeasons)
admin.site.register(LeaguesSeasonsTeamss)
# admin.site.register(TeamsLeaguesSeasons)
# admin.site.register(PlayerStatistics)