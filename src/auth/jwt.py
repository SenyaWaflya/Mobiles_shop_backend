from config import settings
from jwt import encode, decode
from datetime import datetime, timedelta
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


algorithm = settings.ALGORITHM
private_key = settings.JWT_PRIVATE.read_text()
public_key = settings.JWT_PUBLIC.read_text()


def get_auth_user(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())) -> int:
    token = credentials.credentials
    payload = decode_jwt(token=token)
    auth_user_id = payload.get('sub')
    return int(auth_user_id)


def encode_jwt(
        payload: dict,
        expire_minutes: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES
) -> str:
    payload_to_encode = payload.copy()
    now = datetime.utcnow()
    expire = now + timedelta(minutes=expire_minutes)
    payload_to_encode.update(exp=expire, iat=now)
    encoded = encode(payload=payload_to_encode, key=private_key, algorithm=algorithm)
    return encoded


def decode_jwt(token: str) -> dict[str: str]:
    decoded = decode(token, public_key, algorithms=[algorithm])
    return decoded
