from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.orm import Session
from smart_vendor import schemas, models
from smart_vendor.db_services.users import db_get_user


async def db_create_user_account(db: Session, user_account: schemas.UserAccountCreate):
    user = await db_get_user(db, user_account.card_id)
    if user:
        payload = {
            'user_id': user.id,
            'available_balance': user_account.available_balance,
            'location': user_account.location
        }
        account = models.UserAccount(**payload)
        db.add(account)
        db.commit()
        db.refresh(account)
        return account
    else:
        return None


async def db_update_user_account(db: Session, card_id: str, user_account: schemas.UserAccountUpdate):
    account = db.query(models.UserAccount). \
        join(models.User, models.User.id == models.UserAccount.user_id). \
        filter(models.User.card_id == card_id).first()
    if account:
        for attr, value in user_account.model_dump().items():
            setattr(account, attr, value)
        db.commit()
        db.refresh(account)

    return account


async def db_patch_user_account(db: Session, card_id: str, user_account: schemas.UserAccountPatch):
    account = db.query(models.UserAccount). \
        join(models.User, models.User.id == models.UserAccount.user_id). \
        filter(models.User.card_id == card_id).first()
    if account:
        for attr, value in user_account.model_dump(exclude_unset=True).items():
            setattr(account, attr, value)
        db.commit()
        db.refresh(account)

    return account


async def db_get_user_account(db: Session, card_id: str):
    return db.query(models.UserAccount). \
        join(models.User, models.User.id == models.UserAccount.user_id). \
        filter(models.User.card_id == card_id).first()


async def db_get_user_accounts(db: Session):
    try:
        return paginate(db, select(models.UserAccount))
    except Exception as e:
        print(e)
        return None


async def db_delete_user_account(db: Session, card_id: str):
    account = db.query(models.UserAccount). \
        join(models.User, models.User.id == models.UserAccount.user_id). \
        filter(models.User.card_id == card_id).first()
    if account:
        db.delete(account)
        db.commit()
    return account
