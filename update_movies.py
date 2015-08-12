"""Build XML info files for roksbox from omdbapi data."""

import sys
import argparse
import json
import xml.etree.ElementTree as ET

try:
    import requests
except ImportError:
    sys.stderr.write("You do not have the 'requests' module installed. " +
                     "Please see http://docs.python-requests.org/en/latest/ " +
                     "for more information.")
    exit(1)

_base_url = 'http://www.omdbapi.com/'


def api_get(data):
    """Get JSON data from omdbapi."""
    requisite_headers = {'Accept': 'application/json',
                         'Content-Type': 'application/json'}

    response = requests.get(_base_url, headers=requisite_headers, params=data)

    return response.status_code, response.text


def get_movie(movie):
    """Get movie info from the database."""
    movie_data = {'t': movie}
    status, results = api_get(movie_data)

    if status == 200:
        return results


def json_to_xml(movie_json):
    """Convert movie from json to xml.

    Sample JSON:
    {
      "Title": "The Lego Movie",
      "Year": "2014",
      "Rated": "PG",
      "Released": "7 Feb 2014",
      "Runtime": "100 min",
      "Genre": "Animation, Adventure, Comedy",
      "Director": "Phil Lord, Christopher Miller",
      "Writer": "Phil Lord (screenplay), Christopher Miller (screenplay),
                 Dan Hageman (story), Kevin Hageman (story), Phil Lord (story),
                 Christopher Miller (story)",
      "Actors": "Will Arnett, Elizabeth Banks, Craig Berry, Alison Brie",
      "Plot": "An ordinary Lego construction worker, thought to be the
               prophesied 'Special', is recruited to join a quest to stop an
               evil tyrant from gluing the Lego universe into eternal stasis.",
      "Language": "English",
      "Country": "Australia, USA, Denmark",
      "Awards": "Nominated for 1 Oscar. Another 65 wins & 56 nominations.",
      "Poster": "http://ia.media-imdb.com/images/M/V1_SX300.jpg",
      "Metascore": "83",
      "imdbRating": "7.8",
      "imdbVotes": "216176",
      "imdbID": "tt1490017",
      "Type": "movie",
      "Response": "True"
    }

    Sample XML:

    <video>
        <title></title>
        <year></year>
        <genre></genre>
        <mpaa></mpaa>
        <director></director>
        <actors></actors>
        <description></description>
        <length></length>
    </video>

    """
    parsed_json = json.loads(movie_json)

    parsed_xml = ET.Element("video")

    year = ET.SubElement(parsed_xml, 'title')
    year.text = parsed_json['Title']
    title = ET.SubElement(parsed_xml, 'year')
    title.text = parsed_json['Year']
#    genre = ET.SubElement(parsed_xml, 'genre')
#    genre.text = parsed_json['Genre']
    mpaa = ET.SubElement(parsed_xml, 'mpaa')
    mpaa.text = parsed_json['Rated']
    director = ET.SubElement(parsed_xml, 'director')
    director.text = parsed_json['Director']
    actors = ET.SubElement(parsed_xml, 'actors')
    actors.text = parsed_json['Actors']
    desc = ET.SubElement(parsed_xml, 'description')
    desc.text = parsed_json['Plot']
    runtime = ET.SubElement(parsed_xml, 'length')
    runtime.text = parsed_json['Runtime'].split()[0]

    return ET.tostring(parsed_xml)


# call main
if __name__ == '__main__':

    parser = argparse.ArgumentParser(argument_default='')
    parser.add_argument('-m', '--movie', action='store', nargs="*")

    movie_search = ''
    args = parser.parse_args()
    if args.movie != '':
        movie_search = " ".join(args.movie)
        movie_info = get_movie(movie_search)
        xml_ret = json_to_xml(movie_info)
        print xml_ret
    else:
        print "No movie found."
