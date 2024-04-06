import pandas as pd
import streamlit as st
import datetime
# url = "../data/finalized_data.csv"
# df = pd.read_csv(url, dtype=str)

st.write("Airbnb Database for Client")

#data sample
listing_data = {
    'id': [2539],
    'name': ['Clean & quiet apt home by the park'],
    'host_id': [2787],
    'host_name': ['John'],
    'neighbourhood_group': ['Brooklyn'],
    'neighbourhood': ['Kensington'],
    'latitude': [40.64749],
    'longitude': [-73.97237],
    'room_type':['Private room'],
    'price':[200],
    'move_in_date':['1/1/2021'],
    'number_of_days_stay':[2]
}
df = pd.DataFrame(listing_data)
# st.write(df)
with st.container():
    move_in_date = st.date_input("When's your desired move in date: ", datetime.date.today())
    neighbourhood_group = st.selectbox(
        'Location:',
        ('Brooklyn', 'Manhattan','Queens','Staten Island'))
    room_type = st.selectbox(
        'Room Type:',
        ('Private room', 'Entire home/apt'))

    # Search button
    if st.button('Search', key='search1'):
        # replace with SQL select
        # Assuming 'move_in_date' in your DataFrame is of datetime.date type. If not, you'll need to convert it.
        # Adjust the filtering logic based on how your dates are structured, e.g., exact match, after a certain date, etc.
        filtered_df = df[(df['neighbourhood_group'] == neighbourhood_group) & (df['room_type'] == room_type)]
        if not filtered_df.empty:
            st.write(filtered_df)
        else:
            st.write("No results found.")


with st.container():
    move_in_date = st.date_input("When's your desired move-in date:", datetime.date.today(), key='move_in_date1')
    price_range = st.slider('Select price range:', 0, 1500, (50, 300), key='price_range1')
    number_of_days_stay = st.number_input('Number of days stay:', min_value=1, value=1, key='number_of_days_stay1')
    if st.button('Search', key='search2'):
        #replace with SQL select
        filtered_df = df[(df['price'] >= price_range[0]) & (df['price'] <= price_range[1])]
        if not filtered_df.empty:
            st.write(filtered_df)
        else:
            st.write("No results found.")
# desired price range
# how many day you plan to stay
