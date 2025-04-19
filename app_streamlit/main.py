#brouillon streamlit
import streamlit as st

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
    container = st.container(border=True,height=500)
    with container : 
        st.write("new_artist_list")
with col2 : 
    st.write("doughnut by genre")