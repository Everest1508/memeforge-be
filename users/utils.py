import os
from base64 import b64decode
from dotenv import load_dotenv
from Crypto.Cipher import AES

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
