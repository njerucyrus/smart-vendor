from datetime import datetime
from enum import Enum
from typing import Optional, Union

from pydantic import BaseModel, ConfigDict


class UserTypeEnum(str, Enum):
    vendor = 'vendor'
    consumer = 'consumer'


class UserBase(BaseModel):
    card_id: str
    name: str
    phone_number: str
    user_type: UserTypeEnum


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


class StatusEnum(str, Enum):
    pending = 'pending'
    success = 'success'
    failed = 'failed'


class TopUpBase(BaseModel):
    account_id: str
    txn_id: str
    receipt_no: Union[str, None] = None
    amount: float
    phone_number: str
    status: StatusEnum


class TopUpCreate(TopUpBase):
    pass


class TopUpRead(TopUpBase):
    model_config = ConfigDict(from_attributes=True)
    id: str


class TopUpUpdate(BaseModel):
    account_id: Union[str, None] = None
    txn_id: str
    receipt_no: Union[str, None] = None
    amount: Union[float, None] = None
    phone_number: Union[str, None] = None
    status: Union[StatusEnum, None] = None

