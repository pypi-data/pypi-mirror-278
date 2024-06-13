import os
import sys
from time import sleep
from cryptography.fernet import Fernet

def generate_key():
    a = Fernet.generate_key()

    #send a to CNC with app name, ip, and app ver


    return Fernet.generate_key()

def get_key():
    key = os.getenv('DATA_KEY')
    if not key:
        key = generate_key()
        print(f"Generated new key: {key.decode()} Set this as DATA_KEY env var.")
        sleep(90)
        sys.exit()
    return key


def encrypt_data(data):
   key = get_key()
   f = Fernet(key)
   if isinstance(data, str):
       data = data.encode()
   elif not isinstance(data, bytes):
       data = str(data).encode()
   
   return f.encrypt(data)

def decrypt_data(encrypted_data):
   key = os.getenv('ENCRYPTION_KEY')
   if not key:
    raise ValueError("ENCRYPTION_KEY not set. Cannot decrypt data.")
   f = Fernet(key)
   decrypted = f.decrypt(encrypted_data)
   return decrypted.decode()
