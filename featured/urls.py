from django.urls import path, re_path
from .views import (
    FeaturedListView, TabiPayCardListView, 
    RandomMCQByCategory, CheckMCQAnswer, serve_tabipay_image,
    RandomOrCreateTabiPayOverlay, CheckTabiPayCreation
)

urlpatterns = [
    path('api/featured/', FeaturedListView.as_view(), name='featured-list'),
    path('api/tabipay-cards/', TabiPayCardListView.as_view(), name='tabipay-list'),
    re_path(r'^api/tabipay-cards/(?P<uuid>[0-9a-f-]+)\.png$', serve_tabipay_image, name='tabipay-card'),
    path('api/mcq/<int:category_id>/random/', RandomMCQByCategory.as_view(), name='mcq-random'),
    path('api/mcq/check/', CheckMCQAnswer.as_view(), name='mcq-check'),
    path('api/tabipay/', RandomOrCreateTabiPayOverlay.as_view(), name="tabipay_random_or_create"),
    path('api/tabipay/check/', CheckTabiPayCreation.as_view(), name='check_tabipay_creation'),
]
