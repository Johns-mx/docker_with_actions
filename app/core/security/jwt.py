from pytz import timezone
from fastapi import status
from jwt import encode, decode, exceptions
from datetime import datetime, timedelta
from settings import SECRET_KEY_JWT, DURATION_DAYS_TOKEN
from models.models import ResponseModel


#time_zone = timezone("America/Santo_Domingo")
def expire_token():
    date= datetime.now()
    new_date= timedelta(minutes=int(DURATION_DAYS_TOKEN)) + date
    return new_date


async def create_access_token(data: dict):
    """Create a JWT access token for the user"""
    token= encode(payload={**data, "exp": expire_token()}, key=SECRET_KEY_JWT, algorithm="HS256")
    return token


async def validate_access_token(token: str) -> ResponseModel:
    """Validate a JWT access token"""
    try:
        payload = decode(token, SECRET_KEY_JWT, algorithms="HS256")
        username = payload.get("sub")
        if username is None:
            return ResponseModel(status=status.HTTP_401_UNAUTHORIZED, error=True, message="Invalid username.", res=None)
        return ResponseModel(status=status.HTTP_200_OK, error=False, message="User information.", res=username)
    except exceptions.ExpiredSignatureError:
        return ResponseModel(status=status.HTTP_401_UNAUTHORIZED, error=True, message="Token expirado.", res=None)
    except exceptions.DecodeError:
        return ResponseModel(status=status.HTTP_401_UNAUTHORIZED, error=True, message="Token de acceso invalido para el usuario.", res=None)