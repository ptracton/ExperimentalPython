"""
This is the top level UI for the Python Movies Project
At this level we instantiate the Central Window which has the
GUI elements.  This is also the level of handling signal/slot connections.
"""
import datetime
import json
import logging

import numpy as np
import pandas as pd

import PyQt5
import PyQt5.QtWidgets
import sqlalchemy

import OpenMovie
import ORM
import UI_CentralWindow


class UI(PyQt5.QtWidgets.QMainWindow):
    """
    Top level UI class
    """

    def __init__(self, parent=None):
        super(UI, self).__init__(parent)
        # Create Main Window Elements
        self.statusBar().showMessage('Status Bar')
        self.setWindowTitle('Python Movie Project')

        # Create our central widget
        self.centralWidget = UI_CentralWindow.UI_CentralWindow()
        self.setCentralWidget(self.centralWidget)

        # Connect signals and slots
        self.centralWidget.enterMoviePushButton.clicked.connect(
            self.enterMoviePushButtonClicked)
        # Display
        self.show()

    def enterMoviePushButtonClicked(self):
        """
        Callback function for the enterMoviePushButton button object is clicked
        """

        # Read the movie title from the GUI.  This is UNSAFE data.  Never trust a USER!
        movieTitle = self.centralWidget.enterMovieLineEdit.text()
        print("Movie Title {}".format(movieTitle))

        # Get our data
        openMovie = OpenMovie.OpenMovie(title=movieTitle)
        cast = openMovie.getCast()
        director, crew = openMovie.getCrew()
        movieTitleQuery = openMovie.getMovieTitleData()
        year, month, day = movieTitleQuery.release_date.split('-')
        awardsDict = openMovie.getAwards()
        month = int(month)
        openMovie.analyzeMovie(year=int(year), month=month)

        self.statusBar().showMessage("Start Getting Poster")
        if (openMovie.getPoster() is False):
            return
        self.statusBar().showMessage("Done Getting Poster")

        # Upate the GUI
        self.centralWidget.directorInformation.infoLabel.setText(director)
        self.centralWidget.actorInformation.infoLabel.setText(cast[0]['name'])
        self.centralWidget.releaseDateInformation.infoLabel.setText(
            movieTitleQuery.release_date)
        self.centralWidget.budgetInformation.infoLabel.setText(
            "{:,.2f}".format(movieTitleQuery.budget))
        self.centralWidget.revenueInformation.infoLabel.setText(
            "{:,.2f}".format(movieTitleQuery.revenue))
        self.centralWidget.runTimeInformation.infoLabel.setNum(
            movieTitleQuery.runtime)
        self.centralWidget.voteCountInformation.infoLabel.setText(
            "{:,.2f}".format(movieTitleQuery.vote_count))
        self.centralWidget.voteAverageInformation.infoLabel.setText(
            "{:,.2f}".format(movieTitleQuery.vote_average))
        self.centralWidget.statusInformation.infoLabel.setText(
            movieTitleQuery.status)

        self.centralWidget.annualRevenueMean.infoLabel.setText(
            "{:,.2f}".format(openMovie.annualRevenueMean[0]))
        self.centralWidget.annualRevenueMedian.infoLabel.setText(
            "{:,.2f}".format(openMovie.annualRevenueMedian[0]))
        self.centralWidget.annualRevenueStd.infoLabel.setText(
            "{:,.2f}".format(openMovie.annualRevenueStd[0]))

        self.centralWidget.monthlyRevenueMean.infoLabel.setText(
            "{:,.2f}".format(openMovie.monthlyRevenueMean[month-1]))
        self.centralWidget.monthlyRevenueMedian.infoLabel.setText(
            "{:,.2f}".format(openMovie.monthlyRevenueMedian[month-1]))
        self.centralWidget.monthlyRevenueStd.infoLabel.setText(
            "{:,.2f}".format(openMovie.monthlyRevenueStd[month-1]))

        self.centralWidget.updatePoster(openMovie.posterFileName)

        self.centralWidget.awardsDisplay.clear()
        self.centralWidget.updateAwards(awardsDict)
        self.centralWidget.matplot.addBars(
            x=range(1, 13), revenue=openMovie.monthlyRevenue, budget=openMovie.monthlyBudget, year=year)

        return
