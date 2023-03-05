from typing import List, Optional

from pydantic import BaseModel, Field, EmailStr, validator


class UserCreate(BaseModel):
    full_name: str = Field(min_length=5)
    email: EmailStr
    password: str = Field(min_length=6)

    @validator("full_name")
    def name_has_space(cls, v: str) -> str:
        if " " not in v:
            raise ValueError("full name must be has an empty space")
        return v


class UserList(BaseModel):
    id: int
    full_name: str
    email: str

    class Config:
        orm_mode = True


class UserRetrieve(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    scopes: List[str]
    provider: str
    is_active: bool

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    full_name: Optional[str]
    scopes: Optional[List[str]]


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """data that is hashed in token"""

    user: UserRetrieve
    scopes: List[str] = []
