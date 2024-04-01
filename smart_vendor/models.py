import base64
import datetime
import uuid

from sqlalchemy import Column, String, ForeignKey, Numeric, DateTime, Enum
from sqlalchemy.orm import relationship

from smart_vendor.database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()).replace('-', ''))
    card_id = Column(String, unique=True)
    name = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    user_type = Column(Enum('vendor', 'consumer', name='user_type_enum'))
    account = relationship('UserAccount', back_populates='user')


class UserAccount(Base):
    __tablename__ = 'user_accounts'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()).replace('-', ''))
    user_id = Column(String, ForeignKey("users.id"))
    available_balance = Column(Numeric(precision=9, scale=2))
    user = relationship('User', back_populates='account')
    payments = relationship('Payment', back_populates='account')
    location = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)


class Payment(Base):
    __tablename__ = 'payments'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()).replace('-', ''))
    account_id = Column(String, ForeignKey("user_accounts.id"))
    account = relationship('UserAccount', back_populates='payments')
    txn_id = Column(String, unique=True)
    receipt_no = Column(String, nullable=True)
    phone_number = Column(String(20), nullable=True)
    amount = Column(Numeric(precision=9, scale=2))
    status = Column(Enum('pending', 'success', 'failed', name='status_enum'), default='pending')
    date = Column(DateTime, default=datetime.datetime.utcnow)




