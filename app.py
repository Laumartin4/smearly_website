from os import access
import streamlit as st
import requests
import numpy as np
from PIL import Image
import io

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
    st.write("File successfully loaded!")
    
    try:
        # Convert the uploaded file to bytes
        bytes_data = uploaded_file.getvalue()
        
        # Open the image using PIL
        image = Image.open(io.BytesIO(bytes_data))
        
        # Display the image
        st.image(image, width=200)
        
        # Convert the image to a numpy array
        img_array = np.array(image)
        
        # Prepare the parameters for the API request
        params = {'image_array': img_array.tolist()}
        
        # Send the request to the API
        response = requests.post(streamly_url, json=params)
        
        # Check the response status code
        if response.status_code == 200:
            output = response.json()
            st.write("API Response:", output)
        else:
            st.write(f"Error: {response.status_code}")
            st.write(f"Response: {response.text}")
    
    except Exception as e:
        st.write(f"An error occurred: {e}")
else:
    st.write("Please upload a file")