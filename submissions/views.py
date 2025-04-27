from rest_framework import generics
from .models import UserSubmission
from .serializers import UserSubmissionSerializer

# View to handle listing and creating User Submissions
class UserSubmissionListCreateView(generics.ListCreateAPIView):
    queryset = UserSubmission.objects.all()
    serializer_class = UserSubmissionSerializer
