from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ImageCategory, Image, Template
from .serializers import ImageCategorySerializer, ImageSerializer

# List all categories with their images
class ImageCategoryListView(generics.ListAPIView):
    queryset = ImageCategory.objects.all().order_by('-order')
    serializer_class = ImageCategorySerializer
    pagination_class = None

# List images of a specific category
class CategoryImageListView(generics.ListAPIView):
    serializer_class = ImageSerializer
    pagination_class = None
    
    def get_queryset(self):
        slug = self.kwargs['slug']
        return Image.objects.filter(category__slug=slug)

    def get_serializer_context(self):
        return {'request': self.request}



from .serializers import TemplateSerializer

class TemplateListView(APIView):
    def get(self, request):
        templates = Template.objects.all()
        serializer = TemplateSerializer(templates, many=True)
        return Response(serializer.data)