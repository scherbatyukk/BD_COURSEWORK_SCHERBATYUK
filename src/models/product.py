from sqlalchemy import Column, Integer, Numeric, String, Date, func
from sqlalchemy.orm import relationship
from db import Base
from models.links import links_products_categories, links_products_orders

class Product(Base):
    __tablename__ = 'Product'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    brand = Column(String)
    manufacturer = Column(String)
    manufacture_date = Column(Date, default=func.now())
    cost = Column(Numeric)
    Orders = relationship("Order", secondary=links_products_orders, cascade="all, delete")
    Categories = relationship("Category", secondary=links_products_categories, cascade="all, delete")

    def __repr__(self):
      return "<Product(name='%s'," \
             " brand='%s'," \
             " manufacturer='%s'," \
             " manufacture_date='%s'," \
             " cost=%i, " % \
             (self.name,
              self.brand,
              self.manufacturer,
              self.manufacture_date,
              self.cost)

    def __init__(self,
                 name: str,
                 brand: str,
                 manufacturer: str,
                 manufacture_date: str,
                 cost: int):
        self.name = name
        self.brand = brand
        self.manufacturer = manufacturer
        self.manufacture_date = manufacture_date
        self.cost = cost
