from rest_framework_simplejwt.tokens import AccessToken, RefreshToken, UntypedToken
import requests
import base64
import json
import time
import redis

redis_host = '127.0.0.1'
redis_port = '30001'
redis_db= 0

# Create the connection
redis_conn = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)

class TokenUtils:    
    @classmethod
    def get_tokens_for_user_inline(cls, user):
        token = RefreshToken.for_user(user)
        return str(token), str(token.access_token)        
        
    @classmethod
    def get_tokens_for_user(cls, username, password):
        token_obtain_url = 'http://localhost:8000/find-it/token/'  # take out to env file
        data = {
            'email': username,
            'password': password
        }
        try:
            response = requests.post(token_obtain_url, data=data)
            response_data = response.json()
            access_token = response_data.get('access', None)
            refresh_token = response_data.get('refresh', None)

            if access_token and refresh_token:
                return access_token, refresh_token
            else:
                return None, None
        except Exception as e:
            print(f'Token Obtain Error: {e}')
            return None, None
        
    @classmethod
    def refresh_access_token(cls, refresh_token):
        try:
            token = RefreshToken(refresh_token)
            new_access_token = str(token.access_token)
            return new_access_token
        except Exception as e:
            print(f'Token Refresh Error: {e}')
            return None
    
    @classmethod
    def verify_token(cls, access_token):
        try:
            token = AccessToken(access_token)
            success, info = token.verify()
            return success, info
        except Exception as e:
            print(f'Token Verify Error: {e}')
            return False, str(e)
        
    @classmethod
    def decode_token(cls, access_token):
        payload = access_token.split('.')[1]
        payload += '=' * (-len(payload) % 4)
        decoded_payload = base64.b64decode(payload)
        payload_json = json.loads(decoded_payload)
        return payload_json
    
    @classmethod
    def get_expiry(cls, jwt_token):
        payload = jwt_token.split('.')[1]
        # Add padding to fix incorrect token length
        payload += '=' * (-len(payload) % 4)
        decoded_payload = base64.b64decode(payload)
        payload_json = json.loads(decoded_payload)
        return payload_json['exp']
    
    @classmethod
    def is_token_expired(cls, jwt_token):
        expiry = cls.get_expiry(jwt_token)
        return time.time() > expiry
    
    @classmethod
    def validate_token(cls, token):
        try:
            token = UntypedToken(token)
            return True
        except Exception as e:
            print(f"Token validation error: {e}")
            return False

    @classmethod
    def check_blacklist(cls, token):
        # print(f"\nChecking blacklist for token\n")
        decoded_token = cls.decode_token(token)
        if decoded_token:
            jti = decoded_token.get('jti', None)
            jti = jti.encode('utf-8')
            redis_list = cls.get_blacklist(token)
            if jti in redis_list:
                return False
            if jti:               
                return redis_conn.get(jti) is None
            else:
                return None
        return None
        # return True

    @classmethod
    def get_blacklist(cls, token):
        list_redis = redis_conn.keys('*')
        decoded_list = []
        for key in list_redis:
            key = key.decode('utf-8')
            decoded_list.append(key)
        return decoded_list
