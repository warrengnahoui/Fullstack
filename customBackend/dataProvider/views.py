from django.shortcuts import render
from .models import Player, Performance
from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from .renderers import ApiRenderer
from .serializers import (
    PlayerSerializer,
    PerformanceSerializer,
    BlankSerializer
)



# Create your views here.


class PlayerList(generics.ListCreateAPIView):
    serializer_class = PlayerSerializer
    renderer_classes = (ApiRenderer,)
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Player.objects.all()

    def perform_create(self, serializer):
        return serializer.save()

    def get_queryset(self):
        return self.queryset.filter()


class PlayerDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PlayerSerializer
    renderer_classes = (ApiRenderer,)
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Player.objects.all()
    lookup_field = "id"

    def perform_create(self, serializer):
        return serializer.save()

    def get_queryset(self):
        return self.queryset.filter()



class PerformanceList(generics.ListCreateAPIView):
    serializer_class = PerformanceSerializer
    renderer_classes = (ApiRenderer,)
    queryset = Performance.objects.all()

    def perform_create(self, serializer):
        return serializer.save()

    def get_queryset(self):
        return self.queryset.filter()


class PerformanceDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PerformanceSerializer
    renderer_classes = (ApiRenderer,)
    queryset = Performance.objects.all()
    lookup_field = "id"

    def perform_create(self, serializer):
        return serializer.save()

    def get_queryset(self):
        return self.queryset.filter()


class GetAveragePerformance(generics.GenericAPIView):
    serializer_class = BlankSerializer
    renderer_classes = (ApiRenderer,)
    queryset = Performance.objects.all()

    def get(self, request):
        try:
            response = {}
            all_players = Player.objects.all();
            for player in all_players:
                last_five_performances = self.queryset.filter(player=player.id).order_by('-created_at')[:5]
                summary = {
                    "points": 0,
                    "assists": 0,
                    "rebounds": 0
                }
                if(len(last_five_performances)):
                    avg = len(last_five_performances)
                    tmp = {
                        "points": 0,
                        "assists": 0,
                        "rebounds": 0
                    }
                    for performance in last_five_performances:
                        tmp["points"] += performance.stats["points"]
                        tmp["assists"] += performance.stats["assists"]
                        tmp["rebounds"] += performance.stats["rebounds"]
                    summary["points"] = tmp["points"] / avg
                    summary["assists"] = tmp["assists"] / avg
                    summary["rebounds"] = tmp["rebounds"] / avg
                    response[player.id] = summary;
                else:
                    response[player.id] = summary;
            return Response(response, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Something went wrong when parsing merge request event'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)