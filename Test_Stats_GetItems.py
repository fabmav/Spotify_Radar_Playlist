#Gestion API Spotify
from dotenv import load_dotenv
import os
import base64
import json
from requests import get
from MesFonctions_Spotify import*
from io import*

load_dotenv()

client_id =os.getenv("SP_PUB_KEY")
client_secret=os.getenv("SP_PRIV_KEY")
uri = os.getenv("PLAYLIST")
access_token = get_access_token(client_id,client_secret)


#l'uri de la playlist best new track radar

#!retourne un dico je pense que ça ne fonctionne pas
dico = get_playlist_tracks_uri(access_token,uri)
with open ("test_stat_playlist.txt",'w',encoding='UTF-8') as stat : 
     column='id,danceability,energy,key,loudness,mode,valence,tempo,duration_ms,time_signature\n'
     stat.write(column)
f_out = open("test_stat_playlist.txt",'a',encoding='UTF-8')

#!ai-je besoin des uri ou des ids des tracks
with open ("test_stat_uri.txt",'w', encoding='UTF-8') as f :
     for data in dico : 
          f.write(data)

g_out = open("test_stat_uri.txt",'r',encoding='UTF-8')

offset = 0
total= len(g_out.readlines())
print(total)
g_out.seek(0)
pos=0
while offset < total : 

    
    i=0
    string = 'ids='
    for i in range (0,min(100,total - offset)) : 
            pos+=1
            ligne = g_out.readline()
            id_uri=x=re.search('(.)*:*:*:(.+)',ligne)[2]
            string =string+id_uri.rstrip('\n')+','
    string=string.rstrip(',')
    # string_json=json.loads(string)
    headers = {
    'Authorization': f'Bearer {access_token}'
    }
    url=f'https://api.spotify.com/v1/audio-features?{string}'
    result=get(url=url, headers=headers)
    # print(url)
    # print(result.status_code)
    # print(result.content)
    json_result = json.loads(result.content)
    for item in json_result["audio_features"] : 
        print(type(item))
        print(item)
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
    offset = offset+100
g_out.close()
f_out.close()

