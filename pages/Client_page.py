import pandas as pd
import streamlit as st
import datetime
# url = "../data/finalized_data.csv"
# df = pd.read_csv(url, dtype=str)

st.write("Airbnb Database for Client")


listing_data = {
    'id': [2539],
    'name': ['Clean & quiet apt home by the park'],
    'host_id': [2787],
    'host_name': ['John'],
    'neighbourhood_group': ['Brooklyn'],
    'neighbourhood': ['Kensington'],
    'latitude': [40.64749],
    'longitude': [-73.97237],
    'room_type':['Private room']
}
df = pd.DataFrame(listing_data)
# st.write(df)
move_in_date = st.date_input("When's your desired move in date: ", datetime.date.today())
neighbourhood_group = st.selectbox(
    'Location:',
    ('Brooklyn', 'Manhattan','Queens','Staten Island'))
room_type = st.selectbox(
    'Room Type:',
    ('Private room', 'Entire home/apt'))


# Search button
if st.button('Search'):
    # Assuming 'move_in_date' in your DataFrame is of datetime.date type. If not, you'll need to convert it.
    # Adjust the filtering logic based on how your dates are structured, e.g., exact match, after a certain date, etc.
    filtered_df = df[(df['neighbourhood_group'] == neighbourhood_group) & (df['room_type'] == room_type)]

    # If move_in_date needs to be considered in the filtering, you might need additional logic to handle it based on your requirements.

    if not filtered_df.empty:
        st.write(filtered_df)
    else:
        st.write("No results found.")