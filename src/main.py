from db import session, recreate_database
from views.modelView import EntityView
from CUI.constructor import CUI
from models.client import Client
from models.order import Order
from models.category import Category
from models.product import Product

from views.graphsView import GraphsView
from views.dataView import DataView
from views.searchView import SearchView


if __name__ == '__main__':
    #recreate_database()
    cui = CUI('CUI')
    cui.addMenu('Models')
    cui.addField('Clients', lambda: EntityView(Client).run())
    cui.addField('Orders', lambda: EntityView(Order).run())
    cui.addField('Categories', lambda: EntityView(Category).run())
    cui.addField('Products', lambda: EntityView(Product).run())
    cui.finishMenu()

    cui.addField('Graphs', lambda: GraphsView().run())
    cui.addField('Data', lambda: DataView().run())
    cui.addField('Search', lambda: SearchView().run())

    cui.run()
    session.close()


