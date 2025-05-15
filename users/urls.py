from django.urls import path
from . import views

urlpatterns = [
    path('api/decode-message/', views.decode_message),
    path('api/user-token/', views.StoreUserProfileView.as_view()),
]