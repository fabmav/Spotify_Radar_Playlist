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

#on charge les variable : les clés publiques et privées
load_dotenv()
client_id = os.getenv("SP_PUB_KEY")
client_secret = os.getenv("SP_PRIV_KEY")

#les urls dont on va avoir besoin (ie les points d'accès des différentes requêtes)
auth_url = "https://accounts.spotify.com/authorize"
token_url = 'https://accounts.spotify.com/api/token'

#la liste des playliste qu'on va utiliser
liste_uri=liste_uri_playlist("liste_playlist.txt")

#le refresh token
f_out = open("Token_Spotify.txt",'r',encoding='UTF-8')
refresh_token = f_out.readline()

#première étape avoir un access token valide
access_token = get_refresh_token(refresh_token,client_id,client_secret)

#seconde étape : obtenir les piste
store_uri(access_token)

#troisième étape : enlever les doublons et les pistes de plus d'un an
#TODO A transformer en fonction

aujourdhui = datetime.now(tz=timezone.utc)
borne = aujourdhui.replace(year = aujourdhui.year -1)

liste=[]
liste2=[]

f_in = open("compile_playlist_spotify.txt",'r',encoding='UTF-8')
for ligne in f_in :
    x=search('(.+) - (.+)',ligne)
    y= isoparse(x[1])
    annee = y.year
    print(f'{x[1]} - {y} - {annee} - {aujourdhui} - {borne}')
    if y>= borne : 
        liste.append(x[2])

print(len(liste))

i=0
while i < (len(liste)-1) :
    if liste.count(liste[i])>1 :
        del liste [i]
        i=0
    else : i=i+1

print(len(liste))

f2_out = open("compile_playlist_spotify_nettoye.txt",'w',encoding='UTF-8')
for i in range(len(liste)) : 
    f2_out.write(f"{liste[i]}\n")
f2_out.close()

# quatrième étape : obtenir les pistes à supprimer de la playlist
get_delete_uri(access_token)

sleep(60)

#cinquième étape : supprimer les pistes
format_track_todelete(access_token)

sleep(60)

#sixième étape : uploader les nouvelles pistes
#le refresh token

format_track_topost(access_token)

#septième étape : mettre à jour la description
playlist_uri = "5qCOMZEfehGH3T0Pu6vzrd"
description  = "All the tracks from this day one year ago until today from Pithfork Selects, NME's Best New Tracks,  Stereogum's Favorite New Music and Radio Nova Le Grand Mix playlist."
aujourdhui = date.today()
jour = aujourdhui.strftime('%d')
if jour.endswith(('11', '12', '13')):
    suffix = 'th'
else:
    suffix = {'1': 'st', '2': 'nd', '3': 'rd'}.get(jour[-1], 'th')
aujourdhui_text = aujourdhui.strftime(f'%A the %d{suffix} of %B, %Y')
updade_date = f' Last update : {aujourdhui_text}'

url = f"https://api.spotify.com/v1/playlists/{playlist_uri}"

additem_header = {
    "Authorization": 'Bearer '+access_token,
    "Content-Type": 'application/json'
}
data={
    "description": description+updade_date
}

response = requests.put(url, headers=additem_header, json=data)
response_message=response.text
print(response)
print(response.status_code)
print(response_message)



