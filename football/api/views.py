from django.shortcuts import render
from requests.sessions import session
from .models import Countries, Stadiums, Seasons, Teams, Leagues, Players,LeaguesSeasons, LeaguesSeasonsTeamss, LeaguesSeasonsTeams
from django.db.models import Q
import requests
import asyncio
import time
import aiohttp
import json
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework import status, filters
from rest_framework.response import Response
from .serializers import LeaguesSerializer,LeaguesSeasonsTeamsSerializer,TeamsMiniSerializer, TeamsSerializer
from rest_framework.pagination import PageNumberPagination
from django.db.models.functions import Concat
from django.db.models import Value
from asgiref.sync import sync_to_async

# Create your views here.

headers = {
'x-rapidapi-host': 'api-football-v1.p.rapidapi.com',
'x-rapidapi-key': '7a9a1d8bb8msh27eb7eeaf12d1bfp1f3ff7jsnf669a8c4b858'
}

players_ids = Players.objects.values_list('id')
players_ids = [player[0] for player in players_ids]
leagues_ = Leagues.objects.all()
teams_  = Teams.objects.all()[2208:]


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

    for i in range(10505,80000):
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

def player_team_insert():
    for team in teams_:
        url = "https://api-football-v1.p.rapidapi.com/v3/players/squads"
        
        querystring = {"team":str(team.id)}
        response = requests.request("GET", url, headers=headers, params=querystring)
        response = response.json()
        try:
            response = response['response']
            response_players = response[0]['players']
            print("TEAM_ID: ",team.id, "players_numer: ",len(response[0]['players']))
            for player in response_players:
                if player['id'] not in players_ids:
                    player_a= Players(
                                pk=player['id']
                                , name=player['name']
                                , photo=player['photo']
                                , age=player['age']
                                , injured= False
                                , position = player['position']
                                )
                    player_a.save()
                    player_a.team_id.add(team)
                    player_a.save()      
                    players_ids.append(player['id'])         

        except Exception as e:
            print(e)
            
            
def player_insert(start, end): 
    
    for i in range(start, end):
        url = "https://api-football-v1.p.rapidapi.com/v3/players"
        querystring = {
                "id":i,
                "season":"2020"
            }
        time.sleep(0.05)
        response = requests.request("GET", url, headers=headers, params=querystring)
        player = response.json()
        try:
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
                player_ = Players(
                                    pk=player['player']['id']
                                , name=player['player']['name']
                                , first=player['player']['firstname']
                                , last=player['player']['lastname']
                                , country_id=country
                                , photo=player['player']['photo']
                                , age=player['player']['age']
                                , height=player['player']['height']
                                , weight=player['player']['weight']
                                , injured= player['player']['injured']
                                , position = player['statistics'][0]['games']['position']
                                )
                player_.save()
                player_.team_id.add(team)
                player_.save()
            except Exception as e:
                print(e, "line 150")
            
        except Exception as e:
            print(e, player)


def player_add_teams():
    players = Players.objects.filter(team_id__id= None).order_by('id')
    for player_ in players:
        print(player_.id, player_.team_id)
        url = "https://api-football-v1.p.rapidapi.com/v3/players"
        querystring = {
                "id":player_.id,
                "season":"2020"
            }
        response = requests.request("GET", url, headers=headers, params=querystring)
        player = response.json()
        player = player['response']
        if player:
            player = player[0]
            try:
                team = Teams.objects.get(pk=player['statistics'][0]['team']['id'])
                player_.team_id.add(team)
                player_.save()
            except Exception as e:
                print(player['statistics'][0]['team']['id'])
                continue

                                              
def country_from_ip(request):
    
    x_forw_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forw_for is not None:
        ip = x_forw_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
        
    response = requests.get(f"http://ip-api.com/json/{ip}").json()
    
    country = response['country']
    country_code = response['countryCode']
    
    return (country, country_code)

def index(request):
    # league_id = 38
    # seasons = "2017"
    # url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    # querystring = {"league":league_id,"season":seasons}
    # response = requests.request("GET", url, headers=headers, params=querystring) 
    # # try:
    # response = response.json()   
    # seasons_ = Seasons.objects.get(year=seasons)    
    # league = Leagues.objects.get(id=league_id)
    # # with open("xxxx.json", 'w') as fd:
    # #     json.dump(response, fd)
        
    # response = response['response']
    # teams_id = []
    # teams_name = []
    # l = LeaguesSeasonsTeams(seasons=seasons_, leagues_id=league)
    # l.save()
    # for res in response:
    #     # if "Group" in res['league']['round']:
    #     home_id = res['teams']['home']['id']
    #     if home_id not in teams_id:
    #         l.team_id.add(home_id)
    #         l.save()                
    #         teams_id.append(home_id)
    #         teams_name.append(res['teams']['home']['name'])
    # # context = {}
    # # print(mo)

#hna kolo bayz#

    # leagues_seasons_teams = LeaguesSeasonsTeams.objects.order_by('id').all()
    # for i in leagues_seasons_teams:
    #     count = 0
    #     l = LeaguesSeasons.objects.get(leagues_id=i.leagues_id, seasons=i.seasons)
    #     for j in i.team_id.all():
    #         if j:
    #             count += 1
    #             LeaguesSeasonsTeamss(LeaguesSeasons=l,team_id = j).save()
    #         else:
    #             if count == 0:
    #                LeaguesSeasonsTeamss(LeaguesSeasons=l).save() 
    #     count = 0        
    return HttpResponse("WELCOME")

