import streamlit as st
import plotly.express as px
import pandas as pd
from functions import load_dataset


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

filter_options = df_full["Entity"].drop_duplicates()


# PAGE DISPLAY
st.header("Mise en évidence du changement climatique ")

on = st.toggle("Activer le multicolonnes")

st.subheader(
    "Corrélation entre les anomalies de température dans l'atmosphère et de précipitations et les émissions de CO²"
)

if on:
    col1, col2 = st.columns(2)

    with col1:
        filter_options2 = df_full["Entity"].drop_duplicates()
        df_filter2 = st.selectbox(
            label="Sélectionnez un filtre : ", options=filter_options2, key="filter2"
        )

        if df_filter2:
            fig = px.line(
                df_full[df_full["Entity"] == df_filter2],
                x="Year",
                y=[
                    "temperature_anomaly",
                    "precipitation_anomaly",
                    "emissions_total_including_land_use_change",
                ],
                hover_name="Entity",
            )
            fig.update_layout(legend=dict(orientation="h", y=-0.2))
            st.plotly_chart(fig, key="filter22")

    with col2:
        filter_options3 = df_full["Entity"].drop_duplicates()
        df_filter3 = st.selectbox(
            label="Sélectionnez un filtre : ", options=filter_options3, key="filter3"
        )

        if df_filter3:
            fig = px.line(
                df_full[df_full["Entity"] == df_filter3],
                x="Year",
                y=[
                    "temperature_anomaly",
                    "precipitation_anomaly",
                    "emissions_total_including_land_use_change",
                ],
                hover_name="Entity",
            )
            fig.update_layout(legend=dict(orientation="h", y=-0.2))

            st.plotly_chart(fig, key="filter33")

else:
    filter_options = df_full["Entity"].drop_duplicates()
    df_filter = st.selectbox(label="Sélectionnez un filtre : ", options=filter_options)

    if df_filter:
        fig = px.line(
            df_full[df_full["Entity"] == df_filter],
            x="Year",
            y=[
                "temperature_anomaly",
                "precipitation_anomaly",
                "emissions_total_including_land_use_change",
            ],
            hover_name="Entity",
        )
        st.plotly_chart(fig)
