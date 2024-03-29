from sqlalchemy import select
from sqlalchemy.orm import Session
from smart_vendor import models, schemas


async def _create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    print(f'DB USER: {db_user}')
    return db_user


async def _get_user(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.id == user_id).first()


async def _get_users(db: Session):
    stmt = select(models.User)
    result = db.execute(stmt)
    return result.scalars().all()


async def _update_user(db: Session, user_id: str, user_update: schemas.UserUpdate):
    db_user =  db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        for attr, value in user_update.model_dump().items():
            setattr(db_user, attr, value)
        db.commit()
        db.refresh(db_user)
    return db_user


async def _patch_user(db: Session, user_id: str, user_update: schemas.UserPatch):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()

    if db_user:
        for field, value in user_update.model_dump(exclude_unset=True).items():
            setattr(db_user, field, value)
            db.commit()
            db.refresh(db_user)

    return db_user


async def _delete_user(db: Session, user_id: str):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user
