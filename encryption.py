from cryptography.fernet import Fernet #print(Fernet.generate_key().decode())
from config import Config

cipher = Fernet(Config.ENCRYPTION_KEY.encode())

def encrypt_password(password):
    return cipher.encrypt(password.encode())

def decrypt_password(token):
    try:
        return cipher.decrypt(token).decode()
    except Exception:
        return "[Invalid or corrupted password]"

