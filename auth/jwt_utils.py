from starlette.status import HTTP_401_UNAUTHORIZED
from sqlalchemy.orm import Session
from config import settings
from jwt import encode, decode
from datetime import datetime, timedelta
from fastapi import Form, HTTPException, Depends
from routers.db_session import get_db
from models.models import User
from auth.hashing_password import validate_password


def encode_jwt(
        payload: dict,
        private_key: str = settings.JWT_PRIVATE.read_text(),
        algorithm: str = settings.ALGORITHM,
        expire_minutes: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES
):
    payload_to_encode = payload.copy()
    now = datetime.utcnow()
    expire = now + timedelta(minutes=expire_minutes)
    payload_to_encode.update(exp=expire, iat=now)
    encoded = encode(payload=payload_to_encode, key=private_key, algorithm=algorithm)
    return encoded


def decode_jwt(
        token: str,
        public_key: str = settings.JWT_PUBLIC.read_text(),
        algorithm: str = settings.ALGORITHM
):
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
