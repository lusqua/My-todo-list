from typing import Union

from fastapi import Depends, FastAPI, HTTPException

from sqlalchemy.orm import Session

from db import crud, models, schemas
from db.database import SessionLocal, engine
from controllers import item_controller, user_controller

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(user_controller.router, prefix="/users", tags=["users"])
app.include_router(item_controller.router, prefix="/items", tags=["items"])
