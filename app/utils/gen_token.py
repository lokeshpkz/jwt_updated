import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import json
from colorama import Fore
import time
import threading

# Global session for connection pooling/keep-alive
session = requests.Session()

# Thread-safe in-memory cache for Garena tokens
# Key: (uid, password), Value: (token_data, expire_time)
_token_cache = {}
_cache_lock = threading.Lock()


def get_token(password, uid):
    cache_key = (uid, password)
    now = time.time()
    
    # Try retrieving from cache first
    with _cache_lock:
        if cache_key in _token_cache:
            token_data, expire_time = _token_cache[cache_key]
            if now < expire_time:
                return token_data
            else:
                del _token_cache[cache_key]

    url = "https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant"
    headers = {
        "Host": "100067.connect.garena.com",
        "User-Agent": "GarenaMSDK/4.0.19P4 (Redmi Note 10; Android 12; en;IN;)",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }
    data = {
        "uid": uid,
        "password": password,
        "response_type": "token",
        "client_type": "2",
        "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        "client_id": "100067",
    }
    try:
        response = session.post(url, headers=headers, data=data, verify=False, timeout=10)
        if response.status_code != 200:
            print(Fore.RED + f"Failed to retrieve token for UID {uid}: {response.text}")
            return None
        
        token_data = response.json()
        
        # Cache the token for 2 hours (7200 seconds)
        with _cache_lock:
            _token_cache[cache_key] = (token_data, now + 7200)
            
        return token_data
    except Exception as e:
        print(Fore.RED + f"Error getting token for UID {uid}: {e}")
        return None


def encrypt_message(key, iv, plaintext):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = pad(plaintext, AES.block_size)
    encrypted_message = cipher.encrypt(padded_message)
    return encrypted_message


def load_tokens(file_path, limit=None):
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            tokens = list(data.items())
            if limit is not None:
                tokens = tokens[:limit]  # Set token limit
            return tokens
    except Exception as e:
        print(Fore.RED + f"Failed to load tokens: {e}")
        return []
