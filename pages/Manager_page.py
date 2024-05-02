import pandas as pd
import streamlit as st
from datetime import datetime
import pymysql
from sqlalchemy import create_engine
from sqlalchemy import text
import pgeocode


# Center the image
col1, col2, col3 = st.columns([1, 1, 1])

with col2:  # image placed in the middle column
    st.image("https://miro.medium.com/v2/resize:fit:1400/format:webp/0*NChTo-XqLOxLabIW", width=200)

import streamlit as st

# Option selection
option = st.selectbox(
    'What action would you like to perform?',
    ('Select an option', 'Add Data', 'Update Data', 'Delete Data')
)
# Function to determine database based on room type

def room_type_hash(room_type):
    if room_type == 'Entire home/apt':
        return 0
    else:
        return 1
engine = create_engine(f'mysql+pymysql://root:Dsci-551@localhost')
connection = engine.connect()
result = connection.execute(text(f'SELECT MAX(property_id) AS max_id FROM (SELECT property_id FROM airbnb0.property UNION SELECT property_id FROM airbnb1.property) AS combined_ids;'))
max_id = result.fetchone()[0]
result_host = connection.execute(text(f'SELECT MAX(host_id) AS max_id FROM (SELECT host_id FROM airbnb0.host UNION SELECT host_id FROM airbnb1.host) AS combined_ids;'))
max_host_id = result_host.fetchone()[0]
if option == 'Add Data':
    st.header("File Upload")
    st.markdown(
        '[Data Entry Template for Download](https://docs.google.com/spreadsheets/d/1xfcIFy00AS1oHGmre332Bf_v7C_Gv8UohjnzTzd0Icc/edit?usp=sharing)')
    st.write(f"Start your property_id from: {max_id+1}. Please keep your property_id for your record so that you can use it to update/delete your property listing later if needed")
    st.write(f"If you have not had airbnb listing before, start your host id from: {max_host_id + 1}. Please keep your host id for your record so that you can use it to enter future airbnb listing. If you do not remember your host_id, please contact us.")
    uploaded_file = st.file_uploader("Choose a CSV file", type='csv')
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            duplicated_ids_query = f'SELECT property_id FROM (SELECT property_id FROM airbnb0.property UNION SELECT property_id FROM airbnb1.property) AS combined_ids WHERE property_id IN ({",".join(str(x) for x in df["property_id"])})'
            result = connection.execute(text(duplicated_ids_query))
            duplicated_ids = [row[0] for row in result.fetchall()]
            if len(duplicated_ids) > 0:
                st.write(f"Please check the property ID you have entered in your file. Make sure that the property ID listed starts from{max_id+1}", duplicated_ids)
                connection.close()
            else:
                databases = ['airbnb0', 'airbnb1']  # List of databases
                engines = {db: create_engine(f'mysql+pymysql://root:Dsci-551@localhost/{db}') for db in databases}
                for index, row in df.iterrows():
                    room_type = row['room_type']
                    database = 'airbnb' + str(room_type_hash(room_type))
                    engine = engines[database]
                    nomi = pgeocode.Nominatim('us')
                    query = nomi.query_postal_code(row['zipcode'])
                    row['latitude'] = query["latitude"]
                    row['longitude'] = query["longitude"]
                    data = {
                        "property_id": [row['property_id']],
                        "name": [row['name']],
                        "room_type": [row['room_type']],
                        "price": [row['price']],
                        "minimum_nights": [row['minimum_nights']],
                        "availability_365": [row['availability_365']],
                        "available_since_date": [row['available_since_date']]
                    }
                    pd.DataFrame(data).to_sql('property', con=engine, if_exists='append', index=False)
                    if row['host_id'] > max_host_id:
                        data={
                        "host_id": [row['host_id']],
                        "host_name": [row['host_name']]}
                        pd.DataFrame(data).to_sql('host', con=engine, if_exists='append', index=False)
                    data = {
                        "property_id": [row['property_id']],
                        "host_id": [row['host_id']]}
                    pd.DataFrame(data).to_sql('hostby', con=engine, if_exists='append', index=False)
                    #make location id
                    max_location_ids_query = f'SELECT MAX(location_id) FROM locatein;'
                    connection=engine.connect()
                    result = connection.execute(text(duplicated_ids_query))
                    max_location_id = result.fetchone()[0]
                    row['location_id']=max_location_id+1
                    data = {
                        "property_id": [row['property_id']],
                        "location_id": [row['location_id']]}
                    pd.DataFrame(data).to_sql('locatein', con=engine, if_exists='append', index=False)
                    data = {
                        "location_id": [row['location_id']],
                        "neighbourhood_group": [row['neighbourhood_group']],
                    "neighbourhood":[row['neighbourhood']],
                    "latitude":[row['latitude']],
                    "longitude":[row['longitude']]}
                    pd.DataFrame(data).to_sql('location', con=engine, if_exists='append', index=False)
                st.write("Data added successfully.")
        except Exception as e:
            st.write("An error occurred while reading the file.")
            st.write(e)

    with st.form(key='listing_form'):
        st.write("Add New Listing")
        # ID will be generated for them through : SELECT MAX(id) + 1 AS next_id FROM property;
        # Collecting various pieces of information through input fields within the form
        start_date = st.text_input('Property Available Move-in Date', '', placeholder='example: 2022-01-01')
        name = st.text_input('Name', '', placeholder='example: Clean & quiet apt home by the park')
        host_id = st.text_input(f'Host ID(For new hosts,start your host id from:{max_host_id + 1}', '', placeholder='example: 18946')
        host_name = st.text_input('Host Name', '', placeholder='example: Kate')
        neighbourhood_group = st.selectbox(
            'Location:',
            ('Brooklyn', 'Manhattan', 'Queens', 'Staten Island'))
        neighbourhood = st.text_input('Neighbourhood', '', placeholder='example: Williamsburg')
        zipcode=st.text_input("5-digit Zipcode", "",placeholder='example: 11206')
        room_type = st.selectbox(
            'Room Type: (required)',
            ('Private room', 'Entire home/apt', 'Shared room'))
        price = st.text_input('Price', '', placeholder='example: 60')
        minimum_nights = st.text_input('Minimum Nights', '', placeholder='example: 2')
        availability_365 = st.text_input('Available nights', '', placeholder='example: 365')
        nomi = pgeocode.Nominatim('us')
        query = nomi.query_postal_code(zipcode)
        latitude = query["latitude"]
        longitude = query["longitude"]
        property_id=max_id+1
        # Submit button for the form
        submit_button = st.form_submit_button(label='Submit')

    # Conditional to check if the form has been submitted
    if submit_button:
        try:
            datetime.strptime(start_date, '%Y-%m-%d')
        except ValueError:
            st.write(
                "Error: Data type mismatch. move-in-date only accepts date values in 'YYYY-MM-DD' format.")
        else:
            host_name_query_1 = text(f"SELECT host_name FROM airbnb1.host WHERE host_id = :host_id")
            host_name_query_0= text(f"SELECT host_name FROM airbnb0.host WHERE host_id = :host_id")
            host_name_from_query_1 = connection.execute(host_name_query_1, {'host_id': host_id}).fetchall()
            host_name_from_query_0 = connection.execute(host_name_query_0, {'host_id': host_id}).fetchall()
            if int(host_id)<=int(max_host_id):
                host_names0 = [item[0] for item in host_name_from_query_0] if host_name_from_query_0 else []
                host_names1 = [item[0] for item in host_name_from_query_1] if host_name_from_query_1 else []
                combined_host_names = host_names0 + host_names1
                print("Combined Host Names:", combined_host_names)
                if host_name_from_query_0[0][0] != host_name :
                    print(host_name_from_query_0[0][0])
                    print(host_name)
                    st.write(
                        "Your host name does not match the previous host name for this host_id.")
                else:
                    data = {
                        "property_id": property_id,
                        "available_since_date": start_date,
                        "name": name,
                        "host_id": host_id,
                        "host_name": host_name,
                        "neighbourhood_group": neighbourhood_group,
                        "neighbourhood": neighbourhood,
                        "room_type": room_type,
                        "price": price,
                        "minimum_nights": minimum_nights,
                        "availability_365": availability_365,
                        "latitude": latitude,
                        "longitude": longitude
                    }
                    print(data)
                    property_insert_query = f"""
                                       INSERT INTO {'airbnb' + str(room_type_hash(room_type))}.property (property_id, name, room_type, price, minimum_nights, availability_365, available_since_date)
                                       VALUES ({data["property_id"]},'{data["name"].replace("'", "''")}', '{data["room_type"]}', {data["price"]}, {data["minimum_nights"]}, {data["availability_365"]}, '{data["available_since_date"]}');
                                   """

                    host_insert_query = f"""
                                      INSERT INTO {'airbnb' + str(room_type_hash(room_type))}.host (host_id, host_name)
                                      VALUES ({data["host_id"]}, '{data["host_name"]}');
                                      """
                    hostby_insert_query = f"""
                                       INSERT INTO {'airbnb' + str(room_type_hash(room_type))}.hostby (property_id, host_id)
                                       VALUES ({data["property_id"]}, {data["host_id"]});
                                       """
                    location_insert_query = f"""
                                       INSERT INTO {'airbnb' + str(room_type_hash(room_type))}.location (neighbourhood_group, neighbourhood, latitude, longitude)
                                       VALUES ('{data["neighbourhood_group"]}', '{data["neighbourhood"]}', {data["latitude"]}, {data["longitude"]});
                                       """
                    locatein_insert_query = f"""
                                       INSERT INTO {'airbnb' + str(room_type_hash(room_type))}.locatein (property_id, location_id)
                                       VALUES ({data["property_id"]},(SELECT MAX(location_id) FROM {'airbnb' + str(room_type_hash(room_type))}.location));
                                       """
                    try:
                        connection.execute(text(property_insert_query))
                        connection.execute(text(host_insert_query))
                        connection.execute(text(hostby_insert_query))
                        connection.execute(text(location_insert_query))
                        connection.execute(text(locatein_insert_query))
                        # connection.commit()
                        st.write("Form Submitted!")
                        st.write(f"Data Added: {name}, {data}")
                    except Exception as e:
                        st.error(f"An error occurred: {e}")
                        st.write("Please check once again on the data you inputted")
            else:
                data = {
                    "property_id":property_id,
                    "available_since_date": start_date,
                    "name": name,
                    "host_id": host_id,
                    "host_name": host_name,
                    "neighbourhood_group": neighbourhood_group,
                    "neighbourhood": neighbourhood,
                    "room_type": room_type,
                    "price": price,
                    "minimum_nights": minimum_nights,
                    "availability_365": availability_365,
                    "latitude": latitude,
                    "longitude": longitude
                }
                print(data)
                property_insert_query = f"""
                    INSERT INTO {'airbnb' + str(room_type_hash(room_type))}.property (property_id, name, room_type, price, minimum_nights, availability_365, available_since_date)
                    VALUES ({data["property_id"]},'{data["name"].replace("'", "''")}', '{data["room_type"]}', {data["price"]}, {data["minimum_nights"]}, {data["availability_365"]}, '{data["available_since_date"]}');
                """

                host_insert_query = f"""
                   INSERT INTO {'airbnb' + str(room_type_hash(room_type))}.host (host_id, host_name)
                   VALUES ({data["host_id"]}, '{data["host_name"]}');
                   """
                hostby_insert_query = f"""
                    INSERT INTO {'airbnb' + str(room_type_hash(room_type))}.hostby (property_id, host_id)
                    VALUES ({data["property_id"]}, {data["host_id"]});
                    """
                location_insert_query = f"""
                    INSERT INTO {'airbnb' + str(room_type_hash(room_type))}.location (neighbourhood_group, neighbourhood, latitude, longitude)
                    VALUES ('{data["neighbourhood_group"]}', '{data["neighbourhood"]}', {data["latitude"]}, {data["longitude"]});
                    """
                locatein_insert_query = f"""
                    INSERT INTO {'airbnb' + str(room_type_hash(room_type))}.locatein (property_id, location_id)
                    VALUES ({data["property_id"]},(SELECT MAX(location_id) FROM {'airbnb' + str(room_type_hash(room_type))}.location));
                    """
                try:
                    connection.execute(text(property_insert_query))
                    connection.execute(text(host_insert_query))
                    connection.execute(text(hostby_insert_query))
                    connection.execute(text(location_insert_query))
                    connection.execute(text(locatein_insert_query))
                    # connection.commit()
                    st.write("Form Submitted!")
                    st.write(f"Data Added: {name}, {data}")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
                    st.write("Please check once again on the data you inputted")

