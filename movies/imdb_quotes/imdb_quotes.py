#! /usr/bin/env python3

import os
import re
import bs4
import omdb
import requests

if __name__ == "__main__":

    title = "Gladiator"
    title = "Clerks"
    title = "Avatar"
    title = "The Matrix"
    title = "The Expendables"
    client = omdb.OMDBClient(apikey=os.environ['OMDB_API_KEY'])
    movie = client.get(title=title, tomatoes=False)
    print(movie['imdb_id'])
    imdb_url = "https://www.imdb.com/title/{}/awards?ref_=tt_awd".format(
        movie['imdb_id'])

    r = requests.get(imdb_url)
    # print(r.text)
    soup = bs4.BeautifulSoup(r.text, "lxml")

    table = soup.find('table', attrs={'class': 'awards'})
    data = []
    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])  # Get rid of empty values

    # print(len(data))
    # print(data)

    index = 0
    awards_dict = {}
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
                awards_dict[awards[0]] = y
            else:
                awards = x[0].split('\n')
                y = awards[1:]
                while '' in y:
                    y.remove('')
                awards_dict[awards[0]] = y

        index = index + 1
    # print(awards_dict)
    for k, v in awards_dict.items():
        print("Award: {:40} Winner: {:40}".format(k, ", ".join(v)))
