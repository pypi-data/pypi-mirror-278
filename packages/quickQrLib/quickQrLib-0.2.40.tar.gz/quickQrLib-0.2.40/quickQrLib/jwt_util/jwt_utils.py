import requests
import base64
import json
import time
import jwt
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.state import token_backend
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken, UntypedToken


class CustomJWTAuthentication(JWTAuthentication):
    """
    Custom authentication class that extends JWTAuthentication.
    This class handles the authentication process using JWT tokens.
    """

    def __init__(self, *args, **kwargs):
        self.url = kwargs.pop('url', None)
        super().__init__(*args, **kwargs)

    def authenticate(self, request):
        """
        Authenticates the request using JWT token.
        
        Args:
            request (HttpRequest): The request object.
            url (str): The URL to send the token for validation.
        
        Returns:
            tuple: A tuple containing the authenticated user and the raw token.
        
        Raises:
            AuthenticationFailed: If the authorization credentials were not provided or the token is invalid.
        """
        print(f"Request in CustomJWTAuthentication: {request} | URL: {self.url}")
        header = self.get_header(request)
        if header is None:
            raise AuthenticationFailed("Authorization credentials were not provided")

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            raise AuthenticationFailed("Authorization credentials were not provided")
        
        try:
            validated_token = token_backend.decode(raw_token, verify=True)
        except Exception as e:
            raise InvalidToken(e) from e
       
        response = requests.post(url, data={'token': raw_token})
        if response.status_code == 200:
            # return self.get_user(response.json()), raw_token
            return super().authenticate(request)
        else:
            raise AuthenticationFailed("Invalid token")

class TokenUtils:
    def __init__(self, *args, **kwargs):
        self.url = kwargs.pop('url', None)
        super().__init__(*args, **kwargs)
    
    @classmethod
    def get_tokens_for_user(cls, user):        
        data = {
            'email': user.email,            
            'user_id': user.id,
            'emp_id': user.emp_id
        }
        try:
            response = requests.post(cls.url, data=data)
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
    def decode_token(cls, token):
        try:
            print(f"\nDecoding token for {token}\n")
            # Example decoding logic, adjust based on actual implementation
            parts = token.split(',')
            if len(parts) != 3:
                print(f"Invalid token format: {len(parts)}")
                return "Invalid token format"
            # Decode the token using the appropriate method, e.g., jwt.decode
            try:
                decoded_token = jwt.decode(token, options={"verify_signature": False})
            except Exception as e:
                print(f"Error decoding token: {e}")
                return None
            print(f"Decoded token: {decoded_token}")
            return decoded_token
        except (jwt.DecodeError, IndexError) as e:
            return f"Invalid token: {e}"
        except Exception as e:
            return f"Error decoding token: {e}"
        
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