elif option == 'Update Data':
    with (st.form(key='update_form')):
        st.write("Update existing data regarding property information. Please contact us regarding updating other existing data.")
        # Add your input fields for updating here
        property_id = st.text_input('Property ID (Required)', '')
        find_column =st.selectbox('Column that Needs Modification',('name', 'price','minimum_nights','availability_365', "available_since_date"))
        st.write('Note that the price should just be an integer value (e.g. 123, instead of $123)')
        new_data = st.text_input('New Data', '')
        submit_button = st.form_submit_button(label='Update')
        if submit_button:
            error_occurred=False
            if find_column=="available_since_date":
                try:
                    datetime.strptime(new_data, '%Y-%m-%d')
                except ValueError:
                    st.write("Error: Data type mismatch. available_since_date column only accepts date values in 'YYYY-MM-DD' format.")
                    error_occurred=True
            elif find_column in ("availability_365",'minimum_nights','price'):
                if not new_data.isdigit():
                    st.write("Error: Data type mismatch. This column only accepts integer values.(e.g. 125)")
                    error_occurred = True
            if not property_id.isdigit():
                st.write("Error: Property ID should be an integer value")
                error_occurred = True
            property_found=False
            if not error_occurred:
                for i in ['airbnb0','airbnb1']:
                    get_database_query = f""" SELECT EXISTS 
                                            (SELECT 1 FROM {i}.property WHERE property_id = {property_id}); """
                    exists=connection.execute(text(get_database_query)).fetchone()[0]
                    if exists==True:
                        if find_column in ('name','available_since_date'):
                            update_query = f"""
                                            UPDATE {i}.property
                                            SET {find_column} = '{new_data}'
                                            WHERE property_id = {property_id};
                                            """
                        else:
                            update_query = f""" UPDATE {i}.property
                                                SET {find_column} = {new_data}
                                                WHERE property_id = {property_id};
                                                                    """
                        try:
                            connection.execute(text(update_query))
                            # connection.commit()
                            st.write(f"Updated property ID {property_id}'s {find_column} data to be {new_data}")
                            property_found=True
                        except:
                            st.write("An error occurred while updating data.")
                            property_found=True
                        break
                if not property_found:
                    st.write("Property ID not found in the database. Please check your property ID again ")


