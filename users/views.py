from django.http import JsonResponse
from users.utils import decrypt_token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import MemeforgeUser
from .utils import decrypt_token
from .authentication import CreamTokenAuthentication

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
    authentication_classes = [CreamTokenAuthentication]

    def post(self, request):
        user = request.user

        # Check if user already exists in your custom model
        existing_user = MemeforgeUser.objects.filter(email=user.email).first()

        if existing_user:
            return Response({'message': 'ok'}, status=status.HTTP_200_OK)

        # Create a new user profile (this assumes the auth token had extra info you stored on user)
        MemeforgeUser.objects.create(
            email=user.email,
            profile_picture=request.data.get("profile_picture"),
            twitter_x_account=request.data.get("x_account"),
        )

        return Response({'message': 'ok'}, status=status.HTTP_200_OK)
