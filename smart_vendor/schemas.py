from datetime import datetime
from enum import Enum
from typing import Optional, Union, List

from pydantic import BaseModel, ConfigDict, Field


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


class PaymentBase(BaseModel):
    account_id: str
    account: Union[UserAccountRead, None] = None
    txn_id: str
    receipt_no: Union[str, None] = None
    amount: float
    phone_number: str
    status: StatusEnum
    date: Union[datetime, None] = None


class PaymentCreate(PaymentBase):
    pass


class PaymentRead(PaymentBase):
    model_config = ConfigDict(from_attributes=True)
    id: str


class PaymentUpdate(BaseModel):
    account_id: Union[str, None] = None
    txn_id: str
    receipt_no: Union[str, None] = None
    amount: Union[float, None] = None
    phone_number: Union[str, None] = None
    status: Union[StatusEnum, None] = None


class STKPushRequest(BaseModel):
    phone_number: str
    amount: int
    account_number: Union[str, None] = ''


#  mpesa  data schemas

class Item(BaseModel):
    Name: str
    Value: Optional[str]


class CallbackMetadata(BaseModel):
    Item: List[Item]


class StkCallback(BaseModel):
    MerchantRequestID: str
    CheckoutRequestID: str
    ResultCode: int
    ResultDesc: str
    CallbackMetadata: CallbackMetadata


class Body(BaseModel):
    stkCallback: StkCallback


class StkPayload(BaseModel):
    Body: Body


class StkRequestResponse(BaseModel):
    merchant_request_id: str = Field(alias="MerchantRequestID")
    checkout_request_id: str = Field(alias="CheckoutRequestID")
    response_code: str = Field(alias="ResponseCode")
    response_description: str = Field(alias="ResponseDescription")
    customer_message: str = Field(alias="CustomerMessage")

# endof stk push schemas
