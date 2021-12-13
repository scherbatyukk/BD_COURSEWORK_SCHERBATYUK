from CUI.constructor import CUI
from visualzation.graphs import getTop15Categories,\
    getManufactureDateStat,\
    getTransactionDateStat,\
    getTotalMoneyPerYear


class GraphsView(object):
    def __init__(self):
        self.CUI = CUI('Graphs menu')
        self.CUI.addField('Top 15 categories', lambda: getTop15Categories())
        self.CUI.addField('Products per year statistic', lambda: getManufactureDateStat())
        self.CUI.addField('Sale statistics', lambda: getTransactionDateStat())
        self.CUI.addField('Get total money per year', lambda: getTotalMoneyPerYear())

    def run(self):
        self.CUI.run()

