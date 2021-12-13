from sqlalchemy import Column, Integer, String
from db import Base
from sqlalchemy.orm import relationship, backref
from models.links import links_products_categories

class Category(Base):
    __tablename__ = 'Category'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    Products = relationship("Product", secondary=links_products_categories, cascade="all, delete")

    def __repr__(self):
      return "<Category(name='%s', type='%s')>" % \
             (self.name, self.type)

    def __init__(self, name: str, type: str):
        self.name = name
        self.type = type


