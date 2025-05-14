from rest_framework import serializers
from .models import ImageCategory, Image

class ImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ['id', 'title', 'short_description', 'image', 'uploaded_at']

    def get_image(self, obj):
        request = self.context.get('request')
        if request:
            url = request.build_absolute_uri(obj.image.url)
            # Just in case the proxy isn't fully respected:
            return url.replace("http://", "https://")
        return obj.image.url


class ImageCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ImageCategory
        fields = ['id', 'name', 'slug']

# templates/serializers.py

from rest_framework import serializers
from .models import Template

class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = ['id', 'name', 'image', 'short_description', 'uploaded_at']
