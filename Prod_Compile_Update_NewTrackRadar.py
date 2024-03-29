#ce code récupère le authorization code et le "refresh token" puis à partir de là récupère un refreshed token

import requests
import os
import base64
import json
from MesFonctions_Spotify import*
from dateutil.parser import isoparse
from datetime import*
from re import*
from time import sleep

aujourdhui = datetime.now(tz=timezone.utc)


#on créer un fichier de log pour suivre ce qu'il s'est passé
nom_fichier=f'log_best_new_track_radar_{aujourdhui}.txt'

with open (nom_fichier,'w',encoding='UTF-8') as log_txt : 
    log_txt.write(f'log/log_best_new_track_radar_{aujourdhui}\n')
    log_txt.write('----------------------')


#on charge les variable : les clés publiques et privées
load_dotenv()
client_id = os.getenv("SP_PUB_KEY")
client_secret = os.getenv("SP_PRIV_KEY")
#le refresh token
refresh_token = os.getenv("REFRESH_TOKEN")
#l'uri de la playlist
playlist_uri = os.getenv("PLAYLIST")

#les urls dont on va avoir besoin (ie les points d'accès des différentes requêtes)
auth_url = "https://accounts.spotify.com/authorize"
token_url = 'https://accounts.spotify.com/api/token'

#la liste des playliste qu'on va utiliser
#! sert à rien : tester si on enlève
# liste_uri=liste_uri_playlist("liste_playlist.txt")



#première étape avoir un access token valide
access_token = get_refresh_token(refresh_token,client_id,client_secret)

#seconde étape : obtenir les piste
liste_uri=store_uri(access_token)

log_txt.write(f'playlists uris : {liste_uri}')
log_txt.write('----------------------')

#troisième étape : enlever les doublons et les pistes de plus d'un an
#TODO A transformer en fonction

def OneYearFromNow(txt="compile_playlist_spotify.txt") :  
    aujourdhui = datetime.now(tz=timezone.utc)
    borne = aujourdhui.replace(year = aujourdhui.year -1)

    liste=[]
    liste2=[]

    f_in = open(txt,'r',encoding='UTF-8')
    for ligne in f_in :
        x=search('(.+) - (.+)',ligne)
        y= isoparse(x[1])
        annee = y.year
        print(f'{x[1]} - {y} - {annee} - {aujourdhui} - {borne}')
        if y>= borne : 
            liste.append(x[2])
    return liste

print(len(liste))


liste = duplicate_suppr(L)

print(len(liste))

f2_out = open("compile_playlist_spotify_nettoye.txt",'w',encoding='UTF-8')
for i in range(len(liste)) : 
    f2_out.write(f"{liste[i]}\n")
f2_out.close()

# quatrième étape : obtenir les pistes à supprimer de la playlist
get_delete_uri(access_token,playlist_uri)

sleep(60)

#cinquième étape : supprimer les pistes
format_track_todelete(access_token,playlist_uri)

sleep(60)

#sixième étape : uploader les nouvelles pistes
#le refresh token

format_track_topost(access_token,playlist_uri)

#septième étape : mettre à jour la description
with open("playlist_description.txt",'r') as text_desc : 
    description =text_desc.read().replace('\n','')

aujourdhui_text = date_text()
updade_date = f' Last update : {aujourdhui_text}'
new_description = description+updade_date

update_description(access_token,playlist_uri,new_description)


