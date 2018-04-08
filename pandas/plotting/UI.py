"""
This is an example of a basic UI top level module.
Most of the GUI work is handled in the "central" widget.
This level handles signal/slot connections so all the different
level can interact
"""

import logging

import numpy as np
import pandas as pd

import PyQt5
import PyQt5.QtCore
import PyQt5.QtWidgets

import Stock
import UI_Widget


class UI(PyQt5.QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        """
        Our constructor.  This function sets up the main
        UI elements and the connections
        """

        super(UI, self).__init__(parent)

        self.statusBar().showMessage('Statusbar')

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        helpMenu = menubar.addMenu('&Help')

        exitAction = PyQt5.QtWidgets.QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(PyQt5.QtWidgets.qApp.quit)
        fileMenu.addAction(exitAction)

        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAction)

        # This is our main UI element.  All of parts are inside of it
        self.central = UI_Widget.UI_Widget()

        # connecting the button in the UI_Widget to a callback function at this level
        self.central.stockAnalysisPushButton.clicked.connect(
            self.stockAnalysisPushButtonClicked)

        self.setCentralWidget(self.central)
        self.setWindowTitle('Stock Analysis')
        self.show()

        return

    def stockAnalysisPushButtonClicked(self):
        stockName = self.central.stocksComboBox.currentText()
        stocksDir = "../stocks/"
        stockFileName = stocksDir + stockName.lower() + ".us.txt"

        print("stockAnalysisPushButtonClicked {}".format(stockName))
        logging.debug("stockAnalysisPushButtonClicked {}".format(stockName))

        stockInstance = Stock.Stock(stockName=stockName)
        stockInstance.read_csv()
        self.central.plot.plot(stockInstance.stockDataFrame['Open'])
        return
