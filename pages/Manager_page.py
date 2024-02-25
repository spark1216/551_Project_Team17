import pandas as pd
import streamlit as st
st.write("Airbnb Database for Manager")

#this can be used to return listing data
listing_data = {
    'id': [2539],
    'name': ['Clean & quiet apt home by the park'],
    'host_id': [2787],
    'host_name': ['John'],
    'neighbourhood_group': ['Brooklyn'],
    'neighbourhood': ['Kensington'],
    'latitude': [40.64749],
    'longitude': [-73.97237]
}
df = pd.DataFrame(listing_data)
st.write(df)