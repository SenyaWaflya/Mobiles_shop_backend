from fastapi import APIRouter, Form, Depends, status
from pydantic import EmailStr
from typing import Annotated

from src.auth.jwt import get_auth_user
from src.schemas.user import UserResponse, UserDto
from src.services.admin import AdminService

router = APIRouter(prefix='/admins', tags=['Admins'])


@router.post('/register', status_code=status.HTTP_201_CREATED, summary='Register New Admin (authenticated admin)')
async def register_new_admin(
        username: Annotated[str, Form(description='Имя пользователя', min_length=2, max_length=15, examples=['username'])],
        email: Annotated[EmailStr, Form(description='Почта пользователя', examples=['anymail@gmail.com'])],
        password: Annotated[str, Form(description='Пароль пользователя', min_length=8, examples=['secretPassword'])],
        token_payload: dict = Depends(get_auth_user)
) -> UserResponse:
    admin = UserDto(username=username, email=email, is_superuser=True, password=password)
    return await AdminService.register(admin, token_payload)


@router.get('/', summary='Get All Admins (authenticated admin)')
async def get_all_admins(token_payload: dict = Depends(get_auth_user)) -> list[UserResponse]:
    return await AdminService.get_admins(token_payload)
