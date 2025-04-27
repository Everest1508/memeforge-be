from django.urls import path
from .views import UserSubmissionListCreateView, CheckUserSubmissionView

urlpatterns = [
    # Add the API endpoint for listing and creating submissions
    path('submissions/', UserSubmissionListCreateView.as_view(), name='user_submission_list_create'),
    path('check-submission/', CheckUserSubmissionView.as_view(), name='check-submission'),
]
