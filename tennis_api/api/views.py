from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response

from tennis.models import Player, Tourney, Match

from .serializers import PlayerSerializer, TourneySerializer, MatchSerializer


@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'player': '/api/player/<str:pk>',
        'player-matches': '/api/player/<str:pk>/matches/',
        'player-list': '/api/players/',
        'tourney': '/api/tourney/<str:pk>',
        'tourney-matches': '/api/tourney/<str:pk>/matches/',
        'tourney-list': '/api/tourneys/',
        'match': '/api/match/<str:pk>',
        'match-list': '/api//matches/',
    }
    return Response(api_urls)


@api_view(['GET'])
def player(request, pk):
    player = Player.objects.get(id=pk)
    return Response(PlayerSerializer(player).data)


@api_view(['GET'])
def player_matches(request, pk):
    player = Player.objects.get(id=pk)
    return Response(
        {
            'won_matches': MatchSerializer(player.w_match.all(), many=True).data,
            'lost_matches': MatchSerializer(player.l_match.all(), many=True).data
        }
    )


@api_view(['GET'])
def players(request):
    search = request.query_params.get('search', None)
    offset = int(request.query_params.get('offset', 0))
    limit = int(request.query_params.get('limit', 20))
    order_by = request.query_params.get('order_by', 'ranking')
    if search:
        players = Player.objects.filter(name__icontains=search)
    else:
        players = Player.objects.filter(ranking__isnull=False)
    return Response(PlayerSerializer(players.order_by(order_by)[offset:offset + limit], many=True).data)


@api_view(['GET'])
def tourney(request, pk):
    tourney = Tourney.objects.get(id=pk)
    return Response(TourneySerializer(tourney).data)


@api_view(['GET'])
def tourney_matches(request, pk):
    matches = Match.objects.filter(tourney_id=pk).order_by('-match_num')
    return Response(MatchSerializer(matches, many=True).data)


@api_view(['GET'])
def tourneys(request):
    search = request.query_params.get('search', None)
    offset = int(request.query_params.get('offset', 0))
    limit = int(request.query_params.get('limit', 20))
    if search:
        tourneys = Tourney.objects.filter(name__icontains=search)
    else:
        tourneys = Tourney.objects.all()
    return Response(TourneySerializer(tourneys.order_by('-id')[offset:offset + limit], many=True).data)


@api_view(['GET'])
def match(request, pk):
    match = Match.objects.get(id=pk)
    return Response(MatchSerializer(match).data)


@api_view(['GET'])
def matches(request):
    search = request.query_params.get('search', None)
    offset = int(request.query_params.get('offset', 0))
    limit = int(request.query_params.get('limit', 20))
    if search:
        matches = Match.objects.filter(
            Q(l_player__name__icontains=search) |
            Q(w_player__name__icontains=search) |
            Q(tourney__name__icontains=search)
        )
    else:
        matches = Match.objects.filter()
    return Response(MatchSerializer(matches.order_by('-id')[offset:offset + limit], many=True).data)
