from CUI.constructor import CUI
from parsingData.parseCsv import parse1, parse2
from scrapping.amazon import getProductsByCategory
from randomizing.generateData import generateOrders, generateClients, generateOrderRelation


class DataView(object):
    def __init__(self):
        self.CUI = CUI('New data menu')
        self.CUI.addField('Scrapping', lambda: self.__scrapping())
        self.CUI.addField('Parsing', lambda: self.__parsingDataSets())
        self.CUI.addField('Randomizing', lambda: self.__randomizing())


    def run(self):
        self.CUI.run()

    def __scrapping(self):
        localMenu = CUI('Scrapping data')
        try:
            localMenu.addField('Get data from Amazon', lambda: getProductsByCategory())
        except Exception as err:
            localMenu.setMsg(str(err))
        localMenu.run()

    def __parsingDataSets(self):
        localMenu = CUI('Parsing CSV datasets')
        try:
            localMenu.addField('Parse set 1', lambda: parse1())
            localMenu.addField('Parse set 2', lambda: parse2())
        except Exception as err:
            localMenu.setMsg(str(err))
        localMenu.run()

    def __randomizing(self):
        localMenu = CUI('Randomizing data')
        try:
            localMenu.addField('Generate Clients', lambda: generateClients())
            localMenu.addField('Generate Orders', lambda: generateOrders())
            localMenu.addField('Generate Order-Product relations', lambda: generateOrderRelation())
        except Exception as err:
            localMenu.setMsg(str(err))
        localMenu.run()



