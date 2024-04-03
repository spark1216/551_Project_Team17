import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Airbnb Listing"
)
# Define your custom styles via markdown for the title
st.markdown("""
    <style>
    /*  color  */
    h1 {
        color: #FD676C;
    }

    /* center the text */
    .main h1 {
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# Center the image
col1, col2, col3 = st.columns([1, 1, 1])

with col2:  # image placed in the middle column
    st.image("https://miro.medium.com/v2/resize:fit:1400/format:webp/0*NChTo-XqLOxLabIW", width=200)

# The title will now be centered and in Airbnb's brand color
st.title("Welcome to Airbnb Listing Database")


