from pydantic import EmailStr
from sqlalchemy.sql import exists, select

from src.database.connection import async_session
from src.database.models import UserModel
from src.schemas.users import UserDto


class UsersRepository:
    @staticmethod
    async def check_exists_user(tg_id: str) -> bool:
        async with async_session() as session:
            query = select(exists().where(UserModel.tg_id == tg_id))
            result = await session.execute(query)
            user_exists = result.scalar()
            return user_exists

    @staticmethod
    async def check_exists_email(email: EmailStr) -> bool:
        async with async_session() as session:
            query = select(exists().where(UserModel.email == email))
            result = await session.execute(query)
            email_exists = result.scalar()
            return email_exists

    @staticmethod
    async def add(user_dto: UserDto) -> UserModel:
        async with async_session() as session:
            user_model = UserModel(tg_id=user_dto.tg_id, username=user_dto.username, email=user_dto.email)
            session.add(user_model)
            await session.commit()
            await session.refresh(user_model)
            return user_model

    @staticmethod
    async def get(tg_id: str) -> UserModel:
        async with async_session() as session:
            query = select(UserModel).where(UserModel.tg_id == tg_id)
            result = await session.execute(query)
            user_model = result.scalars().first()
            return user_model

    @staticmethod
    async def get_all() -> list[UserModel]:
        async with async_session() as session:
            query = select(UserModel)
            result = await session.execute(query)
            users_models = result.scalars().all()
            return users_models
