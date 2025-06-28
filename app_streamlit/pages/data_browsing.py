from Spotify_Radar_Playlist.app_streamlit.config_streamlit import *

#todo boutons de choix du genre
    #todo browser les sous genre et les artistes et morceaux associés

df = get_weekly_data_local()

st.title('Data Browsing')

col1,col2,col3 = st.columns(3)

with col1 : 
    st.header("browse artists by genre")
    df_genre = df["artist_genre_main"].unique()
    genre = st.selectbox("Pick a genre",df_genre)

    df_selected = df[["artist_name","track_name","popularity"]].sort_values(by="popularity",ascending=False)[df["artist_genre_main"]==genre]
    st.dataframe(df_selected,hide_index=True)

with col2 : 
    st.header("browse by track popularity")

    values = [0,100]

    slider_range = st.slider("choose min & max popularity",value=values)

    df_by_popularity = df[["artist_name","track_name","artist_genre_main","popularity"]].sort_values(by="popularity",ascending=False)[(df['popularity']>slider_range[0]) & (df['popularity']<slider_range[1])]
    st.dataframe(df_by_popularity)

with col3 : 
    st.header("More information on Artist")
    
    with st.form(key="artist_search") : 
        artist = st.text_input("select artist name")
        st.form_submit_button()

        try : 
            artist_info = summary(f'{artist} music',sentences=3)
        except Exception as e : 
            artist_info="No information found"

    # artist_info= summary(artist,sentences=3)

    st.write(artist_info)