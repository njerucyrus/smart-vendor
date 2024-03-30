from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    card_id: str
    name: str
    phone_number: str
    user_type: str


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class UserPatch(BaseModel):
    card_id: Union[str, None] = None
    name: Union[str, None] = None
    phone_number: Union[str, None] = None
    user_type: Union[str, None] = None


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: str


class UserAccountBase(BaseModel):
    user_id: str
    available_balance: float
    user: Union[UserBase, None] = None
    location: Union[str, None] = None
    created_at: Union[datetime, None] = None
    updated_at: Union[datetime, None] = None


class UserAccountCreate(BaseModel):
    user_id: str
    available_balance: float
    location: Union[str, None] = None


class UserAccountUpdate(BaseModel):
    available_balance: Union[float, None] = None
    location: Union[str, None] = None


class UserAccountRead(UserAccountBase):
    model_config = ConfigDict(from_attributes=True)
    id: str


class UserAccountPatch(BaseModel):
    available_balance: Union[float, None] = None
    location: Union[str, None] = None


