"""
This is a wrapper around the Open Movie Database python API module.
"""

import logging
import os
import sys
import traceback

import omdb
import requests


class OpenMovie():
    """
    """

    def __init__(self, title=None, tomatoes=False):
        self.title = title
        self.client = omdb.OMDBClient(apikey=os.environ['OMDB_API_KEY'])
        self.posterFileName = None
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
            self.posterFileName= "NO POSTER"
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
