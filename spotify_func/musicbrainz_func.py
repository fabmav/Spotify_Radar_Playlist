# musicbrainz functions
#TODO need to add logging
#TODO need to manage edge case and errors (no match, request error, no tags)
#TODO need to add the function wich will take the list with missing genres and will update it with an added genre : 
    #TODO for item in list : 
        #TODO if genre is unknown : 
            #TODO add to list_unkown_genre[]
    #TODO for item in missing_genre[]
        #TODO musibrainz_search(item)
        #TODO item[genre] is metalcore, death metal
        #TODO item[main_gerne] is metal
        #TODO update list of arstist / genre


import os
from requests import get,post
from dotenv import load_dotenv
import json
from time import (sleep)

load_dotenv()
USER_AGENT = os.getenv("MB_USER_AGENT")

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
    data = response.json()
    #1 second sleep to manage musicbrains rate limiting policy
    sleep(1)
    return data

def artist_mb_search(L) : 
    '''this function takes a list of artist names as an input and returns result of musicbrains_search for each of them'''
    for artist in L : 
        artist_search = musibrainz_search(artist)
    return artist_search