#This code gets a refresh token from spotify api then retrieves tracks from selected playlist.
#It removes tracks uploaded prior to the same day of previous year.
#It then compares tracks from a selected playlists, removes old ones and uploads new ones

from spotify_func.MesFonctions_Spotify import*
from datetime import*
from re import*
from time import sleep
import logging
from functools import reduce

#constant variables
TODAY = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")

#public and private keys
load_dotenv()
CLIENT_ID = os.getenv("SP_PUB_KEY")
CLIENT_SECRET = os.getenv("SP_PRIV_KEY")
#refresh token
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
#uri of the target playlist
PLAYLIST_URI = os.getenv("PLAYLIST")
#the scrapped playlist 
PLAYLISTS = "liste_playlist.txt"

#first step : getting a valid access token
ACCESS_TOKEN = get_access_token(REFRESH_TOKEN,CLIENT_ID,CLIENT_SECRET)

#fourth step : getting tracks currently in the playlist
dico_uri_old=get_playlist_tracks_uri_new(ACCESS_TOKEN,PLAYLIST_URI)

#comaprison of new tracks vs previous tracks in order to get tracks to be removed and tracks to be uploaded
set_delete = set(dico_uri_old.keys())



liste_uri_toDelete = list(set_delete)
format_track_todelete(ACCESS_TOKEN,PLAYLIST_URI,liste_uri_toDelete)


