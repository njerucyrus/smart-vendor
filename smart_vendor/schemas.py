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
