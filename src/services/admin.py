from sqlalchemy import select

from config import settings
from src.auth.hashing_password import hash_password
from src.database.models import User
from src.auth.jwt import validate_admin_permissions
from src.database.database import new_session
from src.schemas.user import UserDto, UserResponse
from src.services.user import UserService


class AdminService:
    @staticmethod
    async def init_superuser() -> None:
        async with new_session() as session:
            init_superuser = User(
                username=settings.INIT_OWNER_USERNAME,
                email=settings.INIT_OWNER_EMAIL,
                is_superuser=True,
                is_owner=True,
                password=hash_password(settings.INIT_OWNER_PASSWORD)
            )
            query = select(User).where(User.email == init_superuser.email)
            result = await session.execute(query)
            select_superuser = result.scalars().first()
            if not select_superuser:
                session.add(init_superuser)
                await session.commit()


    @staticmethod
    async def register(admin_dto: UserDto, token_payload: dict) -> UserResponse:
        validate_admin_permissions(token_payload)
        async with new_session() as session:
            admin = User(
                username=admin_dto.username,
                email=admin_dto.email,
                is_superuser=admin_dto.is_superuser,
                password=hash_password(admin_dto.password)
            )
            await UserService.check_exists_username_or_email(admin.email, admin.username)
            session.add(admin)
            await session.commit()
            await session.refresh(admin)
            return admin


    @staticmethod
    async def get_admins(token_payload: dict) -> list[UserResponse]:
        validate_admin_permissions(token_payload)
        async with new_session() as session:
            query = select(User).where(User.is_superuser == True)
            result = await session.execute(query)
            admins = result.scalars().all()
            return [admin for admin in admins]
