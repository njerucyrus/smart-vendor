from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi_pagination.links import Page

from sqlalchemy.orm import Session
from starlette import status

from smart_vendor import schemas
from smart_vendor.db_services.user_accounts import \
    db_create_user_account, db_get_user_accounts, db_get_user_account, db_update_user_account, db_patch_user_account, \
    db_delete_user_account
from smart_vendor.dependancies import get_db_session

router = APIRouter()


@router.post("/users/accounts/", response_model=schemas.UserAccountRead)
async def create_user_account(account: schemas.UserAccountCreate, db: Session = Depends(get_db_session)):
    account = await db_create_user_account(db, account)
    return account


@router.get("/users/accounts/{card_id}/", response_model=schemas.UserAccountRead)
async def user_account_detail(card_id: str, db: Session = Depends(get_db_session)):
    account = await db_get_user_account(db, card_id)
    if not account:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Account not found')
    return account


@router.get("/users/accounts/")
async def read_user_accounts(db: Session = Depends(get_db_session)) -> Page[schemas.UserAccountRead]:
    accounts = await db_get_user_accounts(db)
    return accounts


@router.put("/users/accounts/{card_id}/", response_model=schemas.UserAccountRead)
async def update_user_account(card_id: str, account: schemas.UserAccountUpdate, db: Session = Depends(get_db_session)):
    res = await db_update_user_account(
        db=db,
        card_id=card_id,
        user_account=account
    )
    return res


@router.patch("/users/accounts/{card_id}/", response_model=schemas.UserAccountRead)
async def partial_update_user_account(card_id: str, account: schemas.UserAccountPatch,
                                      db: Session = Depends(get_db_session)):
    res = await db_patch_user_account(
        db=db,
        card_id=card_id,
        user_account=account
    )
    return res


@router.delete("/users/account/{card_id}")
async def delete_user_account(card_id: str, response: Response, db: Session = Depends(get_db_session)):
    deleted = await db_delete_user_account(db, card_id)
    if deleted is not None:
        response.status_code = status.HTTP_204_NO_CONTENT
        return {
            'detail': 'Account deleted'
        }
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            'detail': 'Could not find matching account'
        }
