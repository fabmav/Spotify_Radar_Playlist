from config import *

df = get_weekly_data_local()

st.write('page browsing data')

col1,col2 = st.columns(2)

with col1 : 
    with st.form(key="artist_choice") : 
        artist_name = st.text_input("choose an artist")
        st.form_submit_button()

    st.write(artist_name)

    container = st.container(border=True,height=500)
    with container : 
        st.write("artist_list")

with col2 : 
    with st.form(key="genre_choice") : 
        genre = st.text_input("choose a genre")
        st.form_submit_button()