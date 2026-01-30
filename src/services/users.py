from fastapi import HTTPException, status

from src.database.repositories.users import UsersRepository
from src.schemas.users import UserDto, UserResponse


class UsersService:
    @staticmethod
    async def create(user_dto: UserDto) -> UserResponse:
        exists_user = await UsersRepository.check_exists_user(user_dto.tg_id)
        if exists_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='User already exists')
        exists_email = await UsersRepository.check_exists_email(user_dto.email)
        if exists_email:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Email already exists')
        user_model = await UsersRepository.add(user_dto)
        return UserResponse.model_validate(user_model)

    @staticmethod
    async def get_user(tg_id: str) -> UserResponse:
        user_model = await UsersRepository.get(tg_id)
        if not user_model:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
        return UserResponse.model_validate(user_model)

    @staticmethod
    async def get_users() -> list[UserResponse]:
        users_models = await UsersRepository.get_all()
        if not users_models:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No users found')
        return [UserResponse.model_validate(user_model) for user_model in users_models]
