from cryptography.fernet import Fernet

key = Fernet.generate_key()  # Store this securely in production
cipher = Fernet(key)

def encrypt_password(password):
    return cipher.encrypt(password.encode())

def decrypt_password(token):
    return cipher.decrypt(token).decode()