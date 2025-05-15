from django.http import JsonResponse
from users.utils import decrypt_token

# Create your views here.

def decode_message(request):
    token = request.GET.get('token')
    print(token)
    if not token:
        return JsonResponse({'error': 'Missing token parameter'}, status=400)

    try:
        data = decrypt_token(token)
        return JsonResponse({'success': True, 'data': data})
    except Exception as e:
        return JsonResponse({'error': 'Invalid token or decryption failed'}, status=400)
    
# views.py

import json
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import MemeforgeUser
from .serializers import MemeforgeUserSerializer
from .utils import decrypt_token  # Assuming decrypt_token is in utils.py

class StoreUserProfileView(APIView):
    """
    API to decrypt the encrypted user profile data, check if the user exists by email,
    and save it to the database if it doesn't exist.
    """
    
    def post(self, request, *args, **kwargs):
        encrypted_data = request.data.get('encrypted_data')

        if not encrypted_data:
            return Response({'error': 'No encrypted data provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Decrypt the data
            decrypted_data = decrypt_token(encrypted_data)

            # Convert decrypted JSON string back to dictionary
            decrypted_dict = json.loads(decrypted_data)

            # Check if the user already exists by email
            user = MemeforgeUser.objects.filter(email=decrypted_dict['email']).first()

            if user:
                return Response({'message': 'ok'}, status=status.HTTP_200_OK)

            user_profile = MemeforgeUser.objects.create(
                email=decrypted_dict['email'],
                profile_picture=decrypted_dict['profile_picture'],
                twitter_x_account=decrypted_dict['x_account']
            )

            return Response({'message': 'ok'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
