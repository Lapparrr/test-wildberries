from pydantic import BaseModel, EmailStr, HttpUrl
from pydantic_core import Url


class BaseRequest(BaseModel):
    # may define additional fields or config shared across requests
    pass


class RefreshTokenRequest(BaseRequest):
    refresh_token: str


class UserUpdatePasswordRequest(BaseRequest):
    password: str


class UserCreateRequest(BaseRequest):
    email: EmailStr
    password: str


class PhotoUpdateRequest(BaseRequest):
    id: int
    photo_url: HttpUrl


class MemoryCreateRequest(BaseRequest):
    header: str
    text: str
    photos: list[Url] | None


class MemoryUpdateRequest(BaseRequest):
    id: int
    header: str
    text: str
    photos: list[PhotoUpdateRequest] | None
