#TODO: develop service for users
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import exists
from typing_extensions import assert_type

from auth.utils.hashing_password import hash_password
from models.models import User
from models.schemas.user_schema import UserResponse, UserDto
from routers.db_session import get_db


def check_exists_username_or_email(email, username, db):
    if (db.query(exists().where(User.email == email)).scalar() or
        db.query(exists().where(User.username == username)).scalar()):
        raise HTTPException(status_code=409, detail='Username or email is already in use')


def create_user(user: UserDto, db: Session = Depends(get_db)) -> UserResponse:
    db_user = User(username=user.username, email=user.email, password=hash_password(user.password))
    check_exists_username_or_email(db_user.email, db_user.username, db)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(
        id: int,
        db: Session = Depends(get_db)
) -> UserResponse:
    db_user = db.get(User, id)
    if not db_user:
        raise HTTPException(status_code=404, detail='User not found')
    db.delete(db_user)
    db.commit()
    return UserResponse.model_validate(db_user)


def get_users(db: Session = Depends(get_db)) -> list[UserResponse]:
    users = db.query(User).all()
    if not users:
        raise HTTPException(status_code=404, detail='No users found')
    return [UserResponse.model_validate(user) for user in users]


def edit_user_by_id(
        id: int,
        user: UserDto,
        db: Session = Depends(get_db)
) -> UserResponse:
    db_user = db.get(User, id)
    if not db_user:
        raise HTTPException(status_code=404, detail='User not found')
    db_user.username = user.username
    db_user.email = user.email
    db.commit()
    return UserResponse.model_validate(db_user)

def get_user_by_id(id: int, db: Session = Depends(get_db)) -> UserResponse:
    db_user = db.get(User, id)
    if not db_user:
        raise HTTPException(status_code=404, detail='User not found')
    return UserResponse.model_validate(db_user)
