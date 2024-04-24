from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class BaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class AccessTokenResponse(BaseResponse):
    token_type: str = "Bearer"
    access_token: str
    expires_at: int
    refresh_token: str
    refresh_token_expires_at: int


class UserResponse(BaseResponse):
    user_id: str
    email: EmailStr


class PhotoResponse(BaseResponse):
    id: int
    photo_url: str


class MemoryResponse(BaseResponse):
    id: int
    user_id: UUID
    header: str
    text: str | None
    photos: list[PhotoResponse] | None
