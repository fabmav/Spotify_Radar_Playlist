from spotify_func.MesFonctions_Spotify import*
load_dotenv()
CLIENT_ID = os.getenv("SP_PUB_KEY")
CLIENT_SECRET = os.getenv("SP_PRIV_KEY")
#refresh token
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
#uri of the target playlist
PLAYLIST_URI = os.getenv("PLAYLIST")
#the scrapped playlist 
PLAYLISTS = "liste_playlist.txt"

ACCESS_TOKEN = get_access_token(REFRESH_TOKEN,CLIENT_ID,CLIENT_SECRET)



def test_func(token,uri) : 
    # liste=[]
    dico = {}
    valid_token = 'Bearer '+token
    offset = 0
    total = get_playlist_total(token,uri)
    while offset < total : 
        headers = format_token(valid_token)
        champs='items(added_at,track(uri,name,artists(name)))'
        url=f'https://api.spotify.com/v1/playlists/{uri}/tracks?fields={champs}&foffset={offset}&limit=100'
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

test_result=test_func(ACCESS_TOKEN,PLAYLIST_URI)

# print(test_result)

# dico_uri_new= date_below(test_result)


# print(dico_uri_new)

aujourdhui = datetime.now(tz=timezone.utc)
borne = aujourdhui.replace(month= aujourdhui.month -3)
new_month = liste[liste.index(aujourdhui.month) - 6]
print(borne.month)