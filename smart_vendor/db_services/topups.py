from sqlalchemy import select
from sqlalchemy.orm import Session
from smart_vendor import schemas, models
from fastapi_pagination.ext.sqlalchemy import paginate


async def db_create_top_up(db: Session, top_up: schemas.TopUpCreate):
    instance = models.TopUp(**top_up.model_dump())
    db.add(instance)
    db.commit()
    db.refresh(instance)
    return instance


async def db_get_top_up(db:Session, txn_id:str):
    top_up = db.query(models.TopUp).filter(models.TopUp.txn_id == txn_id).first()
    return top_up


async def db_list_top_ups(db:Session):
    return paginate(db, select(models.TopUp).order_by(models.TopUp.date))
