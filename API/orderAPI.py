from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

api = FastAPI()
models.Base.metadata.create_all(bind=engine)

# data validation (input schema)
class OrderBase(BaseModel):
    # don't input the order_id becuse it's auto increment
    order_date: str
    order_status: str

# database dependencies
def get_db():
    db = SessionLocal()
    try :
        yield db
    finally : 
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# endpoint
@api.post("/order/", status_code=status.HTTP_201_CREATED)
async def create_order(order:OrderBase, db:db_dependency):
    db_user = models.Order(**order.dict())
    db.add(db_user)
    db.commit()

