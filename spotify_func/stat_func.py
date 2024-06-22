# function dedicated to parsing json results of requests built to retreive data
# necessary for preparing spotify data analysis
from requests import get
from json import loads
import logging
from functools import reduce
from datetime import datetime, timezone
logger = logging.getLogger(__name__)



def list_to_string(list,sep) : 
    f = lambda x,y : str(x)+sep+str(y)
    string = (reduce(f,list))
    return string


def generate_string(string_start, liste,length, start, end) : 
    logger.info(f'length of base list to generate string : {len(liste)}')
    string_temp = ""       
    for index,i in enumerate(range (start,min(start + length,end))) : 
        string_temp=string_temp+","+liste[i]
    string_temp=string_temp.lstrip(',')
    string_temp=string_temp.rstrip(',')
    string_temp=string_start + string_temp
    logger.info(f'length of string generated : {len(string_temp.split(sep=","))}')
    return string_temp

def get_request_data(base_url,string,request_headers,request_parameters=None) : 
    request_url=f'{base_url}{string}'
    result = get(url=request_url, headers=request_headers, params=request_parameters)
    data = loads(result.content)
    return data


def get_music_data(json_data) : 
    dico={}
    for item in json_data["audio_features"] : 
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
            dico[track_id] = [track_id,danceability,energy,key,loudness,mode,
                              valence,tempo,duration_ms,time_signature]
        except Exception as e : 
            logger.info(f'''music features data not found for track id {item}''')
            print('pas trouvé')
    logger.info(f'total id parsed: {len(dico)}')
    print(f'total parsé : {len(dico)}')
    return dico

def get_tracks_popularity(json_data) : 
    dico= {}
    for item in json_data["tracks"] : 
        track_id = item["id"]
        track_name = item["name"]
        popularity = item['popularity']
        dico[track_id]= [track_id,popularity,track_name]
    return dico


def get_tracks_artist(json_data) : 
    dico= {}
    for item in json_data["tracks"] : 
        track_id = item["id"]
        for artist in item['artists'] : 
            artist_id = artist["id"]
            artist_name = artist["name"]
            dico[artist_id] = [artist_id,artist_name,track_id]
    return dico

def get_artist_data(json_data) : 
    dico = {}
    for item in json_data['artists'] : 
        artist_id=item["id"]
        total_follower = item['followers']['total']
        artist_popularity = item['popularity']
        dico[artist_id] = [artist_id,total_follower,artist_popularity]
    return dico

def get_artist_genre(json_data) : 
    dico = {}
    for item in json_data['artists'] : 
        artist_id=item["id"]
        artist_genres = item['genres']
        try :
            for genre in artist_genres : 
                dico[artist_id] = [artist_id,genre]
        except Exception as e : 
                dico[artist_id] = [artist_id,"Nan"]
    return dico

def write_to_file(liste, file_name,first_line,string_length,base_url,parse_func,request_headers,request_params=None,sep=",") : 
    '''this functions writes to a file the result of a request made to spotify API\n
    input : 
    file_name : name of the file to write to
    firt_line : header of the file
    string_length : max number of item to include in the request
    base_url : api endpoint
    parse_func : the function to use for analysing json output
    headers : header of the query
    params : parameters of the query if any (None by default)
    sep : separator to be used in the output file\n
    action : 
    writes a file\n
    output : 
    none'''

    dico_line = {}
    total = len(liste)
    offset = 0
        
    while offset < total : 
        id_string = generate_string("ids=",liste,string_length,offset,total)
        json_data = get_request_data(base_url,id_string,request_headers,request_params)
        result = parse_func(json_data)
        dico_line.update(result)
        offset += string_length

    logger.info(f'total retrieved : {len(dico_line)}, total expected : {len(liste)}')
    # if len(dico_line) != len(liste) : 
    #     set_notfound = set(liste) - set(dico_line.keys())
    #     for i in set_notfound : 
    #         print(f'index in list of item not found : {liste.index(i)}')
    #         logger.info(f'index in list of item not found : {liste.index(i)}\nid of item not found : {i}\n func : {__name__(parse_func)}')

    with open(file_name,'w',encoding = 'UTF-8') as file : 
        file.write(f'{first_line}\n')
        for key in dico_line : 
            file.write(f'{list_to_string(dico_line[key],sep)}\n')

if __name__ == "__main__" : 
    None