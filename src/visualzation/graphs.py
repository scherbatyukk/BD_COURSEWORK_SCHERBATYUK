import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from db import session
from models.category import Category
from models.product import Product
from models.order import Order
from sqlalchemy import func, Integer


def getTop15Categories():
    try:
        results = session.query(Category.name, func.count(Category.name).label('count')) \
            .join(Product, Category.Products) \
            .group_by(Category.name) \
            .order_by(func.count('count').desc()) \
            .limit(15).all()

        listed = list(zip(*results))

        series = pd.Series(np.array(listed[1]), index=listed[0], name='')

        series.plot.pie(figsize=(9, 7), title="Top 15 categories:")

        plt.plot(series)
        plt.show()
    except Exception as err:
        print(err)
        exit(1)


def getManufactureDateStat():
    results = session.query(func.extract('year', Product.manufacture_date).cast(Integer).label('year'),
                            func.count('year')) \
        .group_by('year') \
        .order_by('year').all()

    listed = list(zip(*results))

    ts = pd.DataFrame(np.array(listed[1]), listed[0])

    ts.plot(kind='bar', figsize=(9, 7), title="Products per year")
    plt.plot(ts)
    plt.show()


def getTransactionDateStat():
    results = session.query(func.extract('year', Order.transaction_date).cast(Integer).label('year'), func.count('year')) \
        .group_by('year') \
        .order_by('year').all()

    listed = list(zip(*results))

    ts = pd.DataFrame(np.array(listed[1]), listed[0])

    ts.plot(kind='bar', figsize=(9, 7), title="Sale statistics")
    plt.plot(ts)
    plt.show()


def getTotalMoneyPerYear():
    results = session.query(func.sum(Product.cost).label('sum'),
                           func.extract('year', Order.transaction_date).cast(Integer).label('year'))\
        .join(Product.Orders)\
        .group_by('year')\
        .order_by('year').all()

    listed = list(zip(*results))
    series = pd.DataFrame(np.array([int(num) for num in listed[0]]), index=listed[1])
    series.plot(figsize=(9, 7), title="Total money per year")
    plt.plot(series)
    plt.show()