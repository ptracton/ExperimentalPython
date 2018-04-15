"""
This is a wrapper around the Open Movie Database python API module.
"""

import logging
import os
import re
import sys
import traceback

import bs4
import omdb
import requests


class OpenMovie():
    """
    """

    def __init__(self, title=None, tomatoes=False):
        self.title = title
        self.client = omdb.OMDBClient(apikey=os.environ['OMDB_API_KEY'])
        self.posterFileName = None
        self.awardsDict = {}
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