elif option == 'Delete Data':
    #delete from property table
    with st.form(key='delete_form'):
        st.write("Delete Data")
        # Add your input field for deletion here
        property_id = st.text_input('Property ID to Delete', '')
        submit_button = st.form_submit_button(label='Delete')
        if submit_button:
            error_occurred = False
            if not property_id.isdigit():
                st.write("Error: Property ID should be an integer value")
                error_occurred = True
            property_found = False
            if not error_occurred:
                for i in ['airbnb0', 'airbnb1']:
                    get_database_query = f""" SELECT EXISTS 
                                                        (SELECT 1 FROM {i}.property WHERE property_id = {property_id}); """
                    exists = connection.execute(text(get_database_query)).fetchone()[0]
                    if exists == True:
                        delete_query = f""" DELETE FROM {i}.property
                                            WHERE property_id={property_id};"""
                        try:
                            connection.execute(text(delete_query))
                            # connection.commit()
                            st.write(f"Property information deleted for property_id: {property_id}")
                            property_found = True
                        except Exception as e:
                            st.write("An error occurred while updating data.")
                            st.write(e)
                            property_found = True
                        break
                if not property_found:
                    st.write("Property ID not found in the database. Please check your property ID again ")


elif option == 'Select an option':
    st.write("Please select an option to proceed.")







