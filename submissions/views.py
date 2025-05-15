from datetime import date
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import UserSubmission
from .serializers import UserSubmissionSerializer
from users.authentication import CreamTokenAuthentication


class UserSubmissionListCreateView(generics.ListCreateAPIView):
    queryset = UserSubmission.objects.all()
    serializer_class = UserSubmissionSerializer
    authentication_classes = [CreamTokenAuthentication]

    def perform_create(self, serializer):
        today = date.today()
        email = serializer.validated_data.get('email')

        if UserSubmission.objects.filter(email=email, created_at__date=today).exists():
            raise ValidationError(f"You have already submitted a meme today, {email}.")
        serializer.save()

    def create(self, request, *args, **kwargs):
        try:
            # Auth class sets request.user (from decrypted token)
            email = getattr(request.user, 'email', None)
            if not email:
                raise ValueError("Email missing from token")

            # Add email into incoming request data (frontend doesn't send it)
            data = request.data.copy()
            data['email'] = email

            # Validate and create submission
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)

            try:
                self.perform_create(serializer)
                message = "Meme successfully submitted!"
            except ValidationError:
                message = "You already submitted today, but the meme is accepted."

            return Response({"message": message}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



class CheckUserSubmissionView(generics.GenericAPIView):
    """
    API endpoint to check if the user has already submitted a meme today.
    """
    authentication_classes = [CreamTokenAuthentication]

    def get(self, request, *args, **kwargs):
        try:
            email = request.user.email
            if not email:
                raise ValueError("Email not found in decrypted payload.")

            today = date.today()
            has_submitted = UserSubmission.objects.filter(email=email, created_at__date=today).exists()

            message = "You have already submitted a meme today." if has_submitted else "You have not submitted a meme today."
            encrypted_response = {"message": message}
            return Response({"data": encrypted_response}, status=status.HTTP_200_OK)

        except Exception as e:
            encrypted_error = {"error": "Invalid or corrupted request."}
            return Response({"data": encrypted_error}, status=status.HTTP_400_BAD_REQUEST)
