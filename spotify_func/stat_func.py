# function dedicated to parsing json results of requests built to retreive data
# necessary for preparing spotify data analysis
from requests import get
from json import loads
import logging
from functools import reduce
from datetime import datetime, timezone
import re
from spotify_func.musicbrainz_func import musibrainz_search_tag

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
        duration = item["duration_ms"]
        dico[track_id]= [track_id,popularity,track_name,duration]
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
    #! only outputs the first genre because of dictionnary...
    dico = {}
    dico_artists = {}

    with open ("stats/weekly_tracks_artists.txt","r",encoding="UTF-8") as f : 
        for line in f : 
            liste_line = line.split(sep=";")
            dico_artists[liste_line[0]] = liste_line[1]

    for item in json_data['artists'] : 
        artist_id=item["id"]

        if item['genres'] == [] : 
            artist_genres = musibrainz_search_tag(dico_artists[artist_id])
        
        else : 
            artist_genres =  item['genres']


        try :
            #! if there are no genre in artist_genres, the loop will not yield anything : empty iterator means no loop iteration
            for genre in artist_genres : 
                dico[artist_id] = [artist_id,genre]
        except Exception as e : 
                dico[artist_id] = [artist_id,'Nan']
    return dico



def compile_genre(L) : 

    dico = {
    'hip_hop_rnb' : re.compile("hip hop|rap|rnb|r&b|urbano|drill",re.IGNORECASE),
    'reggae_afro' : re.compile("reggae|dub|ragga|afro",re.IGNORECASE),
    'metal' : re.compile('metal|djent',re.IGNORECASE),
    'soul_jazz' : re.compile('jazz|soul',re.IGNORECASE),
    'electro_dance' : re.compile('electr|house|tech|break|bass|disco|small room|trip hop|jungle|tek',re.IGNORECASE),
    'folk_acoustic' : re.compile("acoustic|songwriter|americana|folk",re.IGNORECASE),
    'rock' : re.compile("rock|punk|hardcore|shoegaze|indie|power pop|country|screamo|emo|grunge|riot grrrl|psyche|crank wave",re.IGNORECASE),
    'pop' : re.compile('pop|chanson|variete',re.IGNORECASE)}

    # main_genre = [i if re.search(dico[i],L) != None else "other" for i in dico]
    main_genre = "unknown" if L == '[]' or L == "['Nan']" else "other"
    if main_genre == "unknown" : 
        return main_genre
    for i in dico : 
        if re.search(dico[i],L) != None : 
            main_genre = i
            break
    return main_genre


def get_artist_genre_agg(json_data) : 
    dico = {}
    dico_artists = {}

    with open ("stats/weekly_tracks_artists.txt","r",encoding="UTF-8") as f : 
        for line in f : 
            liste_line = line.split(sep=";")
            dico_artists[liste_line[0]] = liste_line[1]



    for item in json_data['artists'] : 
        artist_id=item["id"]
        #! that's where we need to use musicbrainz


        if item['genres'] == [] : 
            artist_genres = musibrainz_search_tag(dico_artists[artist_id])
            
        else : 
            artist_genres =  item['genres']



        artist_genres_main = compile_genre(str(artist_genres))
        try :
            dico[artist_id] = [artist_id,artist_genres,artist_genres_main]
        except Exception as e : 
            dico[artist_id] = [artist_id,"Nan","other"]
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

def synth_genre_list(txt,output_file) : 
    dico = {}
    with open(txt,'r',encoding='UTF-8') as input_file : 
        liste_genre = input_file
        for line in liste_genre : 
            x=re.search('(.+),(.*)',line)
            if x[1] not in dico.keys() : 
                dico[x[1]] = [x[2]]
            else : 
                dico[x[1]].append(x[2])

    with open(output_file,'w',encoding = 'UTF-8') as file : 
        for key in dico : 
            main_genre = compile_genre(str(dico[key]))
            file.write(f'{key},{dico[key]},{main_genre}\n')


if __name__ == "__main__" : 
    None