#update
#add single, file
import pandas as pd
import streamlit as st
from datetime import datetime
import pymysql
from sqlalchemy import create_engine
from sqlalchemy import text
import pgeocode


# Center the image
col1, col2, col3 = st.columns([1, 1, 1])

with col2:  # image placed in the middle column
    st.image("https://miro.medium.com/v2/resize:fit:1400/format:webp/0*NChTo-XqLOxLabIW", width=200)

import streamlit as st

# Option selection
option = st.selectbox(
    'What action would you like to perform?',
    ('Select an option', 'Add Data', 'Update Data', 'Delete Data')
)
# Function to determine database based on room type

def room_type_hash(room_type):
    if room_type == 'Entire home/apt':
        return 0
    else:
        return 1
engine = create_engine(f'mysql+pymysql://root:Dsci-551@localhost')
connection = engine.connect()
result = connection.execute(text(f'SELECT MAX(property_id) AS max_id FROM (SELECT property_id FROM airbnb0.property UNION SELECT property_id FROM airbnb1.property) AS combined_ids;'))
max_id = result.fetchone()[0]
result_host = connection.execute(text(f'SELECT MAX(host_id) AS max_id FROM (SELECT host_id FROM airbnb0.host UNION SELECT host_id FROM airbnb1.host) AS combined_ids;'))
max_host_id = result_host.fetchone()[0]
if option == 'Add Data':
    st.header("File Upload")
    st.markdown(
        '[Data Entry Template for Download](https://docs.google.com/spreadsheets/d/1xfcIFy00AS1oHGmre332Bf_v7C_Gv8UohjnzTzd0Icc/edit?usp=sharing)')
    st.write(f"Start your property_id from: {max_id+1}. Please keep your property_id for your record so that you can use it to update/delete your property listing later if needed")
    st.write(f"If you have not had airbnb listing before, start your host id from: {max_host_id + 1}. Please keep your host id for your record so that you can use it to enter future airbnb listing. If you do not remember your host_id, please contact us.")
    uploaded_file = st.file_uploader("Choose a CSV file", type='csv')
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            duplicated_ids_query = f'SELECT property_id FROM (SELECT property_id FROM airbnb0.property UNION SELECT property_id FROM airbnb1.property) AS combined_ids WHERE property_id IN ({",".join(str(x) for x in df["property_id"])})'
            result = connection.execute(text(duplicated_ids_query))
            duplicated_ids = [row[0] for row in result.fetchall()]
            if len(duplicated_ids) > 0:
                st.write(f"Please check the property ID you have entered in your file. Make sure that the property ID listed starts from{max_id+1}", duplicated_ids)
                connection.close()
            else:
                databases = ['airbnb0', 'airbnb1']  # List of databases
                engines = {db: create_engine(f'mysql+pymysql://root:Dsci-551@localhost/{db}') for db in databases}
                for index, row in df.iterrows():
                    room_type = row['room_type']
                    database = 'airbnb' + str(room_type_hash(room_type))
                    engine = engines[database]
                    nomi = pgeocode.Nominatim('us')
                    query = nomi.query_postal_code(row['zipcode'])
                    row['latitude'] = query["latitude"]
                    row['longitude'] = query["longitude"]
                    data = {
                        "property_id": [row['property_id']],
                        "name": [row['name']],
                        "room_type": [row['room_type']],
                        "price": [row['price']],
                        "minimum_nights": [row['minimum_nights']],
                        "availability_365": [row['availability_365']],
                        "available_since_date": [row['available_since_date']]
                    }
                    pd.DataFrame(data).to_sql('property', con=engine, if_exists='append', index=False)
                    if row['host_id'] > max_host_id:
                        data={
                        "host_id": [row['host_id']],
                        "host_name": [row['host_name']]}
                        pd.DataFrame(data).to_sql('host', con=engine, if_exists='append', index=False)
                    data = {
                        "property_id": [row['property_id']],
                        "host_id": [row['host_id']]}
                    pd.DataFrame(data).to_sql('hostby', con=engine, if_exists='append', index=False)
                    #make location id
                    max_location_ids_query = f'SELECT MAX(location_id) FROM locatein;'
                    connection=engine.connect()
                    result = connection.execute(text(duplicated_ids_query))
                    max_location_id = result.fetchone()[0]
                    row['location_id']=max_location_id+1
                    data = {
                        "property_id": [row['property_id']],
                        "location_id": [row['location_id']]}
                    pd.DataFrame(data).to_sql('locatein', con=engine, if_exists='append', index=False)
                    data = {
                        "location_id": [row['location_id']],
                        "neighbourhood_group": [row['neighbourhood_group']],
                    "neighbourhood":[row['neighbourhood']],
                    "latitude":[row['latitude']],
                    "longitude":[row['longitude']]}
                    pd.DataFrame(data).to_sql('location', con=engine, if_exists='append', index=False)
                st.write("Data added successfully.")
        except Exception as e:
            st.write("An error occurred while reading the file.")
            st.write(e)

    with st.form(key='listing_form'):
        st.write("Add New Listing")
        # ID will be generated for them through : SELECT MAX(id) + 1 AS next_id FROM property;
        # Collecting various pieces of information through input fields within the form
        start_date = st.text_input('Property Available Move-in Date', '', placeholder='example: 2022-01-01')
        name = st.text_input('Name', '', placeholder='example: Clean & quiet apt home by the park')
        host_id = st.text_input(f'Host ID(For new hosts,start your host id from:{max_host_id + 1}', '', placeholder='example: 18946')
        host_name = st.text_input('Host Name', '', placeholder='example: Kate')
        neighbourhood_group = st.selectbox(
            'Location:',
            ('Brooklyn', 'Manhattan', 'Queens', 'Staten Island'))
        neighbourhood = st.text_input('Neighbourhood', '', placeholder='example: Williamsburg')
        zipcode=st.text_input("5-digit Zipcode", "",placeholder='example: 11206')
        room_type = st.selectbox(
            'Room Type: (required)',
            ('Private room', 'Entire home/apt', 'Shared room'))
        price = st.text_input('Price', '', placeholder='example: 60')
        minimum_nights = st.text_input('Minimum Nights', '', placeholder='example: 2')
        availability_365 = st.text_input('Available nights', '', placeholder='example: 365')
        nomi = pgeocode.Nominatim('us')
        query = nomi.query_postal_code(zipcode)
        latitude = query["latitude"]
        longitude = query["longitude"]
        property_id=max_id+1
        # Submit button for the form
        submit_button = st.form_submit_button(label='Submit')

    # Conditional to check if the form has been submitted
    if submit_button:
        try:
            datetime.strptime(start_date, '%Y-%m-%d')
        except ValueError:
            st.write(
                "Error: Data type mismatch. move-in-date only accepts date values in 'YYYY-MM-DD' format.")
        else:
            host_name_query_1 = text(f"SELECT host_name FROM airbnb1.host WHERE host_id = :host_id")
            host_name_query_0= text(f"SELECT host_name FROM airbnb0.host WHERE host_id = :host_id")
            host_name_from_query_1 = connection.execute(host_name_query_1, {'host_id': host_id}).fetchall()
            host_name_from_query_0 = connection.execute(host_name_query_0, {'host_id': host_id}).fetchall()
            if int(host_id)<=int(max_host_id):
                host_names0 = [item[0] for item in host_name_from_query_0] if host_name_from_query_0 else []
                host_names1 = [item[0] for item in host_name_from_query_1] if host_name_from_query_1 else []
                combined_host_names = host_names0 + host_names1
                print("Combined Host Names:", combined_host_names)
                if host_name_from_query_0[0][0] != host_name :
                    print(host_name_from_query_0[0][0])
                    print(host_name)
                    st.write(
                        "Your host name does not match the previous host name for this host_id.")
                else:
                    data = {
                        "property_id": property_id,
                        "available_since_date": start_date,
                        "name": name,
                        "host_id": host_id,
                        "host_name": host_name,
                        "neighbourhood_group": neighbourhood_group,
                        "neighbourhood": neighbourhood,
                        "room_type": room_type,
                        "price": price,
                        "minimum_nights": minimum_nights,
                        "availability_365": availability_365,
                        "latitude": latitude,
                        "longitude": longitude
                    }
                    print(data)
                    property_insert_query = f"""
                                       INSERT INTO {'airbnb' + str(room_type_hash(room_type))}.property (property_id, name, room_type, price, minimum_nights, availability_365, available_since_date)
                                       VALUES ({data["property_id"]},'{data["name"].replace("'", "''")}', '{data["room_type"]}', {data["price"]}, {data["minimum_nights"]}, {data["availability_365"]}, '{data["available_since_date"]}');
                                   """

                    host_insert_query = f"""
                                      INSERT INTO {'airbnb' + str(room_type_hash(room_type))}.host (host_id, host_name)
                                      VALUES ({data["host_id"]}, '{data["host_name"]}');
                                      """
                    hostby_insert_query = f"""
                                       INSERT INTO {'airbnb' + str(room_type_hash(room_type))}.hostby (property_id, host_id)
                                       VALUES ({data["property_id"]}, {data["host_id"]});
                                       """
                    location_insert_query = f"""
                                       INSERT INTO {'airbnb' + str(room_type_hash(room_type))}.location (neighbourhood_group, neighbourhood, latitude, longitude)
                                       VALUES ('{data["neighbourhood_group"]}', '{data["neighbourhood"]}', {data["latitude"]}, {data["longitude"]});
                                       """
                    locatein_insert_query = f"""
                                       INSERT INTO {'airbnb' + str(room_type_hash(room_type))}.locatein (property_id, location_id)
                                       VALUES ({data["property_id"]},(SELECT MAX(location_id) FROM {'airbnb' + str(room_type_hash(room_type))}.location));
                                       """
                    try:
                        connection.execute(text(property_insert_query))
                        connection.execute(text(host_insert_query))
                        connection.execute(text(hostby_insert_query))
                        connection.execute(text(location_insert_query))
                        connection.execute(text(locatein_insert_query))
                        # connection.commit()
                        st.write("Form Submitted!")
                        st.write(f"Data Added: {name}, {data}")
                    except Exception as e:
                        st.error(f"An error occurred: {e}")
                        st.write("Please check once again on the data you inputted")
            else:
                data = {
                    "property_id":property_id,
                    "available_since_date": start_date,
                    "name": name,
                    "host_id": host_id,
                    "host_name": host_name,
                    "neighbourhood_group": neighbourhood_group,
                    "neighbourhood": neighbourhood,
                    "room_type": room_type,
                    "price": price,
                    "minimum_nights": minimum_nights,
                    "availability_365": availability_365,
                    "latitude": latitude,
                    "longitude": longitude
                }
                print(data)
                property_insert_query = f"""
                    INSERT INTO {'airbnb' + str(room_type_hash(room_type))}.property (property_id, name, room_type, price, minimum_nights, availability_365, available_since_date)
                    VALUES ({data["property_id"]},'{data["name"].replace("'", "''")}', '{data["room_type"]}', {data["price"]}, {data["minimum_nights"]}, {data["availability_365"]}, '{data["available_since_date"]}');
                """

                host_insert_query = f"""
                   INSERT INTO {'airbnb' + str(room_type_hash(room_type))}.host (host_id, host_name)
                   VALUES ({data["host_id"]}, '{data["host_name"]}');
                   """
                hostby_insert_query = f"""
                    INSERT INTO {'airbnb' + str(room_type_hash(room_type))}.hostby (property_id, host_id)
                    VALUES ({data["property_id"]}, {data["host_id"]});
                    """
                location_insert_query = f"""
                    INSERT INTO {'airbnb' + str(room_type_hash(room_type))}.location (neighbourhood_group, neighbourhood, latitude, longitude)
                    VALUES ('{data["neighbourhood_group"]}', '{data["neighbourhood"]}', {data["latitude"]}, {data["longitude"]});
                    """
                locatein_insert_query = f"""
                    INSERT INTO {'airbnb' + str(room_type_hash(room_type))}.locatein (property_id, location_id)
                    VALUES ({data["property_id"]},(SELECT MAX(location_id) FROM {'airbnb' + str(room_type_hash(room_type))}.location));
                    """
                try:
                    connection.execute(text(property_insert_query))
                    connection.execute(text(host_insert_query))
                    connection.execute(text(hostby_insert_query))
                    connection.execute(text(location_insert_query))
                    connection.execute(text(locatein_insert_query))
                    # connection.commit()
                    st.write("Form Submitted!")
                    st.write(f"Data Added: {name}, {data}")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
                    st.write("Please check once again on the data you inputted")

