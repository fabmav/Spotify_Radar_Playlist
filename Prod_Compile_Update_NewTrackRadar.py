#This code gets a refresh token from spotify api then retrieves tracks from selected playlist.
#It removes tracks uploaded prior to the same day of previous year.
#It then compares tracks from a selected playlists, removes old ones and uploads new ones

from MesFonctions_Spotify import*
from datetime import*
from re import*
from time import sleep
import logging

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

#logging file setup
logging.basicConfig(filename=f'log/spotify_playlist{TODAY}.log', level=logging.INFO) 

logging.info(f'date script : {TODAY}\n----------------------------------------')

#first step : getting a valid access token
ACCESS_TOKEN = get_access_token(REFRESH_TOKEN,CLIENT_ID,CLIENT_SECRET)

#second step : getting the uris
dico_uri_raw=store_uri(ACCESS_TOKEN,PLAYLISTS)

#third step: expluding traks uploaded more than one year ago.
#using track uri as dictionnary key ensures that we don't have duplicated tracks
dico_uri_new= OneYearFromNow(dico_uri_raw)

expected_length = len(dico_uri_new)

logging.info(f'playlist length : {expected_length}')
print(f'expected number of tracks : {expected_length}')


#fourth step : getting tracks currently in the playlist
dico_uri_old=get_playlist_tracks_uri(ACCESS_TOKEN,PLAYLIST_URI)

#comaprison of new trakcs vs previous tracks in order to get tracks to be removed and tracks to be uploaded
set_prev = set(dico_uri_old.keys())
set_new = set(dico_uri_new.keys())
liste_uri_toDelete = list(set_prev - set_new)
liste_uri_toUpload = list(set_new - set_prev)

logging.info(f'tracks suppressed from playlist : {[dico_uri_old[i] for i in liste_uri_toDelete]}')
logging.info(f'tracks added to playlist : {[dico_uri_new[i] for i in liste_uri_toUpload]}')

#fifth step : suprressing old tracks
if liste_uri_toDelete ==[] : 
    logging.info('no tracks to delete')
else : 
    format_track_todelete(ACCESS_TOKEN,PLAYLIST_URI,liste_uri_toDelete)


#sixth step : uploading new tracks
if liste_uri_toUpload ==[] : 
    logging.info('no tracks to add')
else : 
    format_track_topost(ACCESS_TOKEN,PLAYLIST_URI,liste_uri_toUpload)

#seventh step : updating playlist description
with open("playlist_description.txt",'r') as text_desc : 
    description =text_desc.read().replace('\n','')

aujourdhui_text = date_text()
updade_date = f' Last update : {aujourdhui_text}'
new_description = description+updade_date


update_description(ACCESS_TOKEN,PLAYLIST_URI,new_description)

#control of script result by comparing expected playlist length vs obtained length
new_length = int(get_playlist_total(ACCESS_TOKEN,PLAYLIST_URI))
logging.info(f'expected length : {expected_length}, obtained length : {new_length}')
print(f'expected length : {expected_length}, obtained length : {new_length}')

