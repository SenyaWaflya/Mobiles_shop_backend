from typing import Annotated
from fastapi import APIRouter, Depends, Path, Form
from pydantic import EmailStr
from sqlalchemy.orm import Session

from auth.jwt_utils import get_auth_user
from routers.db_session import get_db
from models.schemas.user_schema import UserResponse, UserDto
from services.user_service import (
    create_user,
    get_users,
    get_user_by_id,
    auth_user_with_jwt,
    get_my_info
)

router = APIRouter(tags=['Users'])


@router.post('/register')
async def create(username: str = Form(),
                 email: EmailStr = Form(),
                 password: str = Form(),
                 db: Session = Depends(get_db)
) -> UserResponse:
    user = UserDto(username=username, email=email, password=password)
    return create_user(user, db)


@router.post('/login')
async def login(email: EmailStr = Form(), password: str = Form(), db: Session = Depends(get_db)):
    return auth_user_with_jwt(email, password, db)


@router.get('/users/me')
async def get_me(id: int = Depends(get_auth_user), db: Session = Depends(get_db)):
    return get_my_info(id=id, db=db)


@router.get('/users')
async def get_all_users(db: Session = Depends(get_db)) -> list[UserResponse]:
    return get_users(db)


@router.get('/users/{id}')
async def get_current_user(
        id: Annotated[int, Path(..., title='Id пользователя', ge=1)],
        db: Session = Depends(get_db)
) -> UserResponse:
    return get_user_by_id(id, db)
