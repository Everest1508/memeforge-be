from rest_framework import generics
from .models import Roadmap
from .serializers import RoadmapSerializer

class RoadmapListAPIView(generics.ListAPIView):
    queryset = Roadmap.objects.all().order_by('order')
    serializer_class = RoadmapSerializer
