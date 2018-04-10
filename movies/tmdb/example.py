#! /usr/bin/env python3

import os
import tmdbv3api

if __name__ == "__main__":

    tmdb = tmdbv3api.TMDb()
    tmdb.api_key = os.environ['TMDB_API_KEY']

    movie = tmdbv3api.Movie()

    movieTitle = "Clerks"
    movieID =  2292
    details = movie.details(movieID)
    search = movie.search(movieTitle)
    print(search)
    for x in search:
        print(x.title)
        print(x.id)
    print(details.title)
    print(details.overview)
    print(details.popularity)
