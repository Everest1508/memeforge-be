from rest_framework import serializers
from .models import ImageCategory, Image

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'title', 'short_description', 'image', 'uploaded_at']

class ImageCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ImageCategory
        fields = ['id', 'name', 'slug']
