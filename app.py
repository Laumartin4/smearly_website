from os import access
import streamlit as st
import requests
import numpy as np
from PIL import Image


"""This front queries the Streamly API http://127.0.0.1:8000"""

streamly_url = 'http://127.0.0.1:8000/predict'


uploaded_file = st.file_uploader('Please upload your cells image', ["jpg", "jpeg", "png"], accept_multiple_files=False)
# bytes_data = uploaded_file.getvalue()
# st.write(bytes_data)

st.image(uploaded_file, width=200)
image = Image.open(uploaded_file)
img_array = np.array(image)



params = {'image_array':img_array.tolist()}
response = requests.post(streamly_url,json=params)


# if response.status_code == 200:
#     output = response.json()
