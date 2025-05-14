from rest_framework import serializers
from .models import Roadmap,RoadmapImage

class RoadmapImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = RoadmapImage
        fields = ['id', 'image', 'caption', 'uploaded_at']

class RoadmapSerializer(serializers.ModelSerializer):
    images = RoadmapImageSerializer(many=True, read_only=True)

    class Meta:
        model = Roadmap
        fields = ['id', 'title', 'image', 'slug', 'description', 'order', 'created_at', 'updated_at', 'images']
