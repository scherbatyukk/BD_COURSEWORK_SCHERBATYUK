from db import session
import time
from models.client import Client
from models.order import Order
from models.product import Product

def inputCount():
    count = input("Enter count of new rows: ")
    if not count.isdigit() or int(count) < 1: raise Exception('Incorrect input')
    return int(count)


def generateClients(*args):
    count = None
    if len(args) == 0:
        count = inputCount()
    else: count = args[0]

    startTime = time.time()
    if len(args) == 0: print('\nRows generating...')

    session.execute(f"INSERT INTO \"Client\" (name, birthday_date, email) "
                    f"SELECT generatestring(10), "
                    f"generatedate(), "
                    f"concat(generatestring(8), '@', generatestring(5), '.com') "
                    f"from generate_series(1, {count})")
    session.commit()

    endTime = time.time()

    if len(args) == 0:
        print('Rows generated! Elapsed time: ' + str(endTime - startTime)[:9] + 's')
        input('\nPress any key to continue...')


def generateOrders(*args):
    count = None
    if len(args) == 0:
        count = inputCount()
    else:
        count = args[0]

    clientsCount = session.query(Client).count()
    startTime = time.time()
    if len(args) == 0: print('\nRows generating...')

    if int(count) / 5 > clientsCount:
        generateClients(int(int(count) / 5) - clientsCount)

    session.execute(f"INSERT INTO \"Order\" (taxes_sum, transaction_date, client_id) "
                    f"SELECT generateint(500)::numeric, "
                    f"generatedate(), "
                    f"getrandomrow('Client')::int "
                    f"FROM generate_series(1, {count})")
    session.commit()

    endTime = time.time()

    if len(args) == 0:
        print('Rows generated! Elapsed time: ' + str(endTime - startTime)[:9] + 's')
        input('\nPress any key to continue...')


def generateOrderRelation(*args):
    count = None
    if len(args) == 0:
        count = inputCount()
    else:
        count = args[0]

    if session.query(Product).count() < 10:
        raise Exception('Too few product in the database. Please scrap or parse some data')
    ordersCount = session.query(Order).count()

    startTime = time.time()
    if len(args) == 0: print('\nRows generating...')

    if int(count) / 10 > ordersCount:
        generateOrders(int(int(count) / 10) - ordersCount)

    session.execute(f"INSERT INTO \"Link_Product-Order\" (product_id, order_id) "
                    f"SELECT getrandomrow('Product')::int, "
                    f"getrandomrow('Order')::int "
                    f"FROM generate_series(1,{count})")
    session.commit()

    endTime = time.time()

    if len(args) == 0:
        print('Rows generated! Elapsed time: ' + str(endTime - startTime)[:9] + 's')
        input('\nPress any key to continue...')

