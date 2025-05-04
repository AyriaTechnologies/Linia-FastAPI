from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

from app.common.schemas import Token


class User(BaseModel):
    id: int = Field(description="The User's ID")
    first_name: str = Field(description="The User's first name")
    last_name: str = Field(description="The User's last name")
    is_active: bool = Field(description="Whether the User is active or not")
    updated_at: datetime | None = Field(
        default=None, description="The User's last update date"
    )
    created_at: datetime = Field(description="The User's creation date")


class UserLoginCredential(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    """
    Base schema for user login response
    """

    user: User = Field(description="The user's details")
    tokens: Token = Field(description="The auth token")
