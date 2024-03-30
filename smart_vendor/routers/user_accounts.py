from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from smart_vendor import schemas
from smart_vendor.db_services.user_accounts import \
    db_create_user_account, db_get_user_accounts, db_get_user_account, db_update_user_account
from smart_vendor.dependancies import get_db_session

router = APIRouter()


@router.post("/users/accounts/", response_model=schemas.UserAccountRead)
async def create_user_account(account: schemas.UserAccountCreate, db: Session = Depends(get_db_session)):
    account = await db_create_user_account(db, account)
    return account


@router.get("/users/accounts/{id}/", response_model=schemas.UserAccountRead)
async def read_user_account(id: str, db: Session = Depends(get_db_session)):
    account = await db_get_user_account(db, id)
    if not account:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Account not found')
    return account


@router.get("/users/accounts/", response_model=List[schemas.UserAccountRead])
async def read_user_accounts(db: Session = Depends(get_db_session)):
    accounts = await db_get_user_accounts(db)
    return accounts


@router.put("/users/accounts/{id}/update", response_model=schemas.UserAccountRead)
async def update_user_account(id: str, account: schemas.UserAccountUpdate, db: Session = Depends(get_db_session)):
    res = await db_update_user_account(
        db=db,
        id=id,
        user_account=account
    )
    return res


