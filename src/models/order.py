from sqlalchemy import Column, Integer, Numeric, Date, func, ForeignKey
from sqlalchemy.orm import relationship, backref
from db import Base
from models.links import links_products_orders

class Order(Base):
    __tablename__ = 'Order'

    id = Column(Integer, primary_key=True)
    transaction_date = Column(Date, default=func.now())
    taxes_sum = Column(Numeric)
    client_id = Column(Integer, ForeignKey('Client.id', ondelete='CASCADE'))
    Client = relationship("Client", backref=backref("Order", uselist=False, cascade="all,delete"))
    Products = relationship("Product", secondary=links_products_orders, cascade="all, delete")

    def __repr__(self):
      return "<Order(taxes_sum=%i, transaction_date='%s', client_id=%i)>" % \
             (self.taxes_sum, self.transaction_date, self.client_id)

    def __init__(self, transaction_date: str, taxes_sum: int, client_id: int):
        self.taxes_sum = taxes_sum
        self.transaction_date = transaction_date
        self.client_id = client_id

