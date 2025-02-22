from starlette.status import HTTP_401_UNAUTHORIZED
from sqlalchemy.orm import Session
from config import settings
from jwt import encode, decode
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from routers.db_session import get_db
from models.models import User
from auth.hashing_password import validate_password


algorithm = settings.ALGORITHM
private_key = settings.JWT_PRIVATE.read_text()
public_key = settings.JWT_PUBLIC.read_text()
http_bearer = HTTPBearer()


def get_auth_user(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)):
    token = credentials.credentials
    payload = decode_jwt(token=token)
    auth_user_id = payload.get('sub')
    return auth_user_id


def encode_jwt(
        payload: dict,
        expire_minutes: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES
):
    payload_to_encode = payload.copy()
    now = datetime.utcnow()
    expire = now + timedelta(minutes=expire_minutes)
    payload_to_encode.update(exp=expire, iat=now)
    encoded = encode(payload=payload_to_encode, key=private_key, algorithm=algorithm)
    return encoded


def decode_jwt(token: str):
    decoded = decode(token, public_key, algorithms=[algorithm])
    return decoded


def validate_auth_user(email: str,
                       password: str,
                       db: Session = Depends(get_db)
):
    user = db.query(User).filter_by(email=email).first()
    if not user:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail='invalid username or password')
    if not validate_password(password=password, hashed_password=user.password):
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail='invalid username or password')
    return user
