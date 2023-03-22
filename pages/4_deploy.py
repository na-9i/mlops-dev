import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode
import mlflow
from mlflow.exceptions import MlflowException
from mlflow import MlflowClient
import os
import pandas as pd


FILESYSTEM_PATH = "./src/filesystem"

client = MlflowClient()

st.write(f'## {st.session_state["experiment_name"]}')

experiment_name = st.session_state["experiment_name"]
experiment_id = mlflow.get_experiment_by_name(experiment_name).experiment_id

df = pd.DataFrame(mlflow.search_runs([experiment_id]))

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

if selected:
    run_id = selected[0]["run_id"]

    model = mlflow.sklearn.load_model(f"./mlruns/{experiment_id}/{run_id}/artifacts/model")

    df = pd.read_csv(os.path.join(FILESYSTEM_PATH, st.session_state["filename"]))\
        .dropna()\
        .drop(columns=st.session_state["target_column"])\
        .select_dtypes("number")

    inputs = {}

    for column in df.columns:
        inputs.update({column: st.text_input(column)})

    if st.button("Predict"):
        inputs.update({key: list(map(float, value.split(','))) for key, value in inputs.items()})

        preds = model.predict(pd.DataFrame(inputs))
        st.write(pd.DataFrame(preds, columns=["prediction"]))


