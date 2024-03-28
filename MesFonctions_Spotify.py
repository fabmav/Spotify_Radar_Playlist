#MesFonctions_Spotify

from dotenv import load_dotenv
import os
import base64
import json
from requests import post, get, delete, put
from io import*
import re
from bs4 import BeautifulSoup
from time import sleep
from datetime import*

def get_current_token() : 
    load_dotenv()
    client_id = os.getenv("SP_PUB_KEY")
    client_secret = os.getenv("SP_PRIV_KEY")
    #le endpoint où je vais poster ma requête pour récupérer mon token
    token_url = 'https://accounts.spotify.com/api/token'
    #j'encode ma clé publique et ma clé privée en base 64
    auth_string = client_id + ":" +client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes),"utf-8")
    #les paramètres de la requête
    token_params = {
        'grant_type': 'client_credentials'
    }
    #l'en-tête de la requête
    token_headers = {
        "Authorization": "Basic " + auth_base64
    }
    #la requête avec l'adresse, les data et l'en-tête
    token_response = post(token_url, data=token_params, headers=token_headers)
    print(token_response)
    token_result = json.loads(token_response.content)
    # Extract the access token from the response JSON
    access_token = token_result['access_token']
    access_expires = token_result['expires_in']
    access_refresh = ['refresh_token']
    print(f'token : {access_token}, expiration : {access_expires}, refresh : {access_refresh}')

def get_token(client_id,client_secret) :
    auth_string = client_id + ":" +client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes),"utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data={"grant_type": "client_credentials"}
    result=post(url, headers = headers, data=data)
    json_result = json.loads(result.content)
    token=json_result["access_token"]
    return token

def get_refresh_token(token, client_id, client_secret) :
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes),"utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data={
        "grant_type": "refresh_token",
        "refresh_token": token}
    
    result=post(url, headers= headers, data=data)
    json_result = json.loads(result.content)
    print(json_result)
    new_token=json_result["access_token"]
    return new_token

def get_auth_token(token) : 
    return{"Authorization": token}

def liste_uri_playlist(nom) :
    '''this function reads from a file spotify playlist uris and puts them in a list'''
    liste=[]
    f_in = open(nom,'r',encoding='UTF-8')
    for ligne in f_in :
        x=re.search('(.)*:*:*:(.+)',ligne)
        liste.append(x[2])   
    return liste

def get_playlist_total(token,uri) : 
    valid_token = 'Bearer '+token
    headers = get_auth_token(valid_token)
    url="https://api.spotify.com/v1/playlists/"+uri+"/tracks?fields=total"
    result=get(url=url, headers=headers)
    json_result = json.loads(result.content)
    return json_result['total']

def get_playlist_snapshotid(token,uri) : 
    valid_token = 'Bearer '+token
    headers = get_auth_token(valid_token)
    url="https://api.spotify.com/v1/playlists/"+uri
    result=get(url=url, headers=headers)
    json_result = json.loads(result.content)
    return json_result['snapshot_id']

def store_uri(token) : 
    '''this function takes a token and a file containing playlist uris as input\n
    identify the total number of tracks of each playlist,\n
    sends a GET request to spotify api and outputs the result of the requests\n
    in a file containing the compiled list of each playlist tracks uri with their upload date '''
    #! pourquoi un fichier, et pas une data structure ou un dataframe
    
    valid_token = 'Bearer '+token
    liste_uri=liste_uri_playlist("liste_playlist.txt")
    f_out = open("compile_playlist_spotify.txt",'w',encoding='UTF-8')
    for i in range(len(liste_uri)) :
        offset = 0
        total = get_playlist_total(token,liste_uri[i])
        print(total)
        while offset < total : 
            headers = get_auth_token(valid_token)
            url=f'https://api.spotify.com/v1/playlists/{liste_uri[i]}/tracks?offset={offset}&limit=100'
            print(url)
            result=get(url=url, headers=headers)
            json_result = json.loads(result.content)
            for item in json_result["items"] : 
                a= item["added_at"]
                b= item["track"]["uri"]
                f_out.write("{} - {} \n".format(a,b))
            print(f'{offset} - {total}')
            offset = offset+100
    f_out.close()


