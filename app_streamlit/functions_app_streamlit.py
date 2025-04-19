#functions app_streamlit
import os
import pandas as pd

def get_directory() : 
    '''this function navigates to the stats folder'''
    os.chdir('..')


def get_weekly_data_local() : 

    curr_dir = os.getcwd()

    os.chdir('..')

    df_track_info = pd.read_csv('stats/weekly_tracks_popularity.txt',sep=";")

    #for mapping artist name and id to tracks
    df_track_artist = pd.read_csv('stats/weekly_tracks_artists.txt',sep=";")

    #artist number of followers and popularity
    df_artist_data = pd.read_csv('stats/weekly_artists_data.txt',sep=",")

    #aggregated genre
    df_genre = pd.read_csv('stats/weekly_artists_genres_agg.txt',sep=";")

    df_spotify = df_track_info.merge(right=df_track_artist,on="track_id")
    df_spotify = df_spotify.merge(right=df_artist_data,on="artist_id")
    df_spotify = df_spotify.merge(right=df_genre,on="artist_id")

    os.chdir(curr_dir)

    return df_spotify

    