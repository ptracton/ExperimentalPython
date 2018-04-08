import logging
import os

import PyQt5
import PyQt5.QtCore
import PyQt5.QtWidgets

import pyqtgraph as pg

class UI_Widget(PyQt5.QtWidgets.QDialog):
    def __init__(self, parent=None):
        """
        This is the layer that handles creating and displaying the various
        UI elements in the central window
        """

        super(UI_Widget, self).__init__(parent)
        hbox = PyQt5.QtWidgets.QHBoxLayout()
        vbox = PyQt5.QtWidgets.QVBoxLayout()

        label = PyQt5.QtWidgets.QLabel("Select a Stock")
        self.stocksComboBox = PyQt5.QtWidgets.QComboBox()
        self.stockAnalysisPushButton = PyQt5.QtWidgets.QPushButton(
            "Analyze Stock")

        hbox.addWidget(label)
        hbox.addWidget(self.stocksComboBox)
        hbox.addWidget(self.stockAnalysisPushButton)

        self.getListOfStocks()

        self.plot = pg.PlotWidget()
        self.plot.setWindowTitle("Stock Analysis")
        self.plot.showGrid(x=True, y=True)
        self.plot.setLabel(axis='left', text='Y Axis', units='y units')
        self.plot.setLabel(axis='bottom', text='x Axis', units='x units')

        
        vbox.addLayout(hbox)
        vbox.addWidget(self.plot)
        
        self.setLayout(vbox)
        return

    def getListOfStocks(self):
        """
        Get out list of stocks from the CSV files in the ../stocks/
        directory and add them to the combo box for selection
        """

        stocksDir = "../stocks/"
        stocksListDir = os.listdir(stocksDir)
        logging.debug("{}".format(stocksListDir))
        print("{}".format(stocksListDir))
        
        correctedStocks = []
        for stock in stocksListDir:
            s = stock.split(".")
            correctedStocks.append(s[0].upper())
        

        self.stocksComboBox.addItems(correctedStocks)
        return
