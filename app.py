from os import access
import streamlit as st
import requests
import numpy as np
from PIL import Image


"""This front queries the Streamly API http://127.0.0.1:8000"""

### TITLE ###
st.title('Smearly app')
st.subheader('AI for Good: Detecting Cancer Cells, Saving Futures')


### THEME ###
primaryColor="#AE5675"
backgroundColor="#DCDCDC"
secondaryBackgroundColor="#AE3036"
textColor="#D69C66"
font="sans serif"


### URL ###
streamly_url = 'http://127.0.0.1:8000/predict'


### FILE UPLOAD ###
uploaded_file = st.file_uploader('Please upload your cells image', ["jpg", "jpeg", "png"], accept_multiple_files=False)

if uploaded_file is not None:
    st.write("File successfully loaded !")
else:
    st.write("Please upload a file")



st.image(uploaded_file, width=200)
image = Image.open(uploaded_file)
img_array = np.array(image)


params = {'image_array':img_array.tolist()}
response = requests.post(streamly_url,json=params)


# if response.status_code == 200:
#     output = response.json()
