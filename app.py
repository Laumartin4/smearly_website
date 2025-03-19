import streamlit as st
import requests
from PIL import Image

# This front queries the Streamly API:
# - http://127.0.0.1:8000
# - https://smearly-103125804301.europe-west1.run.app/predict


# Create two columns
col1, col2 = st.columns(2)

with col1:
    st.title('♀️ Smearly app')
    st.subheader('AI for Good: Detecting Cancer Cells, Saving Futures')
    st.write('<a href="https://www.kaggle.com/competitions/pap-smear-cell-classification-challenge/">Pap Smear Cell Classification Challenge (PS3C)</a>', unsafe_allow_html=True)

with col2:
    st.image('images/kaggle_pap_smear_logo.jpeg')


st.markdown('''
        <style>
            .stFileUploaderFile {display: none}
        <style>''',
        unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=False,
    key="file_uploader",
    help="Drag and drop image here"  # Using help to display drag instruction
)

col1, col2 = st.columns(2)

if uploaded_file is not None:

    with col1:
        #st.write("✅ File successfully loaded!")

        try:
            # Open the image using PIL
            image = Image.open(uploaded_file)

            st.markdown('''
                <style>
                    img:nth-child(1) {border: 2px solid black}
                <style>''',
                unsafe_allow_html=True)

            # Display the image
            st.image(image, width=200)

            # Convert image to bytes
            image_bytes = uploaded_file.getvalue()

        except Exception as e:
            st.error(f"An error occurred: {e}", icon='⚠️')
            raise e

    with col2:
        # Send the image as a file, not JSON
        files = {"file": image_bytes}

        try:
            with st.spinner("Wait for it...", show_time=True):
                response = requests.post('https://smearly-103125804301.europe-west1.run.app/predict', files=files)
        except Exception as e:
            st.error(f"An error occurred: {e}", icon='⚠️')
            raise e

        # Check the response status
        if response.status_code == 200:
            try:
                api_resp = response.json()
            except Exception as e:
                st.error(f"An error occurred: {e}", icon='⚠️')
                raise e

            main_class = api_resp.get('main class', '❌ ERROR')
            preds = api_resp.get('prediction', None)

            main_proba = '???'
            if preds:
                main_proba = str(round(max(preds.values())*100, 2)) + ' %'


            st_writer = {
                'unhealthy': lambda msg: st.error(msg, icon="🚨"),
                'healthy': lambda msg: st.success(msg, icon='✅'),
                'rubbish': lambda msg: st.info(msg, icon='🗑️')
            }.get(main_class, lambda msg: st.write(msg))

            pred_msg = {
                'unhealthy': f"**UNHEALTHY** cell detected (confidence: {main_proba})",
                'healthy': f"**HEALTHY** cell(s) detected (confidence: {main_proba})",
                'rubbish': f"**RUBBISH** - Non-interpretable image (confidence: {main_proba})"
            }.get(main_class, "ERROR")

            st_writer(pred_msg)
        else:
            st.error(f"Error: {response.status_code}")
            st.error(f"Response: {response.text}")
