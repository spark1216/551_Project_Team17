import pandas as pd
import streamlit as st
import datetime



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

if option == 'Add Data':
    st.write("File Upload")
    uploaded_file = st.file_uploader("Choose a file: ")
    #check if contain duplicated ID with existing data
    if uploaded_file is not None:
        try:
            uploaded_data = pd.read_csv(uploaded_file) # make it into SQL Query
            duplicated_ids = uploaded_data['id'].isin(df['id']) #need to replace df['id'] with SQL select ID
            if duplicated_ids.any():
                st.write("File contains duplicated ID.")
            else:
                # Assuming you want to append the new data if there are no duplicates
                df = pd.concat([df, uploaded_data], ignore_index=True)
                st.write("Data added successfully.")
        except Exception as e:
            st.write("An error occurred while reading the file.")
            st.write(e)
    st.write("File added")
    #number_of_reviews,last_review,
    #reviews_per_month,calculated_host_listings_count,availability_365

    with st.form(key='listing_form'):
        st.write("Add New Listing")
        # ID will be generated for them through : SELECT MAX(id) + 1 AS next_id FROM property;
        # Collecting various pieces of information through input fields within the form
        start_date = st.text_input('Property Available Move-in Date', '', placeholder='example: 1/1/2022')
        name = st.text_input('Name', '', placeholder='example: Clean & quiet apt home by the park')
        host_id = st.text_input('Host ID', '', placeholder='example: 18946')
        host_name = st.text_input('Host Name', '', placeholder='example: Kate')
        neighbourhood_group = st.text_input('Neighbourhood Group', '', placeholder='example: Brooklyn')
        neighbourhood = st.text_input('Neighbourhood', '', placeholder='example: Williamsburg')
        latitude = st.text_input('Latitude', '', placeholder='example: 40.7081156')
        longitude = st.text_input('Longitude', '', placeholder='example: -73.9570696')
        room_type = st.text_input('Room Type', '', placeholder='example: Private room')
        price = st.text_input('Price', '', placeholder='example: 60')
        minimum_nights = st.text_input('Minimum Nights', '', placeholder='example: 2')
        num_of_review = st.text_input('Number of Reviews', '', placeholder='example: 3')
        last_review = st.text_input('Last Review', '', placeholder='example: 10/19/2018')
        reviews_per_month = st.text_input('Reviews Per Month', '', placeholder='example: 0.23')
        calculated_host_listings_count = st.text_input('Host listing Count', '', placeholder='example: 2')
        availability_365 = st.text_input('Available nights', '', placeholder='example: 365')

        # Submit button for the form
        submit_button = st.form_submit_button(label='Submit')

    # Conditional to check if the form has been submitted
    if submit_button:
        # write a SQL insert query
        st.write("Form Submitted!")
        st.write(f"Data Added: {name}, {data}")


elif option == 'Update Data':
    with st.form(key='update_form'):
        st.write("Update Existing Data")
        # Add your input fields for updating here
        record_id = st.text_input('Record ID', '')
        find_column = st.text_input('Column Name:', '')
        new_data = st.text_input('New Data', '')
        submit_button = st.form_submit_button(label='Update')
        if submit_button:
            #write a SQL update query
            st.write(f"Data Updated for {find_column}: {record_id}, {new_data}")
            # Process updating data here

elif option == 'Delete Data':
    with st.form(key='delete_form'):
        st.write("Delete Data")
        # Add your input field for deletion here
        record_id = st.text_input('Record ID to Delete', '')
        submit_button = st.form_submit_button(label='Delete')
        if submit_button:
            #write a SQL delete query
            st.write(f"Record Deleted: {record_id}")
            # Process deletion here

elif option == 'Select an option':
    st.write("Please select an option to proceed.")







#update
#add single, file
