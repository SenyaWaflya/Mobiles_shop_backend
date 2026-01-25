from fastapi import HTTPException, status
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.sql import exists

from src.database.database import new_session
from src.database.models import User
from src.schemas.user import UserDto, UserResponse


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
    async def create_user(user_dto: UserDto) -> UserResponse:
        async with new_session() as session:
            user = User(username=user_dto.username, email=user_dto.email)
            await UserService.check_exists_username_or_email(user_dto.email, user_dto.username)
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

    @staticmethod
    async def get_users() -> list[UserResponse]:
        async with new_session() as session:
            query = select(User)
            result = await session.execute(query)
            users = result.scalars().all()
            if not users:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No users found')
            return [UserResponse.model_validate(user) for user in users]

    @staticmethod
    async def get_user_by_id(user_id: int) -> UserResponse:
        async with new_session() as session:
            query = select(User).where(User.id == user_id)
            result = await session.execute(query)
            user = result.scalars().first()
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
            return UserResponse.model_validate(user)

    @staticmethod
    async def edit_info_me(new_username: str, new_email: EmailStr) -> UserResponse:
        async with new_session() as session:
            query = select(User).where(User.id == id)
            result = await session.execute(query)
            user = result.scalars().first()
            user.username = new_username
            user.email = new_email
            await session.commit()
            await session.refresh(user)
            return user
