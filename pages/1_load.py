import streamlit as st
import csv
import os
import pandas as pd

FILESYSTEM_PATH = "/home/nagi/Desktop/mlops/src/filesystem"

st.set_page_config(
    page_title="Load Data",
    page_icon="📁"
)

st.write("# Upload csv files")

uploaded_files = st.file_uploader("Choose a file", accept_multiple_files=True)


if uploaded_files is not None:
    if st.button("Upload"):
        progress_bar = st.progress(0, text="Uploading")

        for idx, file in enumerate(uploaded_files, 1):
            
            with open(os.path.join(FILESYSTEM_PATH, file.name), "wb") as f:
                f.write(file.getbuffer())

            progress_bar.progress(1 / len(uploaded_files) * idx, text="Uploading")


files = os.listdir(FILESYSTEM_PATH)
st.write(pd.DataFrame([(file, os.path.getsize(os.path.join(FILESYSTEM_PATH, file))) for file in files], columns=['filename', 'size']))


