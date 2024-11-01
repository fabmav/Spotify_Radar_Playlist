#MesFonctions_Spotify

from dotenv import load_dotenv
import os
import base64
import json
from requests import post, get, delete, put
from io import*
import re
from datetime import*
from dateutil.parser import isoparse
import logging

logger = logging.getLogger(__name__)

def get_current_token() : 
    '''This function retrieves a refresh token from spotify api, it needs a private and a public keys stored 
    in a .env file'''
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

# deprecated
# def get_token(client_id,client_secret) :
#     auth_string = client_id + ":" +client_secret
#     auth_bytes = auth_string.encode("utf-8")
#     auth_base64 = str(base64.b64encode(auth_bytes),"utf-8")

#     url = "https://accounts.spotify.com/api/token"
#     headers = {
#         "Authorization": "Basic " + auth_base64,
#         "Content-Type": "application/x-www-form-urlencoded"
#     }
#     data={"grant_type": "client_credentials"}
#     result=post(url, headers = headers, data=data)
#     json_result = json.loads(result.content)
#     token=json_result["access_token"]
#     return token

def get_access_token(token, client_id, client_secret) :
    '''This funtion uses spotify private and public keys as well as refresh token to retreive an access token'''
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
    logger.info(f'attempt to retrieve token : {json_result}')
    return new_token

def format_token(token) : 
    '''This function puts in the proper format the access token : {"Authorization": token}'''
    return{"Authorization": token}

def liste_uri_playlist(nom) :
    '''this function reads from a file spotify playlist uris and puts them in a list'''
    liste=[]
    f_in = open(nom,'r',encoding='UTF-8')
    for ligne in f_in :
        logger.info(ligne)
        x=re.search('(.)*:*:*:(.+)',ligne)
        liste.append(x[2])   
    
    return liste

def get_playlist_total(token,uri) : 
    '''this function returns the total number of track of a playlist.
    One can use this to define how many times one needs to make a request to the api endpoints with a qurey size limit'''
    valid_token = 'Bearer '+token
    headers = format_token(valid_token)
    url="https://api.spotify.com/v1/playlists/"+uri+"/tracks?fields=total"
    try : 
        result=get(url=url, headers=headers)
        json_result = json.loads(result.content)
        return json_result['total']
    except Exception as e : 
        logger.info(f'bug get_playlist_total pour uri {uri}')
        logger.info(f'description : \n {e}')
        return 0

def get_playlist_snapshotid(token,uri) : 
    '''this function gets a playlist snapshot id'''
    valid_token = 'Bearer '+token
    headers = format_token(valid_token)
    url="https://api.spotify.com/v1/playlists/"+uri
    result=get(url=url, headers=headers)
    json_result = json.loads(result.content)
    return json_result['snapshot_id']

def store_uri(token,file) : 
    '''this function takes an access token and a file containing playlist uris as input\n
    identify the total number of tracks of each playlist,\n
    sends a GET request to spotify api and outputs the result of the requests\n
    in a dictionnary containing the list of each playlist tracks uri with their upload date, track name and artist name
    dictionnary key is track uri'''
    #liste=[]
    dico = {}
    valid_token = 'Bearer '+token
    liste_uri=liste_uri_playlist(file)
    count_track = 0
    for i in range(len(liste_uri)) :
        offset = 0
        total = get_playlist_total(token,liste_uri[i])
        count_track += total
        logger.info(f' total tracks playlist {i} : {total}')
        print(total)
        while offset < total : 
            headers = format_token(valid_token)
            url=f'https://api.spotify.com/v1/playlists/{liste_uri[i]}/tracks?offset={offset}&limit=100'
            print(url)
            result=get(url=url, headers=headers)
            json_result = json.loads(result.content)
            for item in json_result["items"] : 
                a= item["added_at"]
                b= item["track"]["uri"]
                c=item["track"]["name"]
                d=item["track"]["artists"][0]["name"]
                dico[b] = [a,b,c,d]
                #liste.append(f'{a} - {b} - {c} - {d}')
            print(f'{offset} - {total}')
            offset = offset+100
    #f_out.close()
    logger.info(f' raw number of tracks analysed : {count_track}')
    return dico

def duplicate_suppr(L) : 
    '''NOT USED ANYMORE : if query results are stored in a list, this function can remove duplicates'''
    i=0
    while i < (len(L)-1) :
        if L.count(L[i])>1 :
            del L [i]
            i=0
        else : i=i+1
    return L

def date_above(D) :  
    aujourdhui = datetime.now(tz=timezone.utc)

    liste = [1,2,3,4,5,6,7,8,9,10,11,12]
    new_month = liste[liste.index(aujourdhui.month) - 6]
    new_year=aujourdhui.year
    if liste.index(aujourdhui.month) - 6 <0 : 
        new_year+=-1
    borne = aujourdhui.replace(month= new_month)
    borne = borne.replace(year= new_year)

    logger.info(f' threshold date is : {borne}. all tracks above this date are kept ')
    dico={}

    for i in D :
        y= isoparse(D[i][0])
        # print(f'{i} - {y} - {annee} - {aujourdhui} - {borne}')
        if y>= borne : 
            dico[i] = D[i]
        # else : 
        #     logger.info(f'suppressed : {i}')
    logger.info(f'number of tracks kept: {len(dico)}')
    return dico

