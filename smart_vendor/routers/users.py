from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page
from sqlalchemy.orm import Session

from smart_vendor import schemas
from smart_vendor.db_services.users import db_create_user, db_get_user, db_update_user, db_delete_user, db_patch_user, \
    db_get_users
from smart_vendor.dependancies import get_db_session

router = APIRouter()


@router.post("/users/", response_model=schemas.UserRead)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db_session)):
    db_user = await db_create_user(db, user)
    return db_user


@router.get("/users/{user_id}", response_model=schemas.UserRead)
async def read_user(user_id: str, db: Session = Depends(get_db_session)):
    db_user = await db_get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/users/")
async def list_users(db: Session = Depends(get_db_session)) -> Page[schemas.UserRead]:
    users = await db_get_users(db)
    return users


@router.put("/users/{user_id}", response_model=schemas.UserRead)
async def update_user(user_id: str, user_update: schemas.UserUpdate, db: Session = Depends(get_db_session)):
    db_user = await db_update_user(db, user_id, user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.patch("/users/{user_id}", response_model=schemas.UserRead)
async def patch_user(user_id: str, user_update: schemas.UserPatch, db: Session = Depends(get_db_session)):
    db_user = await db_patch_user(db, user_id, user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.delete("/users/{user_id}", response_model=schemas.UserRead)
async def delete_user(user_id: str, db: Session = Depends(get_db_session)):
    db_user = await db_delete_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
