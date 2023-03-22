import streamlit as st
from datetime import datetime
import os
import numpy as np
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode
import  matplotlib.pyplot as plt
import plotly.figure_factory as ff
import plotly.express as px


def get_file_size(file):
    return os.path.getsize(file)

def get_ctime(file):
    ts = os.path.getctime(file)
    return datetime.fromtimestamp(ts).strftime('%Y/%m/%d %H:%M:%S')


FILESYSTEM_PATH = "./src/filesystem"

st.set_page_config(
    page_title="Analyze Data",
    page_icon="🔎"
)

files = os.listdir(FILESYSTEM_PATH)


df = pd.DataFrame([
    (file, 
    get_file_size(os.path.join(FILESYSTEM_PATH, file)),
    get_ctime(os.path.join(FILESYSTEM_PATH, file))) for file in files], columns=['filename', 'size', 'uploded time']).sort_values(by='uploded time', ascending=False)

gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_default_column(enablePivot=True, enableValue=True, enableRowGroup=True)
gb.configure_selection(selection_mode="single", use_checkbox=True)
gb.configure_side_bar()
gridoptions = gb.build()

response = AgGrid(
    df,
    height=200,
    gridOptions=gridoptions,
    enable_enterprise_modules=True,
    update_mode=GridUpdateMode.MODEL_CHANGED,
    fit_columns_on_grid_load=False,
    header_checkbox_selection_filtered_only=True,
    use_checkbox=True
)

selected = response['selected_rows']


if st.button("analyze") and selected:
    filename = selected[0]['filename']
    
    anal_df = pd.read_csv(os.path.join(FILESYSTEM_PATH, filename))
    columns = anal_df.columns

    st.session_state["filename"] = filename
    st.session_state["columns"] = columns
    st.session_state["experiment_name"] = filename.split(".")[0]

    st.write('## Sample(Top 10)')
    st.dataframe(anal_df.head(10), width=700, use_container_width=True)

    st.write('## Descriptive Statistics')
    st.dataframe(anal_df.describe(), width=700, use_container_width=True)

    st.write('## Histogram')
    for column in anal_df.columns:
        fig = px.histogram(anal_df[column])
        fig.update_traces(marker=dict(color='lightblue', line=dict(width=1, color='blue')))
        st.plotly_chart(fig)