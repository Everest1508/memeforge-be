from django.urls import path
from .views import ImageCategoryListView, CategoryImageListView, TemplateListView

urlpatterns = [
    path('categories/', ImageCategoryListView.as_view(), name='category-list'),
    path('categories/<slug:slug>/images/', CategoryImageListView.as_view(), name='images-by-category'),
    path('templates/', TemplateListView.as_view(), name='template-list'),
]
