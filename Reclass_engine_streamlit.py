import streamlit as st
import base64
import pandas as pd
import numpy as np
from datetime import *

st.title("Welcome to my expense reclassification app!")
st.subheader("Made with love by Shishir R Deshpande.")
st.write('Please ensure your dataset is rectangular and has no blank rows at the top. CSV files preferred. Output dataframe can be viewed & downloaded from the bottom of this page!')
uploaded_file = st.file_uploader("Upload file")

df = pd.read_csv(uploaded_file)

st.write("The column headers in your dataset are...")
st.write(df.columns)
st.write("You can use a maximum of 4 different fields and categories for reclassification.")

current_date_and_time = datetime.now()
current_date_and_time = current_date_and_time.strftime("%Y-%m-%d %H:%M:%S")
current_date_and_time = str(current_date_and_time).replace(":","-")
current_date_and_time_string = str(current_date_and_time)
extension = ".csv"

#Specify classification categories
st.subheader("Please type category names, field names and your keywords. Field names need to be exact and keywords need to be separated by a '|'")
Category1 = st.text_input("Name classification category 1", "Communication")
field1 = st.text_input("Input field-name in which to search for category 1 keywords", "entry description")
keywords1 = st.text_input("Type keywords to search in category 1", "keywords")
Category2 = st.text_input("Name classification category 2", "Travel")
field2 = st.text_input("Input field-name in which to search for category 2 keywords", "supplier")
keywords2 = st.text_input("Type keywords to search in category 2", "keywords")
Category3 = st.text_input("Name classification category 3", "Professional")
field3 = st.text_input("Input field-name in which to search for category 3 keywords", "entry description")
keywords3 = st.text_input("Type keywords to search in category 3", "keywords")
Category4 = st.text_input("Name classification category 4", "Power, fuel & water")
field4 = st.text_input("Input field-name in which to search for category 4 keywords", "entry description")
keywords4 = st.text_input("Type keywords to search in category 4", "keywords")

#Convert field 1 to lowercase
df[field1] = df[field1].str.lower()

#Convert field 2 name to lowercase
df[field2] = df[field2].str.lower()

#Convert field 3 to lowercase
df[field3] = df[field3].str.lower()

#Replace blanks with "0" to avoid erroneous tagging
df[field1] = df[field1].replace(np.nan, "0")

df[field2] = df[field2].replace(np.nan, "0")

df[field3] = df[field3].replace(np.nan, "0")

#Create classifier column
df['category'] = "Not Classified"

#Communication vendor test
df['category'] = np.where(df[field1].str.contains(keywords1), Category1, df['category'])

#Travel vendor test
df['category'] = np.where(df[field2].str.contains(keywords2), Category2, df['category'])

#Professional vendor test
df['category'] = np.where(df[field3].str.contains(keywords3), Category3, df['category'])

#Power fuel & water test
df['category'] = np.where(df[field4].str.contains(keywords4), Category4, df['category'])

st.write(df)

def download_link(object_to_download, download_filename, download_link_text):
    
    if isinstance(object_to_download,pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=False)

    # some strings <-> bytes conversions necessary here
    b64 = base64.b64encode(object_to_download.encode()).decode()

    return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'

if st.button('Download Dataframe as CSV'):
    tmp_download_link = download_link(df, 'Reclass_output ' + current_date_and_time_string + '.csv', 'Click here to download your data!')
    st.markdown(tmp_download_link, unsafe_allow_html=True)

