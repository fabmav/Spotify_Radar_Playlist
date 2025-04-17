# aggreg list
from spotify_func.stat_func import synth_genre_list
INPUT = "stats/stat_artists_genres.txt"
OUTPUT = "stats/stat_artists_genres_agg.txt"

synth_genre_list(INPUT, OUTPUT)