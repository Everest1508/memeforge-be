from django.urls import path
from .views import UserSubmissionListCreateView

urlpatterns = [
    # Add the API endpoint for listing and creating submissions
    path('submissions/', UserSubmissionListCreateView.as_view(), name='user_submission_list_create'),
]
