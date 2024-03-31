from sqlalchemy import select
from sqlalchemy.orm import Session
from smart_vendor import schemas, models
from fastapi_pagination.ext.sqlalchemy import paginate


async def db_create_payment(db: Session, payment: schemas.PaymentCreate):
    instance = models.Payment(**payment.model_dump())
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
    return paginate(db, select(models.Payment).order_by(models.Payment.date))


async def db_delete_payment(db: Session, txn_id: str):
    instance = db.query(models.Payment).filter(models.Payment.txn_id == txn_id).first()
    if instance:
        db.delete(instance)
        db.commit()
    return instance
