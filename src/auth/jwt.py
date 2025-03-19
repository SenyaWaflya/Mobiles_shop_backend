from fastapi import HTTPException, status
from config import settings
from jwt import encode, decode
from datetime import datetime, timedelta
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


algorithm = settings.ALGORITHM
private_key = settings.JWT_PRIVATE.read_text()
public_key = settings.JWT_PUBLIC.read_text()


def get_auth_user(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())) -> dict:
    token = credentials.credentials
    payload = decode_jwt(token=token)
    payload_to_response = {
        'sub': int(payload.get('sub')),
        'is_superuser': payload.get('is_superuser'),
        'is_owner': payload.get('is_owner')
    }
    return payload_to_response


def validate_admin_permissions(token_payload: dict) -> None:
    if not token_payload.get('is_superuser'):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not enough permissions')

def validate_owner_permissions(token_payload: dict) -> None:
    if not token_payload.get('is_owner'):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not enough permissions')


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
