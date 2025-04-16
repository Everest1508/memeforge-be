from rest_framework import generics
from .models import ImageCategory, Image
from .serializers import ImageCategorySerializer, ImageSerializer

# List all categories with their images
class ImageCategoryListView(generics.ListAPIView):
    queryset = ImageCategory.objects.all()
    serializer_class = ImageCategorySerializer

# List images of a specific category
class CategoryImageListView(generics.ListAPIView):
    serializer_class = ImageSerializer

    def get_queryset(self):
        slug = self.kwargs['slug']
        return Image.objects.filter(category__slug=slug)
