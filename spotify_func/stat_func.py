# function dedicated to parsing json results of requests built to retreive data
# necessary for preparing spotify data analysis
from requests import get
from json import loads
import logging

logger = logging.getLogger(__name__)

def generate_string(string_start, liste,length, start, end) : 
    string_temp = string_start       
    for index,i in enumerate(range (0,min(length,end - start))) : 
        string_temp=string_temp+","+liste[i]
    string_temp=string_temp.rstrip(',')
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
            print('pas trouvé')
    return dico

def get_tracks_popularity(json_data) : 
    dico= {}
    for item in json_data["tracks"] : 
        track_id = item["id"]
        popularity = item['popularity']
        dico[track_id]= [{track_id},{popularity}]
    return dico


def get_tracks_artist(json_data) : 
    dico= {}
    for item in json_data["tracks"] : 
        track_id = item["id"]
        for artist in item['artists'] : 
            artist_id = artist["id"]
            artist_name = artist["name"]
            dico[artist_id] = [{artist["id"]},{artist["name"]},{track_id}]
    return dico

def get_artist_data(json_data) : 
    dico = {}
    for i,item in enumerate(json_data['artists']) : 
        artist_id=item["id"]
        total_follower = item['followers']['total']
        artist_popularity = item['popularity']
        dico[artist_id] = [artist_id,total_follower,artist_popularity]
    return dico

def get_artist_genre(json_data) : 
    dico = {}
    for i,item in enumerate(json_data['artists']) : 
        artist_id=item["id"]
        artist_genres = item['genres']
        dico[artist_id] = [artist_id,artist_genres]
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
    total = len(liste) -1
    offset = 0
        
    while offset < total : 
        id_string = generate_string("ids=",liste,string_length,offset,total)
        json_data = get_request_data(base_url,id_string,request_headers,request_params)
        result = parse_func(json_data)
        dico_line.update(result)
        offset += string_length
    
    with open(file_name,'w',encoding = 'UTF-8') as file : 
        file.write(f'{first_line}\n')
        for key in dico_line : 
            file.write(f'{dico_line[key]}\n')

if __name__ == "__main__" : 
    None