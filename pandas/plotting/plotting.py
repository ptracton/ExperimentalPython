#! /usr/bin/env python3

import logging
import sys

import PyQt5
import PyQt5.QtWidgets

import UI

if __name__ == "__main__":

    # Start our log, now any module in this application
    # can import logging and write out details
    logging.basicConfig(filename="plotting.log",
                        level=logging.DEBUG,
                        format='%(asctime)s,%(levelname)s,%(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')
    logging.info("Template Started")
    
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    gui = UI.UI()
    gui.show()
    app.exec_()
