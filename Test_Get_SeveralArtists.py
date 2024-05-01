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
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")

#première étape avoir un access token valide
access_token = get_access_token(REFRESH_TOKEN,client_id,client_secret)

#les paramètres de la requête
headers = {
    'Authorization': f'Bearer {access_token}'
}
#* le pays d'autorisation n'est pas nécessaire
params = {
    'country': "FR"
}


string = 'ids=2CIMQHirSU0MQqyYHq0eOx,57dN52uHvrHOxijzpIgu3E,1vCWHaC5f2uS3yhpwWbIA6'

#définition d'une erreur pour tester les uri
def Test_Erreur_Playlist(n) : 
    if n == [] : 
        raise TypeError('Mauvaise uri')


url = f"https://api.spotify.com/v1/artists?{string}"

result = requests.get(url=url, headers=headers)
data = json.loads(result.content)
print(data)