#Gestion API Spotify
from dotenv import load_dotenv
import os
import base64
import json
from requests import post
from requests import get
from MesFonctions_Spotify import*
from io import*
from bs4 import BeautifulSoup

load_dotenv()

client_id =os.getenv("SP_PUB_KEY")
client_secret=os.getenv("SP_PRIV_KEY")

access_token = get_token(client_id,client_secret)

#l'uri de la playlist best new track radar
uri = "5qCOMZEfehGH3T0Pu6vzrd"

get_delete_uri(access_token,fichier="test_stat_uri.txt")
f_out = open("test_stat_playlist.txt",'w',encoding='UTF-8')
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
        b= item['energy']
        f_out.write(f"{b} \n")
    offset = offset+100
g_out.close
f_out.close

