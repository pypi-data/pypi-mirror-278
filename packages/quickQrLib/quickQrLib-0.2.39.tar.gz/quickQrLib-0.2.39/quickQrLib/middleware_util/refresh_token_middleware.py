from django.http import HttpResponse
from tokenutils import TokenUtils

from django.utils.deprecation import MiddlewareMixin
class TokenRefreshMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
        self.count = 0
        self.token_generator = TokenUtils()
        self.ignore_paths = ['/find-it/token/refresh/', '/find-it/token/', '/find-it/token/verify/', '/find-it/login/', '/find-it/user_management/login/', '/login/','/metrics', '/metrics/', '/find-it/forgot-password/']

    def process_request(self, request):
        self.count += 1
        print(f"Request #{self.count} - {request.path}")
        if request.path in self.ignore_paths:
            return self.get_response(request)
        response, continue_on = self.refresh_access_token(request)
        if continue_on and response != "Access Token is still valid":
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {response}'   
            return self.get_response(request)
        else:
            if response == "Access Token is still valid":
                return self.get_response(request)
            return HttpResponse({"ERROR:", response}, status=401)
        
    def refresh_access_token(self, request):
        access_token = request.META.get('HTTP_AUTHORIZATION', None)
        refresh_token = request.META.get('HTTP_REFRESH_TOKEN', None)   
        if refresh_token:
            not_blacklisted = self.token_generator.check_blacklist(refresh_token)
            #returns True on token not blacklisted, False on token blacklisted, None on token not found
            if not not_blacklisted:
                return "ERROR: Refresh Token is blacklisted", False
            if not_blacklisted is None:
                return "ERROR: Refresh Token is invalid", False
            # token_expired = self.token_generator.is_token_expired(refresh_token)
            token_valid = self.token_generator.validate_token(refresh_token)
            if not token_valid:
                return "ERROR: Refresh Token has expired", False # THIS TRIGGERS A FORCED LOGOUT
        else:
            return "No refresh token", False
        if access_token:            
            not_blacklisted = self.token_generator.check_blacklist(access_token)
            #returns True on token not blacklisted, False on token blacklisted, None on token not found
            if not not_blacklisted:
                return "ERROR: Token is blacklisted", False
            if not_blacklisted is None:
                return "ERROR: Token is invalid", False
            token_expired = self.token_generator.is_token_expired(access_token)
            if token_expired:
                print(f"Access Token is expired")
                access_token = self.token_generator.refresh_access_token(refresh_token)
                if access_token:
                    print("Token Refreshed")
                    return access_token, True
                else:
                    return "ERROR: Invalid Access token", False
            else:
                return "Access Token is still valid", True
        else:
            return "No access token", False

    def process_response(self, request, response):
        # print (f"\n++++++++++++++\nResponse #{self.count} - {response.status_code}\nResponse Msg: - {str(response.content)}\n++++++++++++++++\n")
        print (f"\n++++++++++++++\nResponse #{self.count} - {response.status_code}\n++++++++++++++++\n")
        return response
    
   

   
