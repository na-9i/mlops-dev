import streamlit as st
import pandas as pd
import numpy as np
import mlflow
from mlflow.exceptions import MlflowException
from mlflow import MlflowClient
import os

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import train_test_split


FILESYSTEM_PATH = "./src/filesystem"

MODELS = {
    "Classification": {
        "Random Forest":RandomForestClassifier,
        "Decision Tree": DecisionTreeClassifier,
        "Logistic Regression": LogisticRegression
    },
    "Regression": {
        "Random Forest":RandomForestRegressor,
        "Linear Regression": LinearRegression
    }
}

client = MlflowClient()


st.write(f'## {st.session_state["experiment_name"]}')


try:
    experiment_name = st.session_state["experiment_name"]

    experiment_id = client.create_experiment(experiment_name)

    client.set_experiment_tag(experiment_id, "version", "0.1")

except KeyError:
    print('Error')

except MlflowException:
    pass

mlflow.set_experiment(experiment_name)

inference_type = st.selectbox("Type", options=["Classification", "Regression"])
target_column = st.selectbox("Target Column", options=st.session_state["columns"])

st.session_state["target_column"] = target_column

if inference_type == "Classification":
    selected_model = st.selectbox("Model", options=["Random Forest", "Decision Tree", "Logistic Regression"])
elif inference_type == "Regression":
    selected_model = st.selectbox("Model", options=["Random Forest", "Linear Regression"])

test_size = st.select_slider("Test Size", [i/100 for i in range(0, 101, 1)], value=(0.2))


if st.button("Train"):
    mlflow.sklearn.autolog()

    model = MODELS[inference_type][selected_model]()

    df = pd.read_csv(os.path.join(FILESYSTEM_PATH, st.session_state["filename"])).dropna()

    X = df.drop(columns=target_column).select_dtypes('number')

    y = df[target_column]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)
        

    with mlflow.start_run():
        
        model.fit(X_train, y_train)

        model.score(X_test, y_test)