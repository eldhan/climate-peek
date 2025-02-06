import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd


# DATA PREPARATION
# Load datasets required for graph comparisons
df_temperature_anomaly = pd.read_csv("datasets/annual-temperature-anomalies.csv")
df_precipation_anomaly = pd.read_csv("datasets/global-precipitation-anomaly.csv")
df_co2 = pd.read_csv("datasets/annual-co2-including-land-use.csv")

# Merge the datasets together to display them on the same graph
df_anomalies = pd.merge(
    df_temperature_anomaly,
    df_precipation_anomaly,
    how="inner",
    on=["Entity", "Code", "Year"],
)
df = pd.merge(df_anomalies, df_co2, how="inner", on=["Entity", "Code", "Year"])

# Prepare filters
filter_options = df["Entity"].drop_duplicates()
world_index = 175

# Dataframe for world values only
df1 = df[df["Entity"] == "World"]

# PAGE DISPLAY
st.header("Mise en évidence du changement climatique ")

on = st.toggle("Comparer deux zones")

st.subheader(
    "Corrélation entre les anomalies de température dans l'atmosphère et de précipitations et les émissions de CO² dans le monde"
)

if not on:
    df_filter = st.selectbox(
        label="Sélectionnez un filtre : ", options=filter_options, index=world_index
    )
    if df_filter:
        df0 = df[df["Entity"] == df_filter]
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            go.Scatter(
                x=df0["Year"],
                y=df0["Temperature anomaly"],
                name="anomalies de température (degrés)",
            ),
            secondary_y=False,
        )
        fig.add_trace(
            go.Scatter(
                x=df0["Year"],
                y=df0["Annual precipitation anomaly"] / 100,
                name="anomalies de précipitations (cm)",
            ),
            secondary_y=False,
        )
        fig.add_trace(
            go.Scatter(
                x=df1["Year"],
                y=df1["Annual CO₂ emissions including land-use change"],
                name="émissions de co² dans le monde (milliards de tonnes)",
                line=dict(color="red"),
            ),
            secondary_y=True,
        )
        fig.update_layout(legend=dict(orientation="h", y=-0.2))
        st.plotly_chart(fig)
else:
    col1, col2 = st.columns(2)
    with col1:
        df_filter = st.selectbox(
            label="Sélectionnez un filtre : ", options=filter_options, index=world_index
        )
        if df_filter:
            df2 = df[df["Entity"] == df_filter]
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(
                go.Scatter(
                    x=df2["Year"],
                    y=df2["Temperature anomaly"],
                    name="anomalies de température (degrés)",
                ),
                secondary_y=False,
            )
            fig.add_trace(
                go.Scatter(
                    x=df2["Year"],
                    y=df2["Annual precipitation anomaly"] / 100,
                    name="anomalies de précipitations (cm)",
                ),
                secondary_y=False,
            )
            fig.add_trace(
                go.Scatter(
                    x=df1["Year"],
                    y=df1["Annual CO₂ emissions including land-use change"],
                    name="émissions de co² dans le monde (milliards de tonnes)",
                    line=dict(color="red"),
                ),
                secondary_y=True,
            )
            fig.update_layout(legend=dict(orientation="h", y=-0.2))
            st.plotly_chart(fig, key="filter11")

    with col2:
        df_filter2 = st.selectbox(
            label="Sélectionnez un filtre : ", options=filter_options, key="filter2"
        )

        if df_filter:
            df2 = df[df["Entity"] == df_filter]
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(
                go.Scatter(
                    x=df2["Year"],
                    y=df2["Temperature anomaly"],
                    name="anomalies de température (degrés)",
                ),
                secondary_y=False,
            )
            fig.add_trace(
                go.Scatter(
                    x=df2["Year"],
                    y=df2["Annual precipitation anomaly"] / 100,
                    name="anomalies de précipitations (cm)",
                ),
                secondary_y=False,
            )
            fig.add_trace(
                go.Scatter(
                    x=df1["Year"],
                    y=df1["Annual CO₂ emissions including land-use change"],
                    name="émissions de co² dans le monde (milliards de tonnes)",
                    line=dict(color="red"),
                ),
                secondary_y=True,
            )
            fig.update_layout(legend=dict(orientation="h", y=-0.2))
            st.plotly_chart(fig, key="filter22")
