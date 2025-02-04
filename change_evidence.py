import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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
df = pd.merge(df_anomalies, df_co2, how="inner", on=["Entity", "Code", "Year"])

filter_options = df["Entity"].drop_duplicates()

# PAGE DISPLAY
st.header("Mise en évidence du changement climatique ")

on = st.toggle("Comparer deux zones")

st.subheader(
    "Corrélation entre les anomalies de température dans l'atmosphère et de précipitations et les émissions de CO² dans le monde"
)
df1 = df[df["Entity"] == "World"]

if on:
    col1, col2 = st.columns(2)

    with col1:
        filter_options2 = df["Entity"].drop_duplicates()
        df_filter2 = st.selectbox(
            label="Sélectionnez un filtre : ", options=filter_options2, key="filter2"
        )

        if df_filter2:
            df2 = df[df["Entity"] == df_filter2]
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(
                go.Scatter(
                    x=df2["Year"],
                    y=df2["temperature_anomaly"],
                    name="anomalies de température (degrés)",
                ),
                secondary_y=False,
            )
            fig.add_trace(
                go.Scatter(
                    x=df2["Year"],
                    y=df2["precipitation_anomaly"] / 100,
                    name="anomalies de précipitations (cm)",
                ),
                secondary_y=False,
            )
            fig.add_trace(
                go.Scatter(
                    x=df1["Year"],
                    y=df1["emissions_total_including_land_use_change"],
                    name="émissions de co² dans le monde (milliards de tonnes)",
                    line=dict(color="red"),
                ),
                secondary_y=True,
            )
            fig.update_layout(legend=dict(orientation="h", y=-0.2))
            st.plotly_chart(fig, key="filter22")

    with col2:
        filter_options3 = df["Entity"].drop_duplicates()
        df_filter3 = st.selectbox(
            label="Sélectionnez un filtre : ", options=filter_options3, key="filter3"
        )

        if df_filter3:
            df3 = df[df["Entity"] == df_filter3]
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(
                go.Scatter(
                    x=df3["Year"],
                    y=df3["temperature_anomaly"],
                    name="anomalies de température (degrés)",
                ),
                secondary_y=False,
            )
            fig.add_trace(
                go.Scatter(
                    x=df3["Year"],
                    y=df3["precipitation_anomaly"] / 100,
                    name="anomalies de précipitations (cm)",
                ),
                secondary_y=False,
            )
            fig.add_trace(
                go.Scatter(
                    x=df1["Year"],
                    y=df1["emissions_total_including_land_use_change"],
                    name="émissions de co² dans le monde (milliards de tonnes)",
                    line=dict(color="red"),
                ),
                secondary_y=True,
            )
            fig.update_layout(legend=dict(orientation="h", y=-0.2))
            st.plotly_chart(fig, key="filter33")

else:
    filter_options = df["Entity"].drop_duplicates()
    df_filter = st.selectbox(label="Sélectionnez un filtre : ", options=filter_options)

    if df_filter:
        df0 = df[df["Entity"] == df_filter]
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            go.Scatter(
                x=df0["Year"],
                y=df0["temperature_anomaly"],
                name="anomalies de température (degrés)",
            ),
            secondary_y=False,
        )
        fig.add_trace(
            go.Scatter(
                x=df0["Year"],
                y=df0["precipitation_anomaly"] / 100,
                name="anomalies de précipitations (cm)",
            ),
            secondary_y=False,
        )
        fig.add_trace(
            go.Scatter(
                x=df1["Year"],
                y=df1["emissions_total_including_land_use_change"],
                name="émissions de co² dans le monde (milliards de tonnes)",
                line=dict(color="red"),
            ),
            secondary_y=True,
        )
        fig.update_layout(legend=dict(orientation="h", y=-0.2))
        st.plotly_chart(fig)
