from typing import Annotated
from fastapi import APIRouter, Depends, Path, Form
from sqlalchemy.orm import Session

from auth.jwt_utils import get_auth_user
from routers.db_session import get_db
from models.schemas.user_schema import UserResponse, UserDto
from services.user_service import (
    create_user,
    delete_user,
    get_users,
    edit_user_by_id,
    get_user_by_id,
    auth_user_with_jwt,
    get_my_info
)

router = APIRouter(tags=['Users'])

@router.post('/login')
async def login(email: str = Form(), password: str = Form(), db: Session = Depends(get_db)):
    return auth_user_with_jwt(email, password, db)


@router.get('/users/me')
async def get_me(id: int = Depends(get_auth_user), db: Session = Depends(get_db)):
    return get_my_info(id=id, db=db)


@router.get('/users')
async def get_all_users(db: Session = Depends(get_db)) -> list[UserResponse]:
    return get_users(db)


@router.get('/user/{id}')
async def get_current_user(
        id: Annotated[int, Path(..., title='Id пользователя', ge=1)],
        db: Session = Depends(get_db)
) -> UserResponse:
    return get_user_by_id(id, db)


@router.post('/user')
async def create(user: UserDto, db: Session = Depends(get_db)) -> UserResponse:
    return create_user(user, db)


@router.delete('/user/{id}')
async def delete(
        id: Annotated[int, Path(..., title='Id пользователя', ge=1)],
        db: Session = Depends(get_db)
) -> UserResponse:
    return delete_user(id, db)


@router.put('/user/{id}')
async def edit_user(
        id: Annotated[int, Path(..., title='Id пользователя', ge=1)],
        user: UserDto,
        db: Session = Depends(get_db)
) -> UserResponse:
    return edit_user_by_id(id, user, db)
