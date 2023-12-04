from rest_framework import serializers
from .models import Player, Performance

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields=['id', 'name', 'team', 'position', 'number', 'picture']


class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields=['id', 'match_name', 'player', 'stats']
    
    def validate(self, attrs):
        stats = attrs.get('stats')
        if not stats:
            raise serializers.ValidationError('No stats provided')
        if not isinstance(stats, dict):
            raise serializers.ValidationError('Stats must be a dictionary')
        if not stats.get('points') or not stats.get('assists') or not stats.get('rebounds'):
            raise serializers.ValidationError('Missing keys in stats. This keys (points, assists, rebounds) are required')
        return attrs


class BlankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields=[]