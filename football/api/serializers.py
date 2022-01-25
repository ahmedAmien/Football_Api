from rest_framework import serializers
from .models import Countries, Stadiums, Teams, Leagues, Players, LeaguesSeasonsTeams


class LeaguesSerializer(serializers.ModelSerializer):
    country = serializers.CharField(source='country_id.name')

    class Meta:
        model = Leagues
        fields = ['id', 'name','country','rank', 'logo']
        

    
        
class CountriesSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = Countries
        fields = ['id', 'name','flag']
        

class StadiumsSerializer(serializers.ModelSerializer):
    
    country_name = serializers.CharField(source='country_id.name')
    
    class Meta:
        model = Stadiums
        fields = ['id', 'name','capacity', 'country_name']
 
        
class TeamsSerializer(serializers.ModelSerializer):
    
    country_name = serializers.CharField(source='country_id.name')
    stadiums_name = serializers.CharField(source='stadiums_id')

    class Meta:
        model = Teams
        fields = ['id', 'name','country_name', 'stadiums_name', 'logo', 'founded']
        
class TeamsMiniSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Teams
        fields = ['id', 'name', 'logo', 'founded']
              
class LeaguesSeasonsTeamsSerializer(serializers.ModelSerializer):
    
    # team_photo = serializers.URLField(source='team_id.logo')
    id = serializers.IntegerField(source='leagues_id.id')
    name = serializers.CharField(source='leagues_id.name')
    logo = serializers.CharField(source='leagues_id.logo')
    rank = serializers.IntegerField(source='leagues_id.rank')
    country = serializers.CharField(source='leagues_id.country_id.name')
    class Meta:
        model = LeaguesSeasonsTeams
        fields = ['id','name','country','rank','logo']
                
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["teams"] = TeamsMiniSerializer(instance.team_id.all(), many=True).data      
        return rep
    
class PlayersSerializer(serializers.ModelSerializer):
    
    country_name = serializers.CharField(source='country_id.name')
    team_name = serializers.CharField(source='country_id.name')
   
    class Meta:
        model = Players
        fields = ['id', 'name','country_name', 'team_name', 'age', 'height', 'weight', 'photo', 'position', 'injured']
        
        
# class PlayerStatisticsSerializer(serializers.ModelSerializer):
       
#     class Meta:
#         model = PlayerStatistics
#         fields = '__all__'