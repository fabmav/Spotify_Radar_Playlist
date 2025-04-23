#brouillon streamlit
from config import *

df = get_weekly_data_local()

st.title("Best New Track Radar Dashboard")

st.sidebar.title("coucou")
st.write("bienvenu sur mon app")
st.sidebar.subheader("analyse")
st.sidebar.subheader("dataviz")
st.sidebar.subheader("playlist in depth")

#showing a few metrics
col1,col2 = st.columns(2)
with col1 : 
    st.metric(label = "total number of Tracks", value=1500, delta=50)
    container = st.container(border=True,height=550)
    with container : 
        df_popular_track = df[['track_name','popularity']].drop_duplicates(subset="track_name").sort_values(by="popularity",ascending=False).head(10)
        st.dataframe(df_popular_track)

with col2 : 
    df_genre_pie = df[['artist_id','artist_genre_main']].groupby("artist_genre_main").count().reset_index()
    fig,ax = plt.subplots()
    ax.pie(x=df_genre_pie['artist_id'],labels=df_genre_pie['artist_genre_main'])
    st.pyplot(fig)
    st.write("doughnut by genre")

    fig_px = px.pie(df_genre_pie, values='artist_id', names='artist_genre_main', title='Split By genre', color_discrete_sequence=px.colors.sequential.RdBu)

    st.plotly_chart(fig_px)