elif option == 'Update Data':
    with (st.form(key='update_form')):
        st.write("Update existing data regarding property information. Please contact us regarding updating other existing data.")
        # Add your input fields for updating here
        property_id = st.text_input('Property ID (Required)', '')
        find_column =st.selectbox('Column that Needs Modification',('name', 'price','minimum_nights','availability_365', "available_since_date"))
        st.write('Note that the price should just be an integer value (e.g. 123, instead of $123)')
        new_data = st.text_input('New Data', '')
        submit_button = st.form_submit_button(label='Update')
        if submit_button:
            error_occurred=False
            if find_column=="available_since_date":
                try:
                    datetime.strptime(new_data, '%Y-%m-%d')
                except ValueError:
                    st.write("Error: Data type mismatch. available_since_date column only accepts date values in 'YYYY-MM-DD' format.")
                    error_occurred=True
            elif find_column in ("availability_365",'minimum_nights','price'):
                if not new_data.isdigit():
                    st.write("Error: Data type mismatch. This column only accepts integer values.(e.g. 125)")
                    error_occurred = True
            if not property_id.isdigit():
                st.write("Error: Property ID should be an integer value")
                error_occurred = True
            property_found=False
            if not error_occurred:
                for i in ['airbnb0','airbnb1']:
                    get_database_query = f""" SELECT EXISTS 
                                            (SELECT 1 FROM {i}.property WHERE property_id = {property_id}); """
                    exists=connection.execute(text(get_database_query)).fetchone()[0]
                    if exists==True:
                        if find_column in ('name','available_since_date'):
                            update_query = f"""
                                            UPDATE {i}.property
                                            SET {find_column} = '{new_data}'
                                            WHERE property_id = {property_id};
                                            """
                        else:
                            update_query = f""" UPDATE {i}.property
                                                SET {find_column} = {new_data}
                                                WHERE property_id = {property_id};
                                                                    """
                        try:
                            connection.execute(text(update_query))
                            # connection.commit()
                            st.write(f"Updated property ID {property_id}'s {find_column} data to be {new_data}")
                            property_found=True
                        except:
                            st.write("An error occurred while updating data.")
                            property_found=True
                        break
                if not property_found:
                    st.write("Property ID not found in the database. Please check your property ID again ")


