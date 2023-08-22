from sqlalchemy import Column, Integer, String, Date
from database import Base

class Order(Base):

    __tablename__ = 'order'

    order_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_date = Column(Date)
    order_status = Column(String(25))
