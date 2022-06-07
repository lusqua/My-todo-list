from fastapi import APIRouter, Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from db import crud, models, schemas
from controllers import helper


router = APIRouter()


@router.post("/{user_id}/items/", response_model=schemas.Item, tags=["items"])
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(helper.get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@router.get("/", response_model=list[schemas.Item], tags=["items"])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(helper.get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items