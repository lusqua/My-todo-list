from fastapi import APIRouter, Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from db import crud, models, schemas
from controllers import helper


router = APIRouter()

@router.post("/", response_model=schemas.User , tags=["users"])
def create_user(user: schemas.UserCreate, db: Session = Depends(helper.get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@router.get("/", response_model=list[schemas.User] , tags=["users"])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(helper.get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=schemas.User , tags=["users"])
def read_user(user_id: int, db: Session = Depends(helper.get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user