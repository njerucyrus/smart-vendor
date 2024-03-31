from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.orm import Session
from smart_vendor import schemas, models


async def db_create_user_account(db: Session, user_account: schemas.UserAccountCreate):
    account = models.UserAccount(**user_account.model_dump())
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


async def db_update_user_account(db: Session, id: str, user_account: schemas.UserAccountUpdate):
    account = db.query(models.UserAccount).filter(models.UserAccount.id == id).first()
    if account:
        for attr, value in user_account.model_dump().items():
            setattr(account, attr, value)
        db.commit()
        db.refresh(account)

    return account


async def db_patch_user_account(db: Session, id: str, user_account: schemas.UserAccountPatch):
    account = db.query(models.UserAccount).filter(models.UserAccount.id == id).first()
    if account:
        for attr, value in user_account.model_dump(exclude_unset=True).items():
            setattr(account, attr, value)
        db.commit()
        db.refresh(account)

    return account


async def db_get_user_account(db:Session, id: str):
    return db.query(models.UserAccount).filter(models.UserAccount.id == id).first()


async def db_get_user_accounts(db:Session):
    return paginate(db, select(models.UserAccount))


async def db_delete_user_account(db:Session, id:str):
    account = db.query(models.UserAccount).filter(models.UserAccount.id == id).first()
    if account:
        db.delete(account)
        db.commit()
    return account