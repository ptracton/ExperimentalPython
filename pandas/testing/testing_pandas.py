#! /usr/bin/env python3

import numpy as np
import pandas as pd
import scipy.stats

if __name__ == "__main__":
    print("Pandas Testing")
    stocksDir = "../stocks/"
    medtronicStocks = stocksDir + "mdt.us.txt"
    medtronicDataFrame = pd.read_csv(medtronicStocks)
    print(type(medtronicDataFrame))
    columns = medtronicDataFrame.columns.tolist()
    print(columns)
    print(medtronicDataFrame['Open'].mean())
    print(medtronicDataFrame['Open'].median())
    print(medtronicDataFrame['Open'].idxmax())
    print(medtronicDataFrame['Open'].max())
    print(medtronicDataFrame['Open'].idxmin())
    print(medtronicDataFrame['Open'].min())
    print(np.std(medtronicDataFrame['Open']))
    print(scipy.stats.tstd(medtronicDataFrame['Open']))
