#functions app_streamlit
import os
import pandas as pd

APP_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.dirname(APP_DIR)
DATA_PATH_POP = os.path.join(BASE_PATH,"stats","weekly_tracks_popularity.txt")
DATA_PATH_ART = os.path.join(BASE_PATH,"stats","weekly_tracks_artists.txt")
DATA_PATH_DAT= os.path.join(BASE_PATH,"stats","weekly_artists_data.txt")
DATA_PATH_AGG = os.path.join(BASE_PATH,"stats","weekly_artists_genres_agg.txt")
DATA_PATH_ADD = os.path.join(BASE_PATH,"stats","weekly_tracks_added_at.txt")
print(APP_DIR)
print(DATA_PATH_ADD)


def get_directory() : 
    '''this function navigates to the stats folder'''
    os.chdir('..')

def minute_seconds(x) : 
    rounded = round(x/1000)
    minutes = rounded//60
    seconds = rounded%60
    return str(str(minutes)+"""'"""+str(seconds))

def get_weekly_data_local() : 

    # curr_dir = os.getcwd()

    # os.chdir('..')

    df_track_info = pd.read_csv(DATA_PATH_POP,sep=";")

    #for mapping artist name and id to tracks
    df_track_artist = pd.read_csv(DATA_PATH_ART,sep=";")

    #artist number of followers and popularity
    df_artist_data = pd.read_csv(DATA_PATH_DAT,sep=",")

    #aggregated genre
    df_genre = pd.read_csv(DATA_PATH_AGG,sep=";")

    #date of upload to the playlist
    df_added_at = pd.read_csv(DATA_PATH_ADD,sep=",")

    df_spotify = df_track_info.merge(right=df_track_artist,on="track_id")
    df_spotify = df_spotify.merge(right=df_added_at,on="track_id")
    df_spotify = df_spotify.merge(right=df_artist_data,on="artist_id")
    df_spotify = df_spotify.merge(right=df_genre,on="artist_id")

    df_spotify['duration_seconds']=round(df_spotify['duration']/1000)
    df_spotify["minute_seconds"] = df_spotify["duration"].apply(minute_seconds)

    df_spotify['added_at']=pd.to_datetime(df_spotify['added_at'])

    # os.chdir(curr_dir)

    return df_spotify

if __name__ =="__main__" : 
    None