from django.http import JsonResponse
from users.utils import decrypt_token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import MemeforgeUser
from .utils import decrypt_token
import json

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
    


class StoreUserProfileView(APIView):
    def post(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Cream "):
            return Response({'error': 'Missing or invalid Authorization header'}, status=status.HTTP_401_UNAUTHORIZED)

        encrypted_token = auth_header.split(" ")[1]

        try:
            decrypted_data = decrypt_token(encrypted_token)
            user_info = json.loads(decrypted_data)
            email = user_info.get("email")
        except Exception as e:
            return Response({'error': f'Token decryption failed: {str(e)}'}, status=status.HTTP_401_UNAUTHORIZED)

        if not email:
            return Response({'error': 'Email not found in decrypted token'}, status=status.HTTP_401_UNAUTHORIZED)

        # Check if user already exists
        existing_user = MemeforgeUser.objects.filter(email=email).first()
        if existing_user:
            return Response({'message': 'ok'}, status=status.HTTP_200_OK)

        # Create a new user
        MemeforgeUser.objects.create(
            email=email,
            profile_picture=user_info.get("image")
        )
        return Response({'message': 'ok'}, status=status.HTTP_200_OK)