from sqlalchemy import Column, Integer, Table, ForeignKey
from db import Base

links_products_orders = Table(
    'Link_Product-Order', Base.metadata,
    Column('product_id', Integer, ForeignKey('Product.id', ondelete='CASCADE')),
    Column('order_id', Integer, ForeignKey('Order.id', ondelete='CASCADE'))
)

links_products_categories = Table(
    'Link_Product-Category', Base.metadata,
    Column('product_id', Integer, ForeignKey('Product.id', ondelete='CASCADE')),
    Column('category_id', Integer, ForeignKey('Category.id', ondelete='CASCADE'))
)

