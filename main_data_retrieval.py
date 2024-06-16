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
import logging


#constant variables
TODAY = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")
#logging file setup
logging.basicConfig(filename=f'log/stats_retrieval{TODAY}.log', level=logging.INFO) 

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

FIRST_LINE = ["track_id,danceability,energy,key,loudness,mode,valence,tempo,duration_ms,time_signature",
              "track_id,popularity",
              "artist_id;artist_name;track_id",
              "artist_id,total_follower,artist_popularity",
              "artist_id,artist_genres"]

liste_id = get_playlist_tracks_id(ACCESS_TOKEN,URI)

write_to_file(liste=liste_id,file_name="stats/stat_audio_features.txt",first_line=FIRST_LINE[0],
              string_length=99,base_url=URL_AUDIO_FEATURES,parse_func=get_music_data,
              request_headers=HEADERS)

write_to_file(liste=liste_id,file_name="stats/stat_tracks_popularity.txt",first_line=FIRST_LINE[1],
              string_length=49,base_url=URL_TRACKS,parse_func=get_tracks_popularity,
              request_headers=HEADERS,request_params=PARAMS)

write_to_file(liste=liste_id,file_name="stats/stat_tracks_artists.txt",first_line=FIRST_LINE[2],
              string_length=49,base_url=URL_TRACKS,parse_func=get_tracks_artist,
              request_headers=HEADERS,request_params=PARAMS,sep=";")


liste_artists = []
with open ("stats/stat_tracks_artists.txt","r",encoding="UTF-8") as f : 
    for line in f : 
        liste_line = line.split(sep=";")
        liste_artists.append(liste_line[0])
    liste_artists.remove(liste_artists[0])

write_to_file(liste=liste_artists,file_name="stats/stat_artists_data.txt",first_line=FIRST_LINE[3],
              string_length=49,base_url=URL_ARTISTS,parse_func=get_artist_data,
              request_headers=HEADERS)

write_to_file(liste=liste_artists,file_name="stats/stat_artists_genres.txt",first_line=FIRST_LINE[4],
              string_length=49,base_url=URL_ARTISTS,parse_func=get_artist_genre,
              request_headers=HEADERS)



