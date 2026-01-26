from typing import Annotated

from fastapi import APIRouter, Form, Path, status
from pydantic import EmailStr

from src.schemas.users import UserDto, UserResponse
from src.services.users import UsersService

router = APIRouter(prefix='/users', tags=['Users'])


@router.post('/register', status_code=status.HTTP_201_CREATED, summary='Register')
async def register(
    tg_id: Annotated[str, Form(description='ID пользователя в telegram', examples=['123456789'])],
    username: Annotated[str, Form(description='Имя пользователя', min_length=2, max_length=15, examples=['username'])],
    email: Annotated[EmailStr, Form(description='Почта пользователя', examples=['anymail@gmail.com'])],
) -> UserResponse:
    user = UserDto(tg_id=tg_id, username=username, email=email)
    return await UsersService.create(user)


@router.get('/{tg_id}', summary='Get Current User')
async def get_user(
    tg_id: Annotated[str, Path(description='ID пользователя в telegram', examples=['123456789'])],
) -> UserResponse:
    return await UsersService.get_user(tg_id)


@router.get('/', summary='Get All Users')
async def get_users() -> list[UserResponse]:
    return await UsersService.get_users()
