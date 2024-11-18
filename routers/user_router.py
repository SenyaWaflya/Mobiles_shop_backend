from typing import Annotated
from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session

from routers.db_session import get_db
from models.schemas.user_schema import UserResponse, UserDto
from services.user_service import create_user, delete_user, get_users, edit_user_by_id, get_user_by_id

router = APIRouter()


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