def get_delete_uri(token,uri,fichier="delete_playlist_spotify.txt") : 
    valid_token = 'Bearer '+token
    f_out = open(fichier,'w',encoding='UTF-8')
    offset = 0
    total = get_playlist_total(token,uri)
    while offset < total : 
        headers = get_auth_token(valid_token)
        url=f'https://api.spotify.com/v1/playlists/{uri}/tracks?offset={offset}&limit=100'
        result=get(url=url, headers=headers)
        json_result = json.loads(result.content)
        for item in json_result["items"] : 
            b= item["track"]["uri"]
            f_out.write("{}\n".format(b))
        offset = offset+100
    f_out.close()

def format_track_todelete(token,Uri_Playlist,fichier = "delete_playlist_spotify.txt") : 
    buffer=0
    f_out = open(fichier,'r',encoding='UTF-8')
    total= len(f_out.readlines())
    f_out.seek(0)
    while buffer<=total :
        i=0
        string = '{"tracks":['
        for i in range (0,min(100,total - buffer)) : 
                ligne = f_out.readline()
                string =string+'{ "uri": "'+ligne.rstrip('\n')+'" },'
        string=string.rstrip(',')+']}'
        string_json=json.loads(string)
        delete_tracks(token,string_json,Uri_Playlist)
        buffer = buffer +100
        
def delete_tracks(token, uris,uri_playlist="5qCOMZEfehGH3T0Pu6vzrd") : 
    playlist_uri = uri_playlist
    url = f"https://api.spotify.com/v1/playlists/{playlist_uri}/tracks"
    deleteitem_header = {
    "Authorization": 'Bearer '+token,
    "Content-Type": 'application/json'
        }
    data=uris
    response = delete(url, headers=deleteitem_header, json=data)
    response_message=response.text
    print(response.status_code, response_message)


def post_tracks(token,uris,Uri_Playlist="5qCOMZEfehGH3T0Pu6vzrd") : 
    sleep(15)
    playlist_uri = Uri_Playlist
    url = f"https://api.spotify.com/v1/playlists/{playlist_uri}/tracks"
    deleteitem_header = {
    "Authorization": 'Bearer '+token,
    "Content-Type": 'application/json'
        }
    data=uris
    response = post(url, headers=deleteitem_header, json=data)
    response_message=response.text
    print(f'statut post track : {response.status_code}, {response_message}\n si 200 : pb si 201 : ok')

def format_track_topost(token,uri_playlist,nom = "compile_playlist_spotify_nettoye.txt") : 
    buffer=0
    spot_out = open(nom,'r',encoding='UTF-8')
    spot_out.seek(0)
    total= len(spot_out.readlines())
    print(f'total de piste à uploader : {total}')
    spot_out.seek(0)
    while buffer<=total :
        print(f"taille buffer à l'initialisation de la boucle : {buffer}")
        i=0
        string = '{"uris":['
        print(f'minimum entre total et buffer : {min(100,total - buffer)}')
        for i in range (0,min(100,total - buffer)) : 
                ligne = spot_out.readline()
                string =string+'"'+ligne.rstrip(' \n')+'",'
        string=string.rstrip(',')+']}'
        string_json=json.loads(string)
        post_tracks(token,string_json,Uri_Playlist=uri_playlist)
        buffer = buffer +100

def get_artist(token,artiste) : 
    url = "https://api.spotify.com/v1/search"
    headers = {
        'Authorization': f'Bearer {token}'
    }
    params = {
        'q': artiste,
        'type': 'artist',
        'limit': 10
    }

    response = get(url=url, headers=headers, params=params)
    data = response.json()
    return data

def date_text () : 
    aujourdhui = date.today()
    jour = aujourdhui.strftime('%d')
    if jour.endswith(('11', '12', '13')):
        suffix = 'th'
    else:
        suffix = {'1': 'st', '2': 'nd', '3': 'rd'}.get(jour[-1], 'th')
    aujourdhui_text = aujourdhui.strftime(f'%A the %d{suffix} of %B, %Y')
    return aujourdhui_text

def update_description(token,uri,text) : 
    url = f"https://api.spotify.com/v1/playlists/{uri}"
    additem_header = {
        "Authorization": 'Bearer '+token,
        "Content-Type": 'application/json'
    }
    data={
        "description": text
    }

    response = put(url=url, headers=additem_header, json=data)
    response_message=response.text
    print(response)
    print(response.status_code)
    print(response_message)

if __name__ == '__main__' : 
    None