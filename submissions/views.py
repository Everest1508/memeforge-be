from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from datetime import date
from .models import UserSubmission
from .serializers import UserSubmissionSerializer
from users.utils import decrypt_token
import json

# View to handle listing and creating User Submissions
class UserSubmissionListCreateView(generics.ListCreateAPIView):
    queryset = UserSubmission.objects.all()
    serializer_class = UserSubmissionSerializer

    def perform_create(self, serializer):
        today = date.today()

        email = serializer.validated_data.get('email')
        if UserSubmission.objects.filter(email=email, created_at__date=today).exists():
            raise ValidationError(f"You have already submitted a meme today, {email}.")

        # If no submission exists, proceed with creating a new one
        serializer.save()


    def create(self, request, *args, **kwargs):
        """
        Override the create method to decrypt the request and return an encrypted response.
        """
        try:
            # Step 1: Decrypt incoming AES-encrypted data
            encrypted_payload = request.body
            decrypted_data = decrypt_token(encrypted_payload)

            # Convert decrypted JSON string to Python dict
            parsed_data = json.loads(decrypted_data)

            # Step 2: Validate and create submission
            serializer = self.get_serializer(data=parsed_data)
            serializer.is_valid(raise_exception=True)

            try:
                self.perform_create(serializer)
                message = "Meme successfully submitted!"
            except ValidationError:
                message = "You already submitted today, but the meme is accepted."

            # Step 3: Encrypt the response message
            encrypted_response ={"message": message}
            return Response(encrypted_response, status=status.HTTP_200_OK)

        except Exception as e:
            error_response = {"error": "Invalid or corrupted request."}
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)


class CheckUserSubmissionView(generics.GenericAPIView):
    """
    API endpoint to check if the user has already submitted a meme today.
    """
    def get(self, request, *args, **kwargs):
        # Get the email from query parameters
        email = request.query_params.get('email')

        if not email:
            return Response(
                {"message": "Email parameter is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get the current date
        today = date.today()

        # Check if a submission already exists for this email today
        if UserSubmission.objects.filter(email=email, created_at__date=today).exists():
            return Response(
                {"message": "You have already submitted a meme today."},
                status=status.HTTP_200_OK
            )
        
        # If no submission exists, return a success message
        return Response(
            {"message": "You have not submitted a meme today."},
            status=status.HTTP_200_OK
        )