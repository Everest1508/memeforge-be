from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from datetime import date
from .models import UserSubmission
from .serializers import UserSubmissionSerializer

# View to handle listing and creating User Submissions
class UserSubmissionListCreateView(generics.ListCreateAPIView):
    queryset = UserSubmission.objects.all()
    serializer_class = UserSubmissionSerializer

    def perform_create(self, serializer):
        # Get the current date
        today = date.today()

        # Check if a submission already exists for this email today
        email = serializer.validated_data.get('email')
        if UserSubmission.objects.filter(email=email, created_at__date=today).exists():
            raise ValidationError(f"You have already submitted a meme today, {email}.")

        # If no submission exists, proceed with creating a new one
        serializer.save()

    def create(self, request, *args, **kwargs):
        """
        Override the create method to catch the ValidationError and return it
        as a proper response.
        """
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            return Response(
                {"detail": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
