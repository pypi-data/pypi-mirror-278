import base64
from typing import Optional, Dict
from ecdsa import VerifyingKey, BadSignatureError

from .client import Client


class Webhook:
    def __init__(self, client: Client, public_key_base64: Optional[str] = None, x_sign_base64: Optional[str] = None,
                 headers: Optional[Dict[str, str]] = None):
        if not public_key_base64:
            public_key_base64 = client.get_public_key()
        if not public_key_base64:
            raise Exception('Cannot retrieve public key')
        self.public_key_base64 = public_key_base64

        if x_sign_base64:
            self.x_sign_base64 = x_sign_base64
        elif headers and 'HTTP_X_SIGN' in headers:
            self.x_sign_base64 = headers['HTTP_X_SIGN']
        else:
            raise Exception('Cannot retrieve X-Sign header value')

    def verify(self, request_body: Optional[str] = None) -> bool:
        public_key = VerifyingKey.from_pem(base64.b64decode(self.public_key_base64))
        signature = base64.b64decode(self.x_sign_base64)

        try:
            return public_key.verify(signature, request_body.encode())
        except BadSignatureError:
            return False
