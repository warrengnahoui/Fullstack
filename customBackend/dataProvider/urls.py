from django.urls import path
from .views import (
    PlayerList,
    PlayerDetail,
)

urlpatterns = [
    path('', PlayerList.as_view(), name="player_list"),
    path('<str:id>', PlayerDetail.as_view(), name="player_detail"),
]