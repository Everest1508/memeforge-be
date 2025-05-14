from django.urls import path
from .views import (
    FeaturedListView, TabiPayCardListView, 
    RandomMCQByCategory, CheckMCQAnswer
)

urlpatterns = [
    path('api/featured/', FeaturedListView.as_view(), name='featured-list'),
    path('api/tabipay-cards/', TabiPayCardListView.as_view(), name='tabipay-list'),
    path('api/mcq/<int:category_id>/random/', RandomMCQByCategory.as_view(), name='mcq-random'),
    path('api/mcq/check/', CheckMCQAnswer.as_view(), name='mcq-check'),
]
