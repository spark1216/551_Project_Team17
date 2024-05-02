import pandas as pd
import streamlit as st
import datetime
import pymysql
from sqlalchemy import create_engine
from sqlalchemy import text


connection = pymysql.connect(host='localhost', user='root', password='Dsci-551')
cursor = connection.cursor()
engine = create_engine('mysql+pymysql://root:Dsci-551@localhost/airbnb0', pool_pre_ping=True)
connection=engine.connect()
# connection.commit()
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

move_in_date = st.date_input("When's your desired move in date: ", datetime.date.today())
neighbourhood_group = st.selectbox(
        'Location:',
        ('Brooklyn', 'Manhattan','Queens','Staten Island'))
room_type = st.selectbox(
        'Room Type: (required)',
        ('Private room', 'Entire home/apt','Shared room'))
price_range = st.slider('Select price range:', 0, 1500, (50, 300), key='price_range1')
# Search button
number_of_days_stay = st.number_input('Number of days stay:', min_value=1, value=1, key='number_of_days_stay1')
def room_type_hash(room_type):
    if room_type == 'Entire home/apt':
        return 0
    else:
        return 1

if st.button('Search'):
        # replace with SQL select
        # Assuming 'move_in_date' in your DataFrame is of datetime.date type. If not, you'll need to convert it.
        # Adjust the filtering logic based on how your dates are structured, e.g., exact match, after a certain date, etc.
    database='airbnb' + str(room_type_hash(room_type))
    engine = create_engine(f'mysql+pymysql://root:Dsci-551@localhost/{database}')
    connection = engine.connect()
    result = connection.execute(text(f'SELECT a.property_id, a.name, a.room_type, a.price, a.minimum_nights, a.availability_365, a.available_since_date FROM property a JOIN locatein b ON a.property_id=b.property_id JOIN location c ON b.location_id=c.location_id WHERE a.room_type="{room_type}" AND c.neighbourhood_group="{neighbourhood_group}" AND a.price>={price_range[0]} AND a.price<= {price_range[1]} AND a.minimum_nights<={number_of_days_stay} AND a.available_since_date<= "{move_in_date.strftime("%Y-%m-%d")}" AND (a.available_since_date + INTERVAL a.availability_365 DAY) >= DATE_ADD("{move_in_date.strftime("%Y-%m-%d")}", INTERVAL {number_of_days_stay} DAY) ORDER BY a.price;'))
    tables = [row for row in result.fetchall()]
    filtered_df=pd.DataFrame(tables)
    if not filtered_df.empty:
        st.write(filtered_df)
    else:
        st.write("No results found.")















# desired price range
# how many day you plan to stay
import pandas as pd
import streamlit as st
import datetime
import pymysql
from sqlalchemy import create_engine
from sqlalchemy import text


connection = pymysql.connect(host='localhost', user='root', password='Dsci-551')
cursor = connection.cursor()
engine = create_engine('mysql+pymysql://root:Dsci-551@localhost/airbnb0', pool_pre_ping=True)
connection=engine.connect()
# connection.commit()
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

move_in_date = st.date_input("When's your desired move in date: ", datetime.date.today())
neighbourhood_group = st.selectbox(
        'Location:',
        ('Brooklyn', 'Manhattan','Queens','Staten Island'))
room_type = st.selectbox(
        'Room Type: (required)',
        ('Private room', 'Entire home/apt','Shared room'))
price_range = st.slider('Select price range:', 0, 1500, (50, 300), key='price_range1')
# Search button
number_of_days_stay = st.number_input('Number of days stay:', min_value=1, value=1, key='number_of_days_stay1')
def room_type_hash(room_type):
    if room_type == 'Entire home/apt':
        return 0
    else:
        return 1

if st.button('Search'):
        # replace with SQL select
        # Assuming 'move_in_date' in your DataFrame is of datetime.date type. If not, you'll need to convert it.
        # Adjust the filtering logic based on how your dates are structured, e.g., exact match, after a certain date, etc.
    database='airbnb' + str(room_type_hash(room_type))
    engine = create_engine(f'mysql+pymysql://root:Dsci-551@localhost/{database}')
    connection = engine.connect()
    result = connection.execute(text(f'SELECT a.property_id, a.name, a.room_type, a.price, a.minimum_nights, a.availability_365, a.available_since_date FROM property a JOIN locatein b ON a.property_id=b.property_id JOIN location c ON b.location_id=c.location_id WHERE a.room_type="{room_type}" AND c.neighbourhood_group="{neighbourhood_group}" AND a.price>={price_range[0]} AND a.price<= {price_range[1]} AND a.minimum_nights<={number_of_days_stay} AND a.available_since_date<= "{move_in_date.strftime("%Y-%m-%d")}" AND (a.available_since_date + INTERVAL a.availability_365 DAY) >= DATE_ADD("{move_in_date.strftime("%Y-%m-%d")}", INTERVAL {number_of_days_stay} DAY) ORDER BY a.price;'))
    tables = [row for row in result.fetchall()]
    filtered_df=pd.DataFrame(tables)
    if not filtered_df.empty:
        st.write(filtered_df)
    else:
        st.write("No results found.")















# desired price range
# how many day you plan to stay
