from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from dotenv import load_dotenv
from .models import MemeforgeUser
load_dotenv()
from .utils import decrypt_token


class CreamTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Cream "):
            return None  # Let DRF try other auth classes

        encrypted_token = auth_header.split(" ")[1]

        try:
            decrypted_data = self.decrypt_token(encrypted_token)
        except Exception as e:
            raise AuthenticationFailed(f"Invalid token: {str(e)}")

        # Suppose decrypted_data is a JSON string with an email field
        import json
        try:
            user_info = json.loads(decrypted_data)
            email = user_info.get("email")
        except Exception:
            raise AuthenticationFailed("Malformed decrypted data.")

        if not email:
            raise AuthenticationFailed("No email in token.")

        try:
            user = MemeforgeUser.objects.get(email=email)
        except MemeforgeUser.DoesNotExist:
            raise AuthenticationFailed("User not found.")

        return (user, None)