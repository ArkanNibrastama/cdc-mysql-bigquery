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

class UpdateStatusBase(BaseModel):
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
# add a new order transaction
@api.post("/order/", status_code=status.HTTP_201_CREATED)
async def create_order(order:OrderBase, db:db_dependency):
    input_order = models.Order(**order.dict())
    db.add(input_order)
    db.commit()

# update partial (just the status)
@api.patch("/status/{order_id}", status_code=status.HTTP_200_OK)
async def update_status(order_id:int, status:UpdateStatusBase, db:db_dependency):
    old_status = db.query(models.Order).filter(models.Order.order_id == order_id).first()
    for var, value in vars(status).items():
        setattr(old_status, var, value) if value else None
    db.add(old_status)
    db.commit()