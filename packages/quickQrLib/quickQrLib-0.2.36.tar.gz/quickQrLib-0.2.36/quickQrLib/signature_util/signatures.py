from django import utils
from django.conf import settings 
from rest_framework.response import Response
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import json
import base64
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from rest_framework.status import HTTP_403_FORBIDDEN
import logging
from django.http import HttpResponse
import os

logger = logging.getLogger(__name__)

current_directory = os.path.dirname(os.path.abspath(__file__))
print("CURRENT DIRECTORY:", current_directory)

pem_file_path = os.path.join(current_directory, "public_key.pem")
print("pem_file_path:", pem_file_path)

def load_public_key(pem_file_path):
    try:
        # Read the PEM file
        with open(pem_file_path, "rb") as pem_file:
            pem_data = pem_file.read()
        
        # Load the public key from the PEM data
        public_key = serialization.load_pem_public_key(
            pem_data,
            backend=default_backend()
        )
        print("public_key:", public_key)
        logger.info("Public key loaded successfully.")
        return public_key
    except Exception as e:
        print(f"ERROR LOADING PUBLIC KEY: {e}\n\n")
        logger.error(f"Error loading public key: {e}")
        return None

public_key = load_public_key(pem_file_path)
    
class SignatureActions:
    @classmethod
    def verify_header_permissions(cls, permission, signature):
        if permission and signature:
            signature_bytes = base64.b64decode(signature)
            try:
                json_permission= json.loads(permission)
                json_dumped_permission = json.dumps(json_permission, default=str)
                public_key.verify(
                    signature_bytes,
                    json_dumped_permission.encode('utf-8'),
                    # data_to_verify,
                    padding.PSS(
                        mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.MAX_LENGTH
                    ),
                    hashes.SHA256()
                )
                return json_permission
            except Exception as e:
                logger.error(f"Error verifying header permissions:'{str(e)}'")
                return False
        return False

class SignatureCheckMixin:
    def __init__ (self, permission_type = 'model', *args, **kwargs):
        super().__init__(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        # Check the signature validity here
        permission_result=self.is_signature_valid(request)
        if permission_result:
            request.permission = permission_result
            return super().dispatch(request, *args, **kwargs)
            # Call the original dispatch method
        # Rest Framework Response objects will not work here
        return HttpResponse('Invalid Permissions', status=403)

    def is_signature_valid(self, request):
        print("request:", request)
        
        #  Check the signature
        #  return SignatureActions.verify_permission_signature(request.META.get('HTTP_X_PERMISSION'), request.META.get('HTTP_X_PERMISSION_SIGNATURE'))
        return SignatureActions.verify_header_permissions(request.META.get('HTTP_PERMISSION'), request.META.get('HTTP_PERMISSION_SIGNATURE'))

if __name__ == '__main__': 
    pass