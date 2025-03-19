from pydantic import EmailStr
from sqlalchemy import select
from fastapi import HTTPException, status
from sqlalchemy.sql import exists

from src.auth.hashing_password import hash_password, validate_password
from src.auth import jwt
from src.auth.jwt import validate_admin_permissions, validate_owner_permissions
from src.database.database import new_session
from src.database.models import User, Product, UserProduct
from src.schemas.product import ProductResponse
from src.schemas.user import UserResponse, UserDto
from src.schemas.token import TokenInfo


class UserService:
    @staticmethod
    async def check_exists_username_or_email(email: EmailStr, username: str) -> None:
        async with new_session() as session:
            query = select(exists().where(User.email == email))
            result = await session.execute(query)
            email_exists = result.scalars().first()
            if email_exists:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Email is already in use')

            query = select(exists().where(User.username == username))
            result = await session.execute(query)
            username_exists = result.scalars().first()
            if username_exists:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Username is already in use')


    @staticmethod
    async def validate_auth_user(email: EmailStr, password: str) -> UserResponse | None:
        async with new_session() as session:
            query = select(User).where(User.email == email)
            result = await session.execute(query)
            user = result.scalars().first()
            if not user:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid username or password')
            if not validate_password(password=password, hashed_password=user.password):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid username or password')
            return user


    @staticmethod
    async def create_user(user_dto: UserDto) -> UserResponse:
        async with new_session() as session:
            user = User(
                username=user_dto.username,
                email=user_dto.email,
                password=hash_password(user_dto.password)
            )
            await UserService.check_exists_username_or_email(user.email, user.username)
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user


    @staticmethod
    async def auth_user_with_jwt(email: EmailStr, password: str) -> TokenInfo:
        user = await UserService.validate_auth_user(email, password)
        payload = {
            'sub': str(user.id),
            'username': user.username,
            'email': user.email,
            'is_superuser': user.is_superuser,
            'is_owner': user.is_owner
        }
        token = jwt.encode_jwt(payload=payload)
        return TokenInfo(access_token=token, token_type='Bearer')


    @staticmethod
    async def get_users(token_payload: dict) -> list[UserResponse]:
        validate_admin_permissions(token_payload)
        async with new_session() as session:
            query = select(User)
            result = await session.execute(query)
            users = result.scalars().all()
            if not users:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No users found')
            return [UserResponse.model_validate(user) for user in users]


    @staticmethod
    async def get_user_by_id(id: int, token_payload: dict) -> UserResponse:
        validate_admin_permissions(token_payload)
        async with new_session() as session:
            query = select(User).where(User.id == id)
            result = await session.execute(query)
            user = result.scalars().first()
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
            return UserResponse.model_validate(user)


    @staticmethod
    async def get_info_me(token_payload: dict) -> UserResponse:
        id = token_payload.get('sub')
        async with new_session() as session:
            query = select(User).where(User.id == id)
            result = await session.execute(query)
            user = result.scalars().first()
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
            return UserResponse.model_validate(user)


    @staticmethod
    async def edit_info_me(new_username: str, new_email: EmailStr, token_payload: dict) -> UserResponse:
        id = token_payload.get('sub')
        async with new_session() as session:
            query = select(User).where(User.id == id)
            result = await session.execute(query)
            user = result.scalars().first()
            user.username = new_username
            user.email = new_email
            await session.commit()
            await session.refresh(user)
            return user


    @staticmethod
    async def edit_permissions(id: int, new_is_superuser: bool, token_payload: dict) -> UserResponse:
        validate_admin_permissions(token_payload)
        async with new_session() as session:
            query = select(User).where(User.id == id)
            result = await session.execute(query)
            user = result.scalars().first()
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
            if user.is_superuser:
                validate_owner_permissions(token_payload)
                user.is_superuser = new_is_superuser
                await session.commit()
                await session.refresh(user)
                return user
            user.is_superuser = new_is_superuser
            await session.commit()
            await session.refresh(user)
            return user


    @staticmethod
    async def get_favorites(token_payload: dict) -> list[ProductResponse]:
        id = token_payload.get('sub')
        async with new_session() as session:
            query = select(Product).join(UserProduct).where(UserProduct.user_id == id)
            result = await session.execute(query)
            products = result.scalars().all()
            if not products:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Favorite products not found')
            return [product for product in products]
