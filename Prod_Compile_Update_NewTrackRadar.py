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
TODAY = datetime.now(tz=timezone.utc).strftime('%Y-%m-%d')
HOUR = datetime.now(tz=timezone.utc).strftime('%Hh - %Mmn - %Ss UTC')

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

line_jump = lambda x,y : str(x)+"\n"+str(y)

#logging file setup
logging.basicConfig(filename=f'log/spotify_playlist{TODAY}.log', level=logging.INFO)

logging.info(f'date script : {TODAY} {HOUR}\n----------------------------------------')

#first step : getting a valid access token
ACCESS_TOKEN = get_access_token(REFRESH_TOKEN,CLIENT_ID,CLIENT_SECRET)

#second step : getting the uris
dico_uri_raw=store_uri(ACCESS_TOKEN,PLAYLISTS)
logging.info(f' raw number of tracks less duplicates : {len(dico_uri_raw)}')
print(f' raw number of tracks less duplicates : {len(dico_uri_raw)}')
#third step: expluding traks uploaded more than one year ago.
#using track uri as dictionnary key ensures that we don't have duplicated tracks
dico_uri_new= date_above(dico_uri_raw)

expected_length = len(dico_uri_new)

logging.info(f' number of tracks added less than 6 months ago : {expected_length}')
print(f' number of tracks considered for upload : {expected_length}')


#fourth step : getting tracks currently in the playlist
dico_uri_old=get_playlist_tracks_uri_new(ACCESS_TOKEN,PLAYLIST_URI)

#comaprison of new tracks vs previous tracks in order to get tracks to be removed and tracks to be uploaded
set_prev = set(dico_uri_old.keys())

set_delete = set(date_below(dico_uri_old).keys())

set_new = set(dico_uri_new.keys())

liste_uri_toDelete = list(set_delete)

liste_uri_toUpload = list(set_new - set_prev)

set_expected = (set_new -set_prev) - set_delete 

#TODO simplify logging of tracks added / suppressed
logging.info(f' tracks suppressed from playlist : ')
if dico_uri_old == {} : 
    logging.info(f'none')
else : 
    for i in liste_uri_toDelete : 
        logging.info(f' track : {dico_uri_old[i][2]}, artist : {dico_uri_old[i][3]}, uri : {dico_uri_old[i][1]}')

logging.info(f'tracks added to playlist : ')
if dico_uri_new == {} : 
    logging.info(f'none')
else : 
    for i in liste_uri_toUpload : 
        logging.info(f' track : {dico_uri_new[i][2]}, artist : {dico_uri_new[i][3]}, uri : {dico_uri_new[i][1]}')

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
logging.info(f'expected length : {len(set_expected)}, obtained length : {new_length}')
print(f'expected length : {len(set_expected)}, obtained length : {new_length}')

