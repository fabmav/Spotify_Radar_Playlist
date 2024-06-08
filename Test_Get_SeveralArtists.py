#ce code récupère le authorization code et le "refresh token" puis à partir de là récupère un refreshed token
#* je choisis un artist avec son id spécifique
#* je récupère ses top tracks
import requests
import os
import base64
import json
from spotify_func.MesFonctions_Spotify import*
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

URL = f"https://api.spotify.com/v1/artists?"

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

dico_data_artist = {}
dico_genre_artist = {}

with open('stat_artists.txt','r',encoding='UTF-8') as f_out : 

    total = len(f_out.readlines())
    f_out.seek(0)
    # data_artists = f_out.readlines()
    f_out.seek(0)

    # print(total)
    
f_out = open('stat_artists.txt','r',encoding='UTF-8')


#! transformer le code : 
#! une fonction qui génère l'url.
#! une fonction qui exécute une requête et génère un json.
#! une fonction qui parse le json et sort sort les data.
def main(liste) : 
    offset = 0
    pos = 0
    while offset < total : 
        
        i = 0

        string = 'ids='
        for i in range (0,min(50,total - offset)) : 
                pos+=1
                if pos == 1 : 
                    ligne=f_out.readline()
                else : 
                    ligne = f_out.readline()
                    id_uri=re.search(r'(\w+);*;(.+)',ligne)[1]
                    string =string+id_uri.rstrip('\n')+","
        string=string.rstrip(",")


    # string = 'ids=2CIMQHirSU0MQqyYHq0eOx,57dN52uHvrHOxijzpIgu3E,1vCWHaC5f2uS3yhpwWbIA6'

    # #définition d'une erreur pour tester les uri
    # def Test_Erreur_Playlist(n) : 
    #     if n == [] : 
    #         raise TypeError('Mauvaise uri')

        url_=f'{URL}{string}'
        result = requests.get(url=url_, headers=headers)
        # f_out.seek(offset+1)
        
        data = json.loads(result.content)
        for i,item in enumerate(data['artists']) : 
            artist_id=item["id"]
            total_follower = item['followers']['total']
            artist_genres = item['genres']
            artist_popularity = item['popularity']
            dico_data_artist[artist_id] = [artist_id,total_follower,artist_popularity]
            dico_genre_artist[artist_id] = artist_genres
        offset+=50
    f_out.close()

    with open('data_artist.txt','w',encoding='UTF-8') as f : 
        f.write('artist_id,total_follower,artist_popularity\n')
        for i in dico_data_artist : 
            line = f'{dico_data_artist[i][0]},{dico_data_artist[i][1]},{dico_data_artist[i][2]}\n'
            f.write(line)

    #!tester avec un reduce
    with open('data_genre.txt','w',encoding='UTF-8') as f : 
        f.write('artist_id,genre\n')
        for artist in dico_genre_artist : 
                if dico_genre_artist[artist] == [] : 
                    f.write(f'{artist},Nan\n')
                else : 
                    for genre in dico_genre_artist[artist] : 
                        line = f'{artist},{genre}\n'
                        f.write(line)




#     # print(url)
#     # print(result.status_code)
#     # print(result.content)
#     json_result = json.loads(result.content)
#     # print(json_result)
#     for item in json_result["tracks"] : 
#         # print(type(item))
#         # print(item.keys())
#         track_id = item["id"]
#         popularity = item['popularity']
#         f_out.write(f'{track_id},{popularity}\n')
#         for artist in item['artists'] : 
#             h_out.write(f'{artist["id"]},{artist["name"]},{track_id}\n')

#     offset = offset+50
# #TODO pour chaque id de tracks, je veux une strings d'artistes, une string d'id d'artistes et la popularity
# #TODO la string 

# g_out.close()
# f_out.close()
# h_out.close()

if __name__ == "__main__" : 
     None