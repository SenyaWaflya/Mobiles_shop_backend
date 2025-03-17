from typing import Annotated
from fastapi import APIRouter, Depends, Path, Form
from pydantic import EmailStr

from src.auth.jwt import get_auth_user
from src.schemas.token import TokenInfo
from src.schemas.user import UserResponse, UserDto
from src.services.user import UserService


router = APIRouter(prefix='/users', tags=['Users'])


@router.post('/register')
async def create(username: Annotated[str, Form(description='Имя пользователя', min_length=2, max_length=15, examples=['username'])],
                 email: Annotated[EmailStr, Form(description='Почта пользователя', examples=['anymail@gmail.com'])],
                 password: Annotated[str, Form(description='Пароль пользователя', min_length=8, examples=['secretPassword'])]
) -> UserResponse:
    user = UserDto(username=username, email=email, password=password)
    return await UserService.create_user(user)


@router.post('/login')
async def login(
        email: Annotated[EmailStr, Form(description='Почта пользователя', examples=['anymail@gmail.com'])],
        password: Annotated[str, Form(description='Пароль пользователя', min_length=8, examples=['secretPassword'])]
) -> TokenInfo:
    return await UserService.auth_user_with_jwt(email, password)


@router.get('/me')
async def get_me(id: int = Depends(get_auth_user)) -> UserResponse:
    return await UserService.get_user_by_id(id)


@router.get('/')
async def get_all_users() -> list[UserResponse]:
    return await UserService.get_users()


@router.get('/{id}')
async def get_current_user(
        id: Annotated[int, Path(description='Id пользователя', ge=1)]
) -> UserResponse:
    return await UserService.get_user_by_id(id)
