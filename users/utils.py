import json
import os
from base64 import b64decode
from dotenv import load_dotenv
from Crypto.Cipher import AES
from .models import MemeforgeUser

# Load .env variables
load_dotenv()

# Load AES key and IV from .env
key = os.getenv("AES_KEY").encode('utf-8')
iv = os.getenv("AES_IV").encode('utf-8')

def decrypt_token(encrypted_text: str) -> str:
    """
    Decrypts an AES-encrypted token using the key and IV from .env.

    Args:
        encrypted_text (str): The Base64 encoded encrypted string.

    Returns:
        str: The decrypted plaintext message.
    """
    # Decrypt
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(b64decode(encrypted_text))

    # Remove PKCS7 padding
    pad_len = decrypted[-1]
    decrypted_text = decrypted[:-pad_len].decode('utf-8')
    return decrypted_text


def get_user(request):
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Cream "):
        return (None, None) 

    encrypted_token = auth_header.split(" ")[1]

    try:
        decrypted_data = decrypt_token(encrypted_token)
    except Exception as e:
        return (None, None)

    try:
        user_info = json.loads(decrypted_data)
        email = user_info.get("email")
    except Exception:
        return (None, None)

    if not email:
        return (None, None)
    

    try:
        user = MemeforgeUser.objects.get(email=email)
    except MemeforgeUser.DoesNotExist:
        return (None, None)

    return (user, None)