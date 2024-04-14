#ce code récupère le authorization code et le "refresh token" puis à partir de là récupère un refreshed token
#* je choisis un artist avec son id spécifique
#* je récupère ses top tracks
import requests
import os
import base64
import json
from MesFonctions_Spotify import*
from datetime import*
from re import*
from time import sleep
from random import randint

#on charge les variable : les clés publiques et privées
load_dotenv()
client_id = os.getenv("SP_PUB_KEY")
client_secret = os.getenv("SP_PRIV_KEY")

#les urls dont on va avoir besoin (ie les points d'accès des différentes requêtes)
auth_url = "https://accounts.spotify.com/authorize"
token_url = 'https://accounts.spotify.com/api/token'


#le refresh token
f_out = open("Token_Spotify.txt",'r',encoding='UTF-8')
refresh_token = f_out.readline()

#première étape avoir un access token valide
access_token = get_refresh_token(refresh_token,client_id,client_secret)

#les paramètres de la requête
headers = {
    'Authorization': f'Bearer {access_token}'
}
params = {
    'country': "FR"
}


string = 'ids=7ouMYWpwJ422jRcDASZB7P,4VqPOruhp5EdPBeR92t6lQ,2takcwOaAZWiXQijPHIx7B'

#définition d'une erreur pour tester les uri
def Test_Erreur_Playlist(n) : 
    if n == [] : 
        raise TypeError('Mauvaise uri')


url = f"https://api.spotify.com/v1/tracks?{string}"

result = requests.get(url=url, headers=headers, params=params)
data = json.loads(result.content)
print(data)