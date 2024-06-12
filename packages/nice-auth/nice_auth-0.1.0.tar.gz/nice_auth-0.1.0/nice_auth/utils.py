import hmac
import hashlib
import base64
import json
import random
import string
from datetime import datetime

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def encrypt_aes(data, key, iv):
    secure_key = key.encode()
    iv = iv.encode()
    json_data_str = json.dumps(data)  # Convert the dictionary to a JSON string
    cipher = AES.new(secure_key, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(pad(json_data_str.encode(), AES.block_size))
    enc_data = base64.b64encode(encrypted).decode()
    return enc_data

def hmac_sha256(secret_key, message):
    hmac256 = hmac.new(secret_key.encode(), message.encode(), hashlib.sha256).digest()
    integrity_value = base64.b64encode(hmac256).decode()
    return integrity_value

def generate_request_no():
    current_timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    return f"{current_timestamp}{random_str}"

def decrypt_aes(data, key, iv):
    cipher = AES.new(key.encode(), AES.MODE_CBC, iv.encode())
    encrypted_data = base64.b64decode(data)
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    return decrypted_data.decode()