elif option == 'Delete Data':
    #delete from property table
    with st.form(key='delete_form'):
        st.write("Delete Data")
        # Add your input field for deletion here
        property_id = st.text_input('Property ID to Delete', '')
        submit_button = st.form_submit_button(label='Delete')
        if submit_button:
            error_occurred = False
            if not property_id.isdigit():
                st.write("Error: Property ID should be an integer value")
                error_occurred = True
            property_found = False
            if not error_occurred:
                for i in ['airbnb0', 'airbnb1']:
                    get_database_query = f""" SELECT EXISTS 
                                                        (SELECT 1 FROM {i}.property WHERE property_id = {property_id}); """
                    exists = connection.execute(text(get_database_query)).fetchone()[0]
                    if exists == True:
                        delete_query = f""" DELETE FROM {i}.property
                                            WHERE property_id={property_id};"""
                        try:
                            connection.execute(text(delete_query))
                            # connection.commit()
                            st.write(f"Property information deleted for property_id: {property_id}")
                            property_found = True
                        except Exception as e:
                            st.write("An error occurred while updating data.")
                            st.write(e)
                            property_found = True
                        break
                if not property_found:
                    st.write("Property ID not found in the database. Please check your property ID again ")


elif option == 'Select an option':
    st.write("Please select an option to proceed.")







#update
#add single, file

