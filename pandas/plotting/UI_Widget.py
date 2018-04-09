import logging
import os

import PyQt5
import PyQt5.QtCore
import PyQt5.QtWidgets

import pyqtgraph as pg
import QtMpl

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

        self.pgplot = pg.PlotWidget()
        self.pgplot.addLegend((100,70), offset=(70,30))
        self.pgplot.setWindowTitle("Stock Analysis")
        self.pgplot.showGrid(x=True, y=True)
        self.pgplot.setLabel(axis='left', text='Stock Price', units='$')
        self.pgplot.setLabel(axis='bottom', text='Date', units='days')
        
        #######################################################################
        #
        # Matplotlib object
        #
        #######################################################################
        self.matplot = QtMpl.QtMpl(parent=parent)
        self.line_count = 0
        
        vbox.addLayout(hbox)
        vbox.addWidget(self.pgplot)
        vbox.addWidget(self.matplot)
        
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
