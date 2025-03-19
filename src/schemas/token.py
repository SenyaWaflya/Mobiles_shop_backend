from pydantic import BaseModel, Field
from typing import Annotated


class TokenInfo(BaseModel):
    access_token: Annotated[str, Field(description='JWT токен')]
    token_type: Annotated[str, Field(description='Тип токена')]
