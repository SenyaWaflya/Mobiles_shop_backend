from typing import Annotated
from fastapi import APIRouter, Depends, Path, Form, status
from pydantic import EmailStr

from src.auth.jwt import get_auth_user
from src.schemas.product import ProductResponse
from src.schemas.token import TokenInfo
from src.schemas.user import UserResponse, UserDto
from src.services.user import UserService


router = APIRouter(prefix='/users', tags=['Users'])


@router.post('/register', status_code=status.HTTP_201_CREATED, summary='Register (all)')
async def register(
        username: Annotated[str, Form(description='Имя пользователя', min_length=2, max_length=15, examples=['username'])],
        email: Annotated[EmailStr, Form(description='Почта пользователя', examples=['anymail@gmail.com'])],
        password: Annotated[str, Form(description='Пароль пользователя', min_length=8, examples=['secretPassword'])]
) -> UserResponse:
    user = UserDto(username=username, email=email, password=password)
    return await UserService.create_user(user)


@router.post('/login', status_code=status.HTTP_201_CREATED, summary='Login (all)')
async def login(
        email: Annotated[EmailStr, Form(description='Почта пользователя', examples=['anymail@gmail.com'])],
        password: Annotated[str, Form(description='Пароль пользователя', min_length=8, examples=['secretPassword'])]
) -> TokenInfo:
    return await UserService.auth_user_with_jwt(email, password)


@router.get('/me', summary='Get Me (authenticated)')
async def get_me(token_payload: dict = Depends(get_auth_user)) -> UserResponse:
    return await UserService.get_info_me(token_payload)


@router.get('/me/favorites', summary='Get My Favorites (authenticated)')
async def get_my_favorites(token_payload: dict = Depends(get_auth_user)) -> list[ProductResponse]:
    return await UserService.get_favorites(token_payload)


@router.get('/', summary='Get All Users (authenticated admin)')
async def get_all_users(token_payload: dict = Depends(get_auth_user)) -> list[UserResponse]:
    return await UserService.get_users(token_payload)


@router.get('/{id}', summary='Get Current User (authenticated admin)')
async def get_current_user(
        id: Annotated[int, Path(description='Id пользователя', ge=1)],
        token_payload: dict = Depends(get_auth_user)
) -> UserResponse:
    return await UserService.get_user_by_id(id, token_payload)


@router.put('/me', summary='Edit Me (authenticated)')
async def edit_me(
        new_username: Annotated[str, Form(description='Новое имя пользователя', min_length=2, max_length=15, examples=['NewUsername'])],
        new_email: Annotated[EmailStr, Form(description='Новая почта пользователя', examples=['anothermail@gmail.com'])],
        token_payload: dict = Depends(get_auth_user)
) -> UserResponse:
    return await UserService.edit_info_me(new_username, new_email, token_payload)


@router.put('/{id}', summary='Edit User Permissions (authenticated admin)')
async def edit_user_permissions(
        id: Annotated[int, Path(description='Id пользователя', ge=1)],
        is_superuser: Annotated[bool, Form(description='Права суперпользователя', examples=['False'])],
        token_payload: dict = Depends(get_auth_user)
) -> UserResponse:
    return await UserService.edit_permissions(id, is_superuser, token_payload)
