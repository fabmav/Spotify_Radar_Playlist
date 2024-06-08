#* main script for generating the data for further analysis
#* needs to import librairies
#* retrieve the env variables
#* get the track ids
#* get the 1st stats
#* with the same track ids tracks data including artist id
#* with artist id get artist data

from spotify_func.stat_func import *
from spotify_func.MesFonctions_Spotify import *

from dotenv import load_dotenv
import os
import json
from requests import get
from io import*


load_dotenv()
CLIENT_ID =os.getenv("SP_PUB_KEY")
CLIENT_SECRET=os.getenv("SP_PRIV_KEY")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
URI = os.getenv("PLAYLIST")
ACCESS_TOKEN = get_access_token(REFRESH_TOKEN,CLIENT_ID,CLIENT_SECRET)

HEADERS = {
        'Authorization': f'Bearer {ACCESS_TOKEN}'
}

PARAMS = {
    'country': "FR"
}

URL_AUDIO_FEATURES = f'https://api.spotify.com/v1/audio-features?'
URL_TRACKS = f"https://api.spotify.com/v1/tracks?"
URL_ARTISTS = f"https://api.spotify.com/v1/artists?"


liste_id = get_playlist_tracks_id(ACCESS_TOKEN,URI)

write_to_file(liste_id,"stat_audio_features.txt","coucou",99,URL_AUDIO_FEATURES,
              get_music_data,HEADERS)
