from django.urls import path
from .views import RoadmapListAPIView

urlpatterns = [
    path('api/roadmap/', RoadmapListAPIView.as_view(), name='roadmap-list'),
]
