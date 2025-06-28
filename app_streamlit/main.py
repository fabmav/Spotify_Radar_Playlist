#brouillon streamlit
from app_streamlit.config_streamlit import *

print(f'****************** {os.getcwd()}*****************************')
df = get_weekly_data_local()

st.title("Best New Track Radar Dashboard")

st.sidebar.subheader("analyse")
st.sidebar.subheader("dataviz")
st.sidebar.subheader("playlist in depth")

#showing a few metrics
col1,col2,col3 = st.columns(3)
with col1 : 
    track_number = len(df)
    new_track_number = len(df[df["added_at"] == max(df["added_at"])])
    st.metric(label = "total number of Tracks", value=track_number, delta=new_track_number)
    
    st.header("Split by genre")
    df_genre_pie = df[['artist_id','artist_genre_main']].groupby("artist_genre_main").count().reset_index()
    fig_px = px.pie(df_genre_pie, values='artist_id', names='artist_genre_main', color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig_px)

with col2 : 
    avg_duration = f'{round(df["duration_seconds"].mean())} s'
    st.metric(label="average track duration", value=avg_duration)
    
    st.header("Duration histogram")
    boxplot_px = px.box(df,y="duration_seconds",hover_data="track_name")
    st.plotly_chart(boxplot_px)
    


with col3 : 
    avg_popularity = round(df['popularity'].mean())
    st.metric(label="average track popularity", value=avg_popularity)
    df_popular_track = df[['track_name','popularity','artist_name','artist_genre_main']].drop_duplicates(subset="track_name").sort_values(by="popularity",ascending=False).head(10)
    st.header("most popular tracks")
    st.dataframe(df_popular_track,hide_index=True)