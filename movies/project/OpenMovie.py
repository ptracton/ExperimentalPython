"""
This is a wrapper around the Open Movie Database python API module.
"""

import json
import logging
import os
import re
import sys
import traceback

import bs4
import omdb
import requests

import numpy as np
import pandas as pd
import sqlalchemy

import ORM


class OpenMovie():
    """
    """

    def __init__(self, title=None, tomatoes=False):
        self.title = title
        self.client = omdb.OMDBClient(apikey=os.environ['OMDB_API_KEY'])
        self.posterFileName = None
        self.awardsDict = {}

        self.monthlyBudget = []
        self.monthlyRevenue = []
        self.monthlyMaxRevenue = []
        self.monthlyMovieCount = []
        self.monthlyMovieTitles = []

        self.monthlyRevenueMean = []
        self.monthlyRevenueMedian = []
        self.monthlyRevenueStd = []

        self.monthlyBudgetMean = []
        self.monthlyBudgetMedian = []
        self.monthlyBudgetStd = []

        self.annualBudgetMean = []
        self.annualBudgetMedian = []
        self.annualBudgetStd = []

        self.annualRevenueMean = []
        self.annualRevenueMedian = []
        self.annualRevenueStd = []

        try:
            os.mkdir("Posters")
        except:
            pass

        try:
            self.movie = self.client.get(title=title, tomatoes=tomatoes)
        except Exception:
            logging.error("FAILED to get movie {}".format(title))
            print(traceback.format_exc())
            logging.error(traceback.format_exc())
        return

    def getPoster(self):
        """
        Download the poster for this title and save with the same name
        """

        if 'poster' not in self.movie:
            self.posterFileName = "NO POSTER"
            logging.error("No poster for {}".format(self.title))
            return False

        poster_url = self.movie['poster']

        try:
            r = requests.get(poster_url)
        except Exception:
            logging.error("FAILED to download poster for {}".format(title))
            print(traceback.format_exc())
            logging.error(traceback.format_exc())
            return False

        self.title = self.title.replace("/", " ")
        self.title = self.title.replace("?", " ")
        self.title = self.title.replace(":", " ")
        self.title = self.title.replace(" ", "_")
        self.posterFileName = "Posters/"+self.title+".jpg"
        try:
            open(self.posterFileName, 'wb').write(r.content)
        except:
            logging.error(
                "FAILED to save poster for {}".format(self.posterFileName))
            print(traceback.format_exc())
            logging.error(traceback.format_exc())
            return False

        return True

    def getAwards(self):
        """
        Get a list of awards from IMDB movie page
        """

        if 'imdb_id' not in self.movie:
            logging.error("No IMDB entry for {}".format(self.title))

        imdb_url = "https://www.imdb.com/title/{}/awards?ref_=tt_awd".format(
            self.movie['imdb_id'])

        r = requests.get(imdb_url)
        soup = bs4.BeautifulSoup(r.text, "lxml")
        data = []
        table = soup.find('table', attrs={'class': 'awards'})

        if table is None:
            self.awardsDict = {}
            return

        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])  # Get rid of empty values

        index = 0
        for x in data:
            # print(x)
            nominee = re.search('Nominee', x[0])
            if nominee:
                break
            else:
                if index == 0:
                    awards = x[1].split('\n')
                    y = awards[1:]
                    while '' in y:
                        y.remove('')
                        self.awardsDict[awards[0]] = y
                else:
                    awards = x[0].split('\n')
                    y = awards[1:]
                    while '' in y:
                        y.remove('')
                    self.awardsDict[awards[0]] = y

            index = index + 1
        # print(awards_dict)
        # for k, v in self.awardsDict.items():
        #    print("Award: {:40} Winner: {:40}".format(k, ", ".join(v)))

        return self.awardsDict

    def getCast(self):
        """
        Get the cast list for the movie
        """

        try:
            movieCreditsQuery = ORM.session.query(
                ORM.Credits).filter(ORM.Credits.title == self.title)
        except:
            logging.error("getCast failed on ORM query")
            print("getCast failed on ORM query")
            return False

        # Try to get the cast and crew informatioon
        try:
            cast = json.loads(movieCreditsQuery[0].cast)
        except:
            logging.error(
                "getCast: Failed to retrieve movie or credits"
            )
            print(traceback.format_exc())
            logging.error(traceback.format_exc())

            return False

        return cast

    def getCrew(self):
        """
        Get the director and the crew for the movie
        """
        director = "NONE"
        print(self.title)
        try:
            movieCreditsQuery = ORM.session.query(
                ORM.Credits).filter(ORM.Credits.title == self.title)
        except:
            logging.error("getCast failed on ORM query")
            print("getCrew failed on ORM query")
            return False, False

        # Try to get the cast and crew informatioon
        try:
            crew = json.loads(movieCreditsQuery[0].crew)
        except:
            logging.error(
                "getCrew: Failed to retrieve credits"
            )
            print(traceback.format_exc())
            logging.error(traceback.format_exc())

            return False, False

        try:
            for x in crew:
                if x['job'] == 'Director':
                    director = x['name']
        except:
            logging.error("No crew or director")
            print("No crew or director")
            return False

        return director, crew

    def getMovieTitleData(self):
        """
        Get the database information for this title
        """
        # Query the database for all movies with this title
        try:
            movieTitleQuery = ORM.session.query(
                ORM.Movies).filter(ORM.Movies.title == self.title).one()
        except sqlalchemy.orm.exc.NoResultFound:
            logging.error("Movie Not in Database {}".format(movieTitle))
            #print("Movie Not in Database {}".format(movieTitle))
            return False

        return movieTitleQuery

    def analyzeMovie(self, year=None, month=None):
        """
        Analyze the year of this film
        """
        if year is None or month is None:
            return False

        print("Analyze Year {} {}".format(year, month))
        months = range(1, 13)
        print("MONTHS {}".format(months))

        for m in months:
            nextMonth = m + 1
            startOfMonth = "{}-{:02d}-01".format(year, m)
            if nextMonth == 13:
                endOfMonth = "{}-{:02d}-01".format(year + 1, 1)
            else:
                endOfMonth = "{}-{:02d}-01".format(year, nextMonth)

                # print("\nSTART: {}  END {}".format(startOfMonth, endOfMonth))

            movieTitleSQL = """select * from public."Movies" where release_date>'{}' and release_date <'{}';""".format(
                startOfMonth, endOfMonth)
            monthlyMovieDataFrame = pd.read_sql(movieTitleSQL,
                                                ORM.db.raw_connection())
            self.monthlyBudget.append(monthlyMovieDataFrame['budget'].sum())
            self.monthlyRevenue.append(monthlyMovieDataFrame['revenue'].sum())

            self.monthlyRevenueMean.append(np.nanmean(monthlyMovieDataFrame['revenue']))
            self.monthlyRevenueStd.append(np.nanstd(monthlyMovieDataFrame['revenue']))
            self.monthlyRevenueMedian.append(np.nanmedian(monthlyMovieDataFrame['revenue']))

            self.monthlyBudgetMean.append(np.nanmean(monthlyMovieDataFrame['budget']))
            self.monthlyBudgetStd.append(np.nanstd(monthlyMovieDataFrame['budget']))
            self.monthlyBudgetMedian.append(np.nanmedian(monthlyMovieDataFrame['budget']))

            monthlyMovieDataFrame.set_index('title')
            # print("Month: {}".format(m))
            # print("Monthyl DataFrame {}".format(monthlyMovieDataFrame))
            # for row in monthlyMovieDataFrame.iterrows():
            #    movie = row[1].to_dict()
            #    print("\tTITLE:{:40} RELEASE {:8} BUDGET {:10} REVENUE {:10}".
            #          format(movie['title'], movie['release_date'],
            #                 movie['budget'], movie['revenue']))

        startOfYear = "{}-01-01".format(year)
        endOfYear = "{}-01-01".format(int(year) + 1)
        movieTitleSQL = """select * from public."Movies" where release_date>'{}' and release_date <'{}';""".format(
            startOfYear, endOfYear)

        yearMovieDataFrame = pd.read_sql(movieTitleSQL,
                                         ORM.db.raw_connection())
        self.annualBudget = yearMovieDataFrame['budget'].sum()
        self.annualRevenue = yearMovieDataFrame['revenue'].sum()
        numberOfMovies = len(yearMovieDataFrame['revenue'])

        self.annualRevenueMean.append(np.nanmean(yearMovieDataFrame['revenue']))
        self.annualRevenueStd.append(np.nanstd(yearMovieDataFrame['revenue']))
        self.annualRevenueMedian.append(np.nanmedian(yearMovieDataFrame['revenue']))

        self.annualBudgetMean.append(np.nanmean(yearMovieDataFrame['budget']))
        self.annualBudgetStd.append(np.nanstd(yearMovieDataFrame['budget']))
        self.annualBudgetMedian.append(np.nanmedian(yearMovieDataFrame['budget']))

        print("Annual Budget {:,.2f}".format(self.annualBudget))
        print("Annual Revenue {:,.2f}".format(self.annualRevenue))
        print("Number Of Movies {:,.2f}".format(numberOfMovies))
        print("Annual Revenue Mean {:,.2f}".format(self.annualRevenueMean[0]))
        print("Annual Revenue Median {:,.2f}".format(self.annualRevenueMedian[0]))
        print("Annual Revenue Std {:,.2f}".format(self.annualRevenueStd[0]))
        print("Annual Budget Mean {:,.2f}".format(self.annualBudgetMean[0]))
        print("Annual Budget Median {:,.2f}".format(self.annualBudgetMedian[0]))
        print("Annual Budget Std {:,.2f}".format(self.annualBudgetStd[0]))

        for m in months:
            print("Month {}  Budget {:,.2f} Revenue {:,.2f} Mean {:,.2f} Median {:,.2f} Std {:,.2f}".format(
                m, self.monthlyBudget[m - 1], self.monthlyRevenue[m - 1],
                self.monthlyRevenueMean[m-1], self.monthlyRevenueMedian[m -
                                                                        1],  self.monthlyRevenueStd[m-1]
            )
            )
