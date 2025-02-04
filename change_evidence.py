import streamlit as st
import plotly.express as px
import pandas as pd
from functions import load_dataset, normalize_data


# DATA PREPARATION
# Load datasets required for graph comparisons
df_temperature_anomaly, metadata_temperature_anomaly = load_dataset(
    "annual-temperature-anomalies"
)
df_precipation_anomaly, metadata_precipation_anomaly = load_dataset(
    "global-precipitation-anomaly"
)
df_co2, metadata_co2 = load_dataset("annual-co2-including-land-use")

# Merge the datasets together to display them on the same graph
df_anomalies = pd.merge(
    df_temperature_anomaly,
    df_precipation_anomaly,
    how="inner",
    on=["Entity", "Code", "Year"],
)
df_full = pd.merge(df_anomalies, df_co2, how="inner", on=["Entity", "Code", "Year"])

data_values = [
    "temperature_anomaly",
    "precipitation_anomaly",
    "emissions_total_including_land_use_change",
]

# Normalize the data
df = normalize_data(df_full, data_values)

filter_options = df["Entity"].drop_duplicates()

# PAGE DISPLAY
st.header("Mise en évidence du changement climatique ")
df_filter = st.selectbox(label="Sélectionnez un filtre : ", options=filter_options)
st.subheader(
    "Corrélation entre les anomalies de température dans l'atmosphère et de précipitations et les émissions de CO²"
)
if df_filter:
    fig = px.line(
        df[df["Entity"] == df_filter],
        x="Year",
        y=data_values,
    )
    st.plotly_chart(fig)
