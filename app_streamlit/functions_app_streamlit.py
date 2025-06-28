#functions app_streamlit
import os
import pandas as pd

def get_directory() : 
    '''this function navigates to the stats folder'''
    os.chdir('..')

def minute_seconds(x) : 
    rounded = round(x/1000)
    minutes = rounded//60
    seconds = rounded%60
    return str(str(minutes)+"""'"""+str(seconds))

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

    #date of upload to the playlist
    df_added_at = pd.read_csv('stats/weekly_tracks_added_at.txt',sep=",")

    df_spotify = df_track_info.merge(right=df_track_artist,on="track_id")
    df_spotify = df_spotify.merge(right=df_added_at,on="track_id")
    df_spotify = df_spotify.merge(right=df_artist_data,on="artist_id")
    df_spotify = df_spotify.merge(right=df_genre,on="artist_id")

    df_spotify['duration_seconds']=round(df_spotify['duration']/1000)
    df_spotify["minute_seconds"] = df_spotify["duration"].apply(minute_seconds)

    df_spotify['added_at']=pd.to_datetime(df_spotify['added_at'])

    os.chdir(curr_dir)

    return df_spotify

if __name__ =="__main__" : 
    None