from dotenv import load_dotenv
import os
import base64
import json
from requests import get
from spotify_func.MesFonctions_Spotify import*
from io import*

load_dotenv()

CLIENT_ID =os.getenv("SP_PUB_KEY")

CLIENT_SECRET=os.getenv("SP_PRIV_KEY")

REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")

URI = os.getenv("PLAYLIST")

ACCESS_TOKEN = get_access_token(REFRESH_TOKEN,CLIENT_ID,CLIENT_SECRET)

#l'URI de la playlist best new track radar

liste_id = get_playlist_tracks_id(ACCESS_TOKEN,URI)

#!ai-je besoin des URI ou des ids des tracks
# with open ("test_stat_uri.txt",'w', encoding='UTF-8') as f :
#      for data in dico : 
#           f.write(data)

# g_out = open("test_stat_uri.txt",'r',encoding='UTF-8')

def main(liste) : 
    '''this fuction writes on a file named test_stat_playlist.txt musical data of spotify tracks\n
    input : list of track id\n
    action : generates a file of track musical data\n
    output : none'''

    offset = 0
    total= len(liste)-1

    with open ("test_stat_playlist.txt",'w',encoding='UTF-8') as stat : 
        column='id,danceability,energy,key,loudness,mode,valence,tempo,duration_ms,time_signature\n'
        stat.write(column)
    
    f_out = open("test_stat_playlist.txt",'a',encoding='UTF-8')
    
    while offset < total : 
    
        string = 'ids='
        for index,i in enumerate(range (0,min(99,total - offset))) : 
            string=string+","+liste_id[i]
        string=string.rstrip(',')
        # string_json=json.loads(string)
        headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}'
        }
        url=f'https://api.spotify.com/v1/audio-features?{string}'
        result=get(url=url, headers=headers)
        # print(url)
        # print(result.status_code)
        # print(result.content)
        json_result = json.loads(result.content)
        for item in json_result["audio_features"] : 
            # print(type(item))
            # print(item)
            try : 
                track_id=item['id']
                danceability= item['danceability']
                energy = item['energy']
                key = item['key']
                loudness = item['loudness']
                mode = item['mode']
                valence = item['valence']
                tempo = item['tempo']
                duration_ms = item['duration_ms']
                time_signature = item['time_signature']
                f_out.write(f"{track_id},{danceability},{energy},{key},{loudness},{mode},{valence},{tempo},{duration_ms},{time_signature}\n")
            except Exception as e : 
                print('pas trouvé')
        offset = offset+index+1
    # g_out.close()
    f_out.close()

if __name__ == "__main__" : 

    liste_id = get_playlist_tracks_id(ACCESS_TOKEN,URI)
    #TODO mettre du logging pour identifier le nombre de tracks de départ,le nombre de tracks pas trouvé, 
    #TODO le nombre de tracks stockées dans le fichier txt
    main(liste_id)
