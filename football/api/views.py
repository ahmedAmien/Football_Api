from django.shortcuts import render
from requests.sessions import session
from .models import Countries, Stadiums, Seasons, Teams, Leagues, Players
import requests
from django.http import HttpResponse
# Create your views here.

headers = {
'x-rapidapi-host': 'api-football-v1.p.rapidapi.com',
'x-rapidapi-key': '7a9a1d8bb8msh27eb7eeaf12d1bfp1f3ff7jsnf669a8c4b858'
}

def country_insert():
    
    url = "https://api-football-v1.p.rapidapi.com/v3/countries"
    
    response = requests.request("GET", url, headers=headers)

    countries = response.json()
    for country in countries["response"]:
        
        if str(country['name']).upper() == 'World'.upper():
            Countries(name='World',flag='All',code='111').save()
        else:
            Countries(name=country['name'],flag=country['flag'],code=country['code']).save()

def seasons_insert():
    url = "https://api-football-v1.p.rapidapi.com/v3/leagues/seasons"

    response = requests.request("GET", url, headers=headers)
    seasons = response.json()
    for season in seasons['response']:
        Seasons(year=season).save()
  
def league_insert():
    headers = {
    'x-rapidapi-host': 'api-football-v1.p.rapidapi.com',
    'x-rapidapi-key': '7a9a1d8bb8msh27eb7eeaf12d1bfp1f3ff7jsnf669a8c4b858'
    }
    url = "https://api-football-v1.p.rapidapi.com/v3/leagues"

    response = requests.request("GET", url, headers=headers)
    leagues = response.json()
    for league in leagues['response']:
        league_seasons = []
        l = Leagues.objects.values_list('id', flat=True)
        l = list(l)
        Country = Countries.objects.get(name=league['country']['name'])
        years = [year['year'] for year in league['seasons']]
        seasons = Seasons.objects.filter(year__in=years)      
        if league['league']['id'] not in l:       
            league = Leagues(pk=league['league']['id'], name=league['league']['name'], type=league['league']['type'], logo=league['league']['logo'], country_id=Country)
            for i in seasons:
                league.seasons.add(i)
            league.save()
                
def stadiums_insert():
    url = "https://api-football-v1.p.rapidapi.com/v3/venues"
    countries = Countries.objects.all()
    

    for country in countries:
        if country.name == 'World':
            continue

        querystring = {"country": country.name}
        response = requests.request("GET", url, headers=headers, params=querystring)
        stadiums = response.json()
        stadiums = stadiums['response']
        for stadium in stadiums:
            try:
                Stadiums(pk=stadium['id'], country_id=country, name=stadium['name'], capacity=stadium['capacity']).save()
            except Exception as e:
                print(e)
                
def teams_insert():

    for i in range(80000):
        url = "https://api-football-v1.p.rapidapi.com/v3/teams"
        querystring = {
                "id":i
            }
        response = requests.request("GET", url, headers=headers, params=querystring)
        team = response.json()
        team = team['response']
        if team:
            team = team[0]
            try:
                country = Countries.objects.get(name=team['team']['country'].replace(" ","-"))
            except:
                print(team['team']['country'])
        else:
            continue
        try:
            if team['venue']['id']:
                try:
                    stadium_ = Stadiums(name=team['venue']['name'], pk=team['venue']['id'], country_id=country, capacity=team['venue']['capacity'])
                    stadium_.save()
                    
                except Exception as e:
                    print(e, "line 95")     
            staduim_id = Stadiums.objects.get(pk=team['venue']['id'])
            team_ = Teams(pk=team['team']['id'], name=team['team']['name'], country_id=country,stadiums_id=staduim_id, logo=team['team']['logo'],national=team['team']['national'], founded=team['team']['founded'])
            team_.save()
        except:
            try:
                team_ = Teams(pk=team['team']['id'], name=team['team']['name'], country_id=country, logo=team['team']['logo'],national=team['team']['national'], founded=team['team']['founded'])
                team_.save()
            except Exception as e:
                print(e, "line 124")



def player_insert():
    
    for i in range(80000):
        url = "https://api-football-v1.p.rapidapi.com/v3/players"
        querystring = {
                "id":i,
                "season":"2020"
            }
        response = requests.request("GET", url, headers=headers, params=querystring)
        player = response.json()
        player = player['response']
        if player:
            player = player[0]
            try:
                
                try:
                    country = Countries.objects.get(name=player['player']['nationality'].replace(" ","-"))
                except:
                    Countries(name=player['player']['nationality'].replace(" ","-"),code="000",flag="000").save()
                country = Countries.objects.get(name=player['player']['nationality'].replace(" ","-"))
                team = Teams.objects.get(pk=player['statistics'][0]['team']['id'])
            except Exception as e:
                print(e)
                print(player['player']['nationality'])
                print(player['statistics'][0]['team']['id'])
                continue
        else:
            continue
        try:  
            player_ = Players(pk=player['player']['id']
                              , name=player['player']['name'], first=player['player']['firstname'], last=player['player']['lastname']
                              , country_id=country,team_id=team
                              , photo=player['player']['photo']
                              ,age=player['player']['age']
                              , height=player['player']['height']
                              ,weight=player['player']['weight']
                              ,injured= player['player']['injured']
                              ,position = player['statistics'][0]['games']['position']
                              )
            player_.save()
            
        except Exception as e:
            print(e, "line 150")

def index(request):
    player_insert()
    return HttpResponse("hello")


def hello(request):
    return HttpResponse("hello, world")