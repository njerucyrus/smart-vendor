from sqlalchemy import select, desc
from sqlalchemy.orm import Session
from smart_vendor import schemas, models
from fastapi_pagination.ext.sqlalchemy import paginate


async def db_create_payment(db: Session, payment: schemas.PaymentCreate):
    data_dict = payment.model_dump()
    account_id = data_dict.pop('account_id')
    # remove account keywork from the data_dict
    data_dict.pop('account')
    account = db.query(models.UserAccount).filter(models.UserAccount.id == account_id).first()
    instance = models.Payment(account=account, **data_dict)
    db.add(instance)
    db.commit()
    db.refresh(instance)
    return instance


async def db_get_payment(db: Session, txn_id: str):
    payment = db.query(models.Payment).filter(models.Payment.txn_id == txn_id).first()
    return payment


async def db_update_payment(db: Session, txn_id: str, payment: schemas.PaymentUpdate):
    instance = db.query(models.Payment).filter(models.Payment.txn_id == txn_id).first()
    if instance:
        for attr, value in payment.model_dump().items():
            setattr(instance, attr, value)
        db.commit()
        db.refresh(instance)
    return instance


async def db_patch_payment(db: Session, txn_id: str, payment: schemas.PaymentUpdate):
    instance = db.query(models.Payment).filter(models.Payment.txn_id == txn_id).first()
    if instance:
        for attr, value in payment.model_dump(exclude_unset=True).items():
            setattr(instance, attr, value)
        db.commit()
        db.refresh(instance)
    return instance


async def db_list_payments(db: Session):
    return paginate(db, select(models.Payment).order_by(desc(models.Payment.date)))


async def db_delete_payment(db: Session, txn_id: str):
    instance = db.query(models.Payment).filter(models.Payment.txn_id == txn_id).first()
    if instance:
        db.delete(instance)
        db.commit()
    return instance
