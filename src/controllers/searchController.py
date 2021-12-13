from db import session
from models.product import Product
from models.order import Order
from models.category import Category
from sqlalchemy import func


class SearchController(object):

    def getProductsByCostRange(self, min: int, max: int, *args):
        try:
            if len(args) == 0:
                return session.query(Product.id, Product.name, Product.cost) \
                    .filter(Product.cost > min, Product.cost < max) \
                    .order_by(Product.cost).all()
            else:
                return session.query(Product.id, Product.name, Product.cost) \
                    .filter(Product.cost > min, Product.cost < max) \
                    .order_by(Product.cost)\
                    .limit(args[1])\
                    .offset(args[0] * args[1]).all()
        except Exception as err:
            print("Get error! ", err)

    def getAllClientOrders(self, client_id: int):
        try:
            return session.query(Order.id, Order.transaction_date, Order.taxes_sum)\
                .filter(Order.client_id == client_id)\
                .order_by(Order.transaction_date).all()
        except Exception as err:
            raise str(err)

    def getAllProductCategories(self, product_id: int):
        try:
            return session.query(Product.id, func.array_agg(Product.name), func.array_agg(Category.name))\
                .join(Product.Categories)\
                .filter(Product.id == product_id)\
                .group_by(Product.id).all()
        except Exception as err:
            raise str(err)
