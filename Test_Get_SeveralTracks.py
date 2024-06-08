#ce code récupère le authorization code et le "refresh token" puis à partir de là récupère un refreshed token
#* je choisis un artist avec son id spécifique
#* je récupère ses top tracks
import requests
import os
import json
from spotify_func.MesFonctions_Spotify import*
from datetime import*

#on charge les variable : les clés publiques et privées
load_dotenv()
CLIENT_ID = os.getenv("SP_PUB_KEY")
CLIENT_SECRET = os.getenv("SP_PRIV_KEY")

#les urls dont on va avoir besoin (ie les points d'accès des différentes requêtes)
AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = 'https://accounts.spotify.com/api/token'

#le refresh token
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")

#première étape avoir un access token valide
ACCESS_TOKEN = get_access_token(REFRESH_TOKEN,CLIENT_ID,CLIENT_SECRET)

#les paramètres de la requête
headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}'
}
params = {
    'country': "FR"
}

#définition d'une erreur pour tester les uri
# def Test_Erreur_Playlist(n) : 
#     if n == [] : 
#         raise TypeError('Mauvaise uri')


URL = f"https://api.spotify.com/v1/tracks?"

# result = requests.get(url=URL, headers=headers, params=params)
# data = json.loads(result.content)
# print(data)

# g_out = open("test_stat_uri.txt",'r',encoding='UTF-8')

#!attention aux virgules dans le nom des groupes


def main(liste) : 
    ''' this function generates two files from a list 
    of track id one with track popularity,\n
    one with artists associated with the track\n
    input : list of track id
    action : two files written
    output : none'''
    
    f_out = open("stat_tracks_popularity.txt",'w',encoding='UTF-8')
    f_out.write('id,popularity\n')

    h_out = open("stat_artists.txt",'w',encoding='UTF-8')
    h_out.write('artist_id;artist_name;track_id\n')


    offset = 0
    total= len(liste)
    # print(total)

    pos=0
    while offset < total :      
        string = 'ids='        
        for i in range (0,min(49,total - offset)) : 
            for index,i in enumerate(range (0,min(49,total - offset))) : 
                string=string+","+liste[i]
            string=string.rstrip(',')
        string=string.rstrip(",")




        url_=f'{URL}{string}'
        result = requests.get(url=url_, headers=headers, params=params)

        # print(url)
        # print(result.status_code)
        # print(result.content)
        json_result = json.loads(result.content)
        # print(json_result)
        for item in json_result["tracks"] : 
            # print(type(item))
            # print(item.keys())
            track_id = item["id"]
            popularity = item['popularity']
            f_out.write(f'{track_id},{popularity}\n')
            for artist in item['artists'] : 
                h_out.write(f'{artist["id"]};{artist["name"]};{track_id}\n')

        offset = offset+50
    #TODO pour chaque id de tracks, je veux une strings d'artistes, une string d'id d'artistes et la popularity
    #TODO la string 
    #TODO : générer une liste d'id d'artiste

    f_out.close()
    h_out.close()

if __name__ == "__main__" : 
    None