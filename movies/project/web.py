#! /usr/bin/env python3

import logging
import os
import sys

import flask
import jinja2

import OpenMovie
import ORM

app = flask.Flask(__name__)
env = jinja2.Environment(
    loader=jinja2.PackageLoader(__name__,
                                'templates'))
app.secret_key = "randometksdfjsdfd"


def ask_for_movie():
    """
    Form to ask which movie to display
    """
    template = env.get_template('ask_movie.html')
    html = template.render()
    return html


def display_movie():
    """
    Collects the information about the movie and displays it
    """
    movieTitle = str(flask.request.form['MOVIE'])
    string = "Display Movie: {}".format(movieTitle)

    # Get our data
    openMovie = OpenMovie.OpenMovie(title=movieTitle)
    cast = openMovie.getCast()
    director, crew = openMovie.getCrew()
    movieTitleQuery = openMovie.getMovieTitleData()
    year, month, day = movieTitleQuery.release_date.split('-')
    awardsDict = openMovie.getAwards()
    month = int(month)
    openMovie.analyzeMovie(year=int(year), month=month)
    getPoster = (openMovie.getPoster())

    return string


@app.route('/', methods=['GET', 'POST'])
def front_page():
    """
    Front page
    """
    if flask.request.method == 'POST':
        html = display_movie()
    else:
        html = ask_for_movie()
    return html


if __name__ == "__main__":
    logging.basicConfig(filename="movie_project.log",
                        level=logging.DEBUG,
                        format='%(asctime)s,%(levelname)s,%(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')

    logging.info("Web Program Starting")

    # These are the file unzipped from https://www.kaggle.com/tmdb/tmdb-movie-metadata/data
    moviesCSVFile = "../tmdb-5000-movie-dataset/tmdb_5000_movies.csv"
    creditsCSVFile = "../tmdb-5000-movie-dataset/tmdb_5000_credits.csv"

    # If the tables do not exist, create them
    if not ORM.tableExists(ORM.inspector, "Movies"):
        ORM.csvToTable(moviesCSVFile, tableName="Movies", db=ORM.db)

    if not ORM.tableExists(ORM.inspector, "Credits"):
        ORM.csvToTable(creditsCSVFile, tableName="Credits", db=ORM.db)

    use_debugger = True
    app.run(debug=True)

    # All done, log it and exit
    logging.info("Web Program Terminated")
    sys.exit(0)
