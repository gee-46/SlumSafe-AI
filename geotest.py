import streamlit as st
from streamlit_geolocation import streamlit_geolocation

st.title("Geo Test")
loc = streamlit_geolocation()
st.write(loc)
