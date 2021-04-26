from rest_framework import serializers

from tennis.models import Player, Tourney, Match


class MatchSerializer(serializers.ModelSerializer):
    w_name = serializers.CharField(source='w_player.name', read_only=True)
    l_name = serializers.CharField(source='l_player.name', read_only=True)
    tourney_name = serializers.CharField(source='tourney.name', read_only=True)

    class Meta:
        model = Match
        fields = '__all__'


class TourneySerializer(serializers.ModelSerializer):
    class Meta:
        model = Tourney
        fields = '__all__'


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'
