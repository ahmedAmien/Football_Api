from rest_framework import serializers
from .models import Leagues

class LeaguesSerializer(serializers.ModelSerializer):
    country_name = serializers.CharField(source='country_id.name')
    
    class Meta:
        model = Leagues
        fields = ['id', 'name','country_name','rank', 'logo']