import logging
import pandas as pd


class Stock():
    def __init__(self, stockName=None):
        """
        This is a class for handling a specific stock and its analysis
        """
        self.stockName = stockName
        self.stockCSVFile = "../stocks/" + stockName.lower() + ".us.txt"
        self.stockDataFrame = None
        return

    def read_csv(self):
        """
        Read the CSV file into a DataFrame in this class
        """

        try:
            self.stockDataFrame = pd.read_csv(self.stockCSVFile)
        except:
            logging.error("Failed to read {}".format(self.stockCSVFile))

        return
