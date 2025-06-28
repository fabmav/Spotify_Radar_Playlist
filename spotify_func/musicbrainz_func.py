# musicbrainz functions
#TODO : improve robustness by adding a check of spotify artist uri
    #le requête cherche, puis la requête lookup pour les tags et l'url spotify
    #si le match ne se fait pas sur l'uri spotify, passer au truc suivant
    #si le match fonctionne, récupérer les tags


import os
from requests import get
from dotenv import load_dotenv
import json
from time import (sleep)
import logging

logger = logging.getLogger(__name__)

load_dotenv()
USER_AGENT = os.getenv("MB_USER_AGENT")

def musicbrainz_get_tag(data) : 
    '''this fuction gets the genre tags from the FIRST artist found in a musicbrainz search. It assumes that the first artist is the best match'''
    tags = []
    
    try : 
        for i in data['artists'][0]['tags'] : 
            tag_artist = i['name'].replace(";",",")
            tags.append(tag_artist) 
    except Exception as e : 
        tags = ['Nan']
    return tags


def musibrainz_search(artist) : 
    '''this function uses the search api from musicbrainz to get musicbrainz mbid and genres (tags) based on an artist name'''
    url = "https://musicbrainz.org/ws/2/artist/"
    params = {
        "query": artist,
        "fmt": "json"
    }
    headers = {
        "User-Agent": USER_AGENT
    }
    response = get(url, params=params, headers=headers)
    try  : 
        data = response.json()
    except Exception as e : 
        logger.info(f'not working for {artist} : {response.status_code}, {response.reason}')
        data = []
    #1 second sleep to manage musicbrains rate limiting policy

    sleep(1)
    return data

def musibrainz_search_tag (artist) : 
    '''this function uses the search api from musicbrainz to get musicbrainz mbid and genres (tags) based on an artist name'''
    url = "https://musicbrainz.org/ws/2/artist/"
    params = {
        "query": artist,
        "fmt": "json"
    }
    headers = {
        "User-Agent": USER_AGENT
    }
    response = get(url, params=params, headers=headers)
    try  : 
        data = response.json()
    except Exception as e : 
        logger.info(f'not working for {artist} : {response.status_code}, {response.reason}')
        data = []
    #1 second sleep to manage musicbrains rate limiting policy

    tags_list = musicbrainz_get_tag(data)

    sleep(1)
    return tags_list

def artist_mb_search(L) : 
    '''this function takes a list of artist names as an input and returns result of musicbrains_search for each of them'''
    for artist in L : 
        artist_search = musibrainz_search(artist)
    return artist_search

def musibrainz_tag_lookup(mbid) : 
    '''this function takes a musicbrains id and performs a lookup on musicbrainz api to fetch tags'''
    lookup_url = f"https://musicbrainz.org/ws/2/artist/{mbid}"
    lookup_params = {
        "inc": "tags",
        "fmt": "json"
    }
    headers = {
        "User-Agent": USER_AGENT
    }
    lookup_response = get(lookup_url, params=lookup_params, headers=headers)
    details = lookup_response.json()
    tags = details.get('tags', [])
    return tags





if __name__ == '__main__' : 
    None