def add_player(request, page):
    player_team_insert()
        
    return HttpResponse(page)


def add_teams_to_player(request):
    player_add_teams()
    return HttpResponse("DONE")

def add_leagues_seasons_teams(request):
    seasons = Seasons.objects.get(year=2020)
    for league in leagues_:
        teams_id = []
        try:
            leagues_exsits = LeaguesSeasonsTeams.objects.get(seasons__year=2020, leagues_id__id=league.id)
        except:                
            url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
            querystring = {"league":league.id,"season":"2020"}
            response = requests.request("GET", url, headers=headers, params=querystring) 
            # try:
            response = response.json()   
            response = response['response']
            l = LeaguesSeasonsTeams(leagues_id=league,seasons=seasons)
            l.save()
            for res in response:
                
                home_id = res['teams']['home']['id']
                away_id = res['teams']['away']['id']
                if home_id not in teams_id:
                    l.team_id.add(home_id)
                    l.save()
                    l.team_id.add(away_id)
                    l.save()
                    teams_id.append(home_id)
                    teams_id.append(away_id)
            # except:
            #     pass
    return HttpResponse("DONE")


@api_view(['GET'])
def top_ten_leagues(request):
    ten_leagues = Leagues.objects.order_by('rank')[:11]
    country_league = ""
    try:
        coutry_ = country_from_ip(request)
        country_league = Countries.objects.get(name=coutry_[0].replace(" ", "-")).leagues.filter(type='league')[0]
    except:
        pass
    if country_league:
        leagues_with_country_league = []
        leagues_with_country_league.append(country_league)
        for league in ten_leagues:
            leagues_with_country_league.append(league)
        serializer = LeaguesSerializer(leagues_with_country_league, many=True)
    else:
        serializer = LeaguesSerializer(ten_leagues, many=True)

    return Response({"data":serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def all_leagues(request):
    if request.method == 'POST':
        leagues = Leagues.objects.filter(
            Q(name__icontains = request.data['name']) | Q(country_id__name__icontains = request.data['name']))
        
        if not leagues:
            queryset = Leagues.objects.annotate(search_name=Concat('name', Value(' '), 'country_id__name'))
            leagues = queryset.filter(search_name__icontains=request.data['name'])    
            if not leagues:
                queryset = Leagues.objects.annotate(search_name=Concat('country_id__name', Value(' '), 'name'))
                leagues = queryset.filter(search_name__icontains=request.data['name']) 
        if leagues:
            serializer = LeaguesSerializer(leagues, many=True)
            return Response({"data":serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"data":[]},status=status.HTTP_200_OK)
        
    paginator = PageNumberPagination()
    paginator.page_size = 25
    leagues = Leagues.objects.all()
    result_page = paginator.paginate_queryset(leagues, request)
    serializer = LeaguesSerializer(result_page, many=True)
    return paginator.get_paginated_response({"data":serializer.data})

@api_view(['POST'])
def leagues_teams(request):
    
    if request.method == 'POST':
        leagues_ids = []
        if type(request.data['leagues']) == str:
            leagues_ids = request.data['leagues'].replace('[','').replace(']','')
            if len(leagues_ids) < 1:
                return Response({"data":[]}, status=status.HTTP_200_OK)
            leagues_ids = leagues_ids.split(',')
        else:
            leagues_ids = request.data['leagues']        

        # leagues = Leagues.objects.filter(Q(pk__in = leagues_ids))
        leagues_with_all_seasons = LeaguesSeasonsTeams.objects.order_by('-seasons__year').filter(Q(leagues_id__in = leagues_ids))
        leagues_with_last_season = []
        unique_ids = []
        for i in leagues_with_all_seasons:
            if not i.leagues_id in unique_ids:
                leagues_with_last_season.append(i)
                unique_ids.append(i.leagues_id)
                
        teams_serializer = LeaguesSeasonsTeamsSerializer(leagues_with_last_season, many=True)
        return Response({"data":teams_serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def teams(request):
    if request.method == 'POST':
        # print(request.data['team'])
        teams_ = Teams.objects.filter(Q(name__icontains = request.data['team']))
        # print(teams_)
        serializer = TeamsSerializer(teams_, many=True)
        if teams_:
          return Response({"data":serializer.data}, status=status.HTTP_200_OK)  
        return Response({"data":[]},status=status.HTTP_200_OK)
    #hna hanzwd el most popular 
    teams_ = Teams.objects.all()[:26]
    serializer = TeamsSerializer(teams_, many=True)
    return Response({"data":serializer.data})


# @api_view(['GET'])
# def player_static(request):
#     pass
#     # if request.method == 'POST':
#     #     # print(request.data['team'])
#     #     teams_ = Teams.objects.filter(Q(name__icontains = request.data['team']))
#     #     # print(teams_)
#     #     serializer = TeamsSerializer(teams_, many=True)
#     #     if teams_:
#     #       return Response({"data":serializer.data}, status=status.HTTP_200_OK)  
#     #     return Response({"data":[]},status=status.HTTP_200_OK)
#     #hna hanzwd el most popular 
#     teams_ = PlayerStatistics.objects.all()[:26]
#     serializer = PlayerStatisticsSerializer(teams_, many=True)
#     return Response({"data":serializer.data})