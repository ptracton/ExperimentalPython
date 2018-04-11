"""
This is the top level UI for the Python Movies Project
At this level we instantiate the Central Window which has the
GUI elements.  This is also the level of handling signal/slot connections.
"""
import datetime
import json
import logging

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

        # Query the database for all movies with this title
        try:
            movieTitleQuery = ORM.session.query(
                ORM.Movies).filter(ORM.Movies.title == movieTitle).one()
        except sqlalchemy.orm.exc.NoResultFound:
            logging.error("Movie Not in Database {}".format(movieTitle))
            return

        year, month, day = movieTitleQuery.release_date.split('-')

        # There must be at least 1 movie with this title, look up the credits for this title.
        movieCreditsQuery = ORM.session.query(
            ORM.Credits).filter(ORM.Credits.title == movieTitle)

        # Try to get the cast and crew informatioon
        try:
            cast = json.loads(movieCreditsQuery[0].cast)
            crew = json.loads(movieCreditsQuery[0].crew)
        except:
            logging.error(
                "enterMoviePushButtonClicked: Failed to retrieve movie or credits"
            )
            return

        director = "NONE"
        for x in crew:
            if x['job'] == 'Director':
                director = x['name']

        # for x in movieTitleQuery:
        #    print("FILM: {:20} TAGLINE: {:40} STARING {:15} DIRECTOR {:15} ".format(x.title, x.tagline, cast[0]['name'], director ))

        self.centralWidget.directorInformation.infoLabel.setText(director)
        self.centralWidget.actorInformation.infoLabel.setText(cast[0]['name'])
        self.centralWidget.releaseDateInformation.infoLabel.setText(
            movieTitleQuery.release_date)
        self.centralWidget.budgetInformation.infoLabel.setText(
            "{:,}".format(movieTitleQuery.budget))
        self.centralWidget.revenueInformation.infoLabel.setText(
            "{:,}".format(movieTitleQuery.revenue))
        self.centralWidget.runTimeInformation.infoLabel.setNum(
            movieTitleQuery.runtime)
        self.centralWidget.voteCountInformation.infoLabel.setText(
            "{:,}".format(movieTitleQuery.vote_count))
        self.centralWidget.voteAverageInformation.infoLabel.setText(
            "{:,}".format(movieTitleQuery.vote_average))
        self.centralWidget.statusInformation.infoLabel.setText(
            movieTitleQuery.status)

        openMovie = OpenMovie.OpenMovie(title=movieTitle)

        self.statusBar().showMessage("Start Getting Poster")
        if (openMovie.getPoster() is False):
            return
        self.centralWidget.updatePoster(openMovie.posterFileName)
        self.statusBar().showMessage("Done Getting Poster")

        self.analyzeYear(int(year))

        return

    def analyzeYear(self, year=None):

        print("Analyze Year {}".format(year))
        months = range(1, 13)
        monthlyBudget = []
        monthlyRevenue = []
        monthlyMaxRevenue = []
        monthlyMovieCount = []
        monthlyMovieTitles = []
        for m in months:
            nextMonth = m + 1
            startOfMonth = "{}-{:02d}-01".format(year, m)
            if nextMonth == 13:
                endOfMonth = "{}-{:02d}-01".format(year + 1, 1)
            else:
                endOfMonth = "{}-{:02d}-01".format(year, nextMonth)

            print("\nSTART: {}  END {}".format(startOfMonth, endOfMonth))

            movieTitleSQL = """select * from public."Movies" where release_date>'{}' and release_date <'{}';""".format(
                startOfMonth, endOfMonth)
            monthlyMovieDataFrame = pd.read_sql(movieTitleSQL,
                                                ORM.db.raw_connection())
            monthlyBudget.append(monthlyMovieDataFrame['budget'].sum())
            monthlyRevenue.append(monthlyMovieDataFrame['revenue'].sum())

            monthlyMovieDataFrame.set_index('title')
            print("Month: {}".format(m))
            #print("Monthyl DataFrame {}".format(monthlyMovieDataFrame))
            for row in monthlyMovieDataFrame.iterrows():
                movie = row[1].to_dict()
                print("\tTITLE:{:40} RELEASE {:8} BUDGET {:10} REVENUE {:10}".
                      format(movie['title'], movie['release_date'],
                             movie['budget'], movie['revenue']))

                #print("\tMOVIE: {} ".format(movie))
                #monthlyMovieTitles.append(title)
                #print("\t{} {}".format(title, monthlyMovieDataFrame['title'], monthlyMovieDataFrame.loc[[2]] ))
            #maxRev = monthlyMovieDataFrame['revenue'].max()
            #print(maxRev)


#            movieTitleSQL = """select * from public."Movies" where release_date>'{}' and release_date <'{}' and revenue = {};""".format(startOfMonth, endOfMonth, int(maxRev))
#            maxMovieDataFrame = pd.read_sql(movieTitleSQL, ORM.db.raw_connection())
#            monthlyMaxRevenue.append(maxMovieDataFrame['title'])

        startOfYear = "{}-01-01".format(year)
        endOfYear = "{}-01-01".format(int(year) + 1)
        movieTitleSQL = """select * from public."Movies" where release_date>'{}' and release_date <'{}';""".format(
            startOfYear, endOfYear)

        yearMovieDataFrame = pd.read_sql(movieTitleSQL,
                                         ORM.db.raw_connection())
        annualBudget = yearMovieDataFrame['budget'].sum()
        annualRevenue = yearMovieDataFrame['revenue'].sum()
        numberOfMovies = len(yearMovieDataFrame['revenue'])

        print("Annual Budget {:,}".format(annualBudget))
        print("Annual Revenue {:,}".format(annualRevenue))
        print("Number Of Movies {:,}".format(numberOfMovies))
        for m in months:
            print("Month {}  Budget {:,} Revenue {:,}".format(
                m, monthlyBudget[m - 1], monthlyRevenue[m - 1],
                monthlyRevenue[m - 1]))
            self.centralWidget.matplot.addBar(x=m, y=monthlyRevenue[m - 1])
        """
        openMovieList = []
        self.statusBar().showMessage("Start Open Movie Downloading....")
        print(type(yearMovieDataFrame))
        for x in yearMovieDataFrame['original_title']:
            m = OpenMovie.OpenMovie(title=x, tomatoes=True)
            if 'title' in m.movie.keys():
                print("TITLE {}  DIRECTOR {} ACTORS {} IMDB RATING {}  META {}  TOMATO {}".format(
                    m.movie['title'],
                    m.movie['director'],
                    m.movie['actors'],
                    m.movie['imdb_rating'],
                    m.movie['metascore'],
                    m.movie['tomato_rating']
                ))

        self.statusBar().showMessage("Done Open Movie Downloading")
        """

        return
