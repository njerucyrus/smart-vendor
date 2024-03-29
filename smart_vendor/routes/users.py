from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from smart_vendor import schemas
from smart_vendor.crud.users import _create_user, _get_user, _update_user, _delete_user, _patch_user, _get_users
from smart_vendor.dependancies import get_db


router = APIRouter()


@router.post("/users/", response_model=schemas.UserRead)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    db_user = await _create_user(db, user)
    return db_user


@router.get("/users/{user_id}", response_model=schemas.UserRead)
async def read_user(user_id: str, db: Session = Depends(get_db)):
    db_user = await _get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/users/", response_model=List[schemas.UserRead])
async def list_users(db: Session = Depends(get_db)):
    users = await _get_users(db)
    return users


@router.put("/users/{user_id}", response_model=schemas.UserRead)
async def update_user(user_id: str, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = await _update_user(db, user_id, user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.patch("/users/{user_id}", response_model=schemas.UserRead)
async def patch_user(user_id: str, user_update: schemas.UserPatch, db: Session = Depends(get_db)):
    db_user = await _patch_user(db, user_id, user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.delete("/users/{user_id}", response_model=schemas.UserRead)
async def delete_user(user_id: str, db: Session = Depends(get_db)):
    db_user = await _delete_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
