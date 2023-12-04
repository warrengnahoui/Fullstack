from django.urls import path
from .views import (
    PerformanceList,
    PerformanceDetail,
    GetAveragePerformance
)

urlpatterns = [
    path('', PerformanceList.as_view(), name="performance_list"),
    path('<str:id>', PerformanceDetail.as_view(), name="performance_detail"),
    path('statistics/', GetAveragePerformance.as_view(), name='statistics')
]