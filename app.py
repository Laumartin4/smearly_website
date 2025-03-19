import streamlit as st
import requests
import numpy as np
from PIL import Image
import io

"""This front queries the Streamly API http://127.0.0.1:8000"""

# Inject custom CSS to change the background color and text color

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&display=swap');

    .stApp {
        background-color: #A9A9A9;
        color: #D3D3D3;
        font-family: 'Roboto Mono', monospace;
    }
    h1, h2 {
        color: #D3D3D3;
        font-family: 'Roboto Mono', monospace;
    }
    .upload-square {
        border: 2px dashed #D3D3D3; /* Dashed border for drag and drop feel */
        padding: 20px;
        width: 300px;
        height: 300px;
        display: flex;
        justify-content: center;
        align-items: center;
        margin: auto;
    }
    .drag-text {
        text-align: center;
        margin-top: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Create two columns
col1, col2 = st.columns(2)

with col1:
    st.title('Smearly app')
    st.subheader('AI for Good: Detecting Cancer Cells, Saving Futures')

with col2:
    uploaded_file = st.file_uploader(
        "",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=False,
        key="file_uploader",
        help="Drag and drop image here"  # Using help to display drag instruction
    )

    if uploaded_file is not None:
        st.write("✅ File successfully loaded!")

        try:
            # Open the image using PIL
            image = Image.open(uploaded_file)

            # Display the image
            st.image(image, width=200)

            # Convert image to bytes
            image_bytes = uploaded_file.getvalue()

            # Send the image as a file, not JSON
            files = {"file": image_bytes}
            response = requests.post('https://smearly-103125804301.europe-west1.run.app/predict', files=files)

            # Check the response status
            if response.status_code == 200:
                output = response.json()
                st.write("**AI Prediction:**", output)
            else:
                st.write(f"Error: {response.status_code}")
                st.write(f"Response: {response.text}")

        except Exception as e:
            st.write(f"⚠️ An error occurred: {e}")
