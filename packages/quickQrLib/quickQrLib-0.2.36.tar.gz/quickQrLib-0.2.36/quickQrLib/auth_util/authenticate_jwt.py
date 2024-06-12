from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.state import token_backend
from rest_framework.exceptions import AuthenticationFailed
from auth_n_auth.models import AppUser

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            raise AuthenticationFailed("Authorization credentials were not provided")

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            raise AuthenticationFailed("Authorization credentials were not provided")
        try:
            validated_token = token_backend.decode(raw_token, verify=True)
        except Exception as e:
            raise InvalidToken(e)

        try:
            # Retrieve the user using the `emp_id`
            user = AppUser.objects.get(id=id)
        except AppUser.DoesNotExist:
            raise AuthenticationFailed("User not found")

        return (user, validated_token)  # Return the user and token