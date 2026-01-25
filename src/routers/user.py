from typing import Annotated

from fastapi import APIRouter, Form, Path, status
from pydantic import EmailStr

from src.schemas.user import UserDto, UserResponse
from src.services.user import UserService

router = APIRouter(prefix='/users', tags=['Users'])


@router.post('/register', status_code=status.HTTP_201_CREATED, summary='Register')
async def register(
    username: Annotated[str, Form(description='Имя пользователя', min_length=2, max_length=15, examples=['username'])],
    email: Annotated[EmailStr, Form(description='Почта пользователя', examples=['anymail@gmail.com'])],
    password: Annotated[str, Form(description='Пароль пользователя', min_length=8, examples=['secretPassword'])],
) -> UserResponse:
    user = UserDto(username=username, email=email, password=password)
    return await UserService.create_user(user)


@router.get('/', summary='Get All Users')
async def get_all_users() -> list[UserResponse]:
    return await UserService.get_users()


@router.get('/{user_id}', summary='Get Current User')
async def get_current_user(
    user_id: Annotated[int, Path(description='Id пользователя', ge=1)],
) -> UserResponse:
    return await UserService.get_user_by_id(user_id)


@router.put('/me', summary='Edit Me')
async def edit_me(
    new_username: Annotated[
        str, Form(description='Новое имя пользователя', min_length=2, max_length=15, examples=['NewUsername'])
    ],
    new_email: Annotated[EmailStr, Form(description='Новая почта пользователя', examples=['anothermail@gmail.com'])],
) -> UserResponse:
    return await UserService.edit_info_me(new_username, new_email)
