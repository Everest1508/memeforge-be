from django.urls import path
from .views import (
    FeaturedListView, TabiPayCardListView, 
    RandomMCQByCategory, CheckMCQAnswer, serve_tabipay_image,
    RandomOrCreateTabiPayOverlay
)

urlpatterns = [
    path('api/featured/', FeaturedListView.as_view(), name='featured-list'),
    path('api/tabipay-cards/', TabiPayCardListView.as_view(), name='tabipay-list'),
    path('api/tabipay-cards/<uuid>/', serve_tabipay_image, name='tabipay-card'),
    path('api/mcq/<int:category_id>/random/', RandomMCQByCategory.as_view(), name='mcq-random'),
    path('api/mcq/check/', CheckMCQAnswer.as_view(), name='mcq-check'),
    path('api/tabipay/', RandomOrCreateTabiPayOverlay.as_view(), name="tabipay_random_or_create"),
]
