import base64
import datetime
import uuid

from sqlalchemy import Column, String, ForeignKey, Numeric, DateTime, Enum
from sqlalchemy.orm import relationship

from smart_vendor.database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()).replace('-', ''))
    card_id = Column(String)
    name = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    user_type = Column(Enum('vendor', 'consumer', name='user_type_enum'))
    accounts = relationship('UserAccount', back_populates='user')


class UserAccount(Base):
    __tablename__ = 'user_accounts'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()).replace('-', ''))
    user_id = Column(String, ForeignKey("users.id"))
    available_balance = Column(Numeric(precision=9, scale=2))
    user = relationship('User', back_populates='accounts')
    top_ups = relationship('TopUp', back_populates='account')
    location = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)


class TopUp(Base):
    __tablename__ = 'topups'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()).replace('-', ''))
    account_id = Column(String, ForeignKey("user_accounts.id"))
    account = relationship('UserAccount', back_populates='top_ups')
    txn_id = Column(String, unique=True)
    receipt_no = Column(String, nullable=True)
    phone_number = Column(String(20), nullable=True)
    amount = Column(Numeric(precision=9, scale=2))
    status = Column(Enum('pending', 'success', 'failed', name='status_enum'), default='pending')
    date = Column(DateTime, default=datetime.datetime.utcnow)




