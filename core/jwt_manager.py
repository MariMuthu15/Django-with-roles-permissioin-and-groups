import json
from datetime import timedelta
from uuid import uuid4
import os

from dotenv import load_dotenv

from rest_framework.exceptions import AuthenticationFailed
import jwt

env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path=env_path)

from core.schema import JWTManagerSchema
from core.utils import get_current_utc, days_to_minutes

algorithm = os.getenv('JWT_ALGORITHM')
secret_key = os.getenv('JWT_SECRET_KEY')
access_token_expiry = os.getenv('ACCESS_TOKEN_EXPIRY_IN_MINUTES')
refresh_token_expiry = os.getenv('REFRESH_TOKEN_EXPIRY_IN_DAYS')


class JWTManager:
    @staticmethod
    def create_token(data: dict, expires_in: int = 60) -> JWTManagerSchema:
        """Create a token by encoding data
        :param data: dict type, dynamically place data to templated
        :param expires_in: int type, minutes to expire
        """
        # Ensure datetime fields are serialized to ISO format
        data = json.loads(json.dumps(data, default=str))

        unique_id = str(uuid4())
        now_utc = get_current_utc()
        payload = data.copy()
        payload['jti'] = unique_id
        payload["exp"] = now_utc + timedelta(minutes=expires_in)

        token = jwt.encode(payload, secret_key, algorithm=algorithm)
        return JWTManagerSchema(token=token, expires_at=payload['exp'], jti=payload['jti'])

    @staticmethod
    def create_access_token(user_data: dict):
        """Create Access token by encoding user_data"""
        payload = user_data.copy()
        payload['token_type'] = 'access'
        return JWTManager.create_token(data=payload, expires_in=int(access_token_expiry))

    @staticmethod
    def create_refresh_token(user_data: dict):
        """Create refresh token by encoding user_data"""
        payload = user_data.copy()
        payload['token_type'] = 'refresh'
        expiry = days_to_minutes(day=int(refresh_token_expiry))
        return JWTManager.create_token(data=payload, expires_in=expiry)

    @staticmethod
    def verify_token(token: str) -> bool:
        try:
            jwt.decode(token, secret_key, algorithms=[algorithm])
            return True
        except jwt.ExpiredSignatureError:
            print("Token has expired")
        except jwt.InvalidTokenError:
            print("Invalid token")
        return False

    @staticmethod
    def decode_token(token: str) -> dict:
        try:
            return jwt.decode(token, secret_key, algorithms=[algorithm])
        except jwt.InvalidTokenError as e:
            raise AuthenticationFailed('Found Invalid Token to decode ' + str(e))