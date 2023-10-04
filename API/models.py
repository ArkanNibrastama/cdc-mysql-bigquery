from sqlalchemy import Column, Integer, String, Date
from database import Base

class Order(Base):

    __tablename__ = 'order'

    order_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer)
    product_category_id = Column(Integer)
    order_date = Column(Date)
    origin_office = Column(String(30))
    destination_office = Column(String(30))
    order_status = Column(String(25))