def date_below(D) :  
    aujourdhui = datetime.now(tz=timezone.utc)

    liste = [1,2,3,4,5,6,7,8,9,10,11,12]
    new_month = liste[liste.index(aujourdhui.month) - 6]
    new_year=aujourdhui.year
    if liste.index(aujourdhui.month) - 6 <0 : 
        new_year+=-1
    borne = aujourdhui.replace(month= new_month)
    borne = borne.replace(year= new_year)

    logger.info(f'threshold date is : {borne}. all tracks below this date are kept')
    dico={}

    for i in D :
        y= isoparse(D[i][0])
        # print(f'{i} - {y} - {annee} - {aujourdhui} - {borne}')
        if y< borne : 
            dico[i] = D[i]
        # else : 
        #     logger.info(f'suppressed : {i}')
    logger.info(f'number of tracks to be removed : {len(dico)}')
    return dico


def get_playlist_tracks_uri(token,uri) : 
    # liste=[]
    dico = {}
    valid_token = 'Bearer '+token
    offset = 0
    total = get_playlist_total(token,uri)
    while offset < total : 
        headers = format_token(valid_token)
        url=f'https://api.spotify.com/v1/playlists/{uri}/tracks?offset={offset}&limit=100'
        result=get(url=url, headers=headers)
        json_result = json.loads(result.content)
        for item in json_result["items"] : 
            b= item["track"]["uri"]
            c=item["track"]["name"]
            d=item["track"]["artists"][0]["name"]
            #f_out.write("{}\n".format(b))
            # liste.append(f'{b} - {c} - {d}')
            dico[b] = [b,c,d]
        offset = offset+100
    #f_out.close()
    return dico


def get_playlist_tracks_uri_new(token,uri) : 
    # liste=[]
    dico = {}
    valid_token = 'Bearer '+token
    offset = 0
    total = get_playlist_total(token,uri)
    while offset < total : 
        headers = format_token(valid_token)
        champs='items(added_at,track(uri,name,artists(name)))'
        url=f'https://api.spotify.com/v1/playlists/{uri}/tracks?fields={champs}&offset={offset}&limit=100'
        result=get(url=url, headers=headers)
        json_result = json.loads(result.content)
        for item in json_result["items"] : 
            b= item["track"]["uri"]
            c=item["track"]["name"]
            d=item["track"]["artists"][0]["name"]
            e=item["added_at"]
            #f_out.write("{}\n".format(b))
            # liste.append(f'{b} - {c} - {d}')
            dico[b] = [e,b,c,d]
        offset = offset+100
    #f_out.close()
    return dico



def get_playlist_tracks_id(token,uri) : 
    liste=[]
    # dico = {}
    valid_token = 'Bearer '+token
    offset = 0
    total = get_playlist_total(token,uri)
    while offset < total : 
        headers = format_token(valid_token)
        url=f'https://api.spotify.com/v1/playlists/{uri}/tracks?offset={offset}&limit=100'
        result=get(url=url, headers=headers)
        json_result = json.loads(result.content)
        for item in json_result["items"] : 
            track_id = item["track"]["id"]
            #f_out.write("{}\n".format(b))
            # liste.append(f'{b} - {c} - {d}')
            liste.append(track_id)
        offset = offset+100
    #f_out.close()
    return liste


def format_track_todelete(token,Uri_Playlist,liste) : 
    '''this function takes tracks uri stored in a list and puts them in the proper json format 
    to submit a delete request to spotify api'''
    buffer=0
    total= len(liste)
    while buffer<=total :
        i=0
        string = '{"tracks":['
        for i in range (0,min(100,total - buffer)) : 
                ligne = liste[buffer+i]
                string =string+'{ "uri": "'+ligne.rstrip('\n')+'" },'
        string=string.rstrip(',')+']}'
        string_json=json.loads(string)
        response = delete_tracks(token,string_json,Uri_Playlist)
        logger.info(f'batch : {int(buffer/100+1)}, delete track response status : {response.status_code, response.text}')
        buffer = buffer +100


def delete_tracks(token, uris,uri_playlist) : 
    '''this fuction sends a delete request to the spotify playlist endpoint'''
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
    return response


def post_tracks(token,uris,Uri_Playlist) : 
    '''this function sens a post request to the spotify playlist endpoint'''
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
    return response


def format_track_topost(token,uri_playlist,liste) : 
    '''this function takes tracks uri stored in a list and puts them in the proper json format 
    to submit a post request to spotify api'''
    buffer=0
    total= len(liste)
    print(f'total de piste à uploader : {total}')
    while buffer<=total :
        print(f"taille buffer à l'initialisation de la boucle : {buffer}")
        i=0
        string = '{"uris":['
        print(f'minimum entre total et buffer : {min(100,total - buffer)}')
        for i in range (0,min(100,total - buffer)) : 
                ligne = liste[buffer+i]
                string =string+'"'+ligne.rstrip(' \n')+'",'
        string=string.rstrip(',')+']}'
        string_json=json.loads(string)
        response = post_tracks(token,string_json,Uri_Playlist=uri_playlist)
        logger.info(f'batch : {int(buffer/100+1)}, upload track response status : {response.status_code, response.text}')
        buffer = buffer +100

def date_text () : 
    '''this functions gets the current date in a proper format'''
    aujourdhui = date.today()
    jour = aujourdhui.strftime('%d')
    if jour.endswith(('11', '12', '13')):
        suffix = 'th'
    else:
        suffix = {'1': 'st', '2': 'nd', '3': 'rd'}.get(jour[-1], 'th')
    aujourdhui_text = aujourdhui.strftime(f'%A the %d{suffix} of %B, %Y')
    return aujourdhui_text

def update_description(token,uri,text) : 
    '''this function posts a playlist description to the spotify playlist endpoint'''
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