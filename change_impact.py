import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd


# DATA PREPARATION
# Load dataset
df1 = pd.read_csv("datasets/annual-co2-including-land-use.csv")
df2 = pd.read_csv("datasets/number-of-natural-disaster-events.csv")
# Sort dataset by year to correctly animate the graph
df1 = df1.sort_values(by="Year", ascending=True)
# Remove aggregated categories from the dataframe
df1 = df1[df1["Code"].notna()]
df1 = df1[df1["Entity"] == "World"]

df2 = df2[
    (df2["Entity"] == "Flood")
    | (df2["Entity"] == "Drought")
    | (df2["Entity"] == "Wildfire")
    | (df2["Entity"] == "Extreme temperature")
    | (df2["Entity"] == "Extreme weather")
]
# PAGE DISPLAY
st.header("Les impacts du changement climatique")

st.subheader("Les évènements climatiques extrêmes vs les émissions de CO²")

df_filter = st.selectbox(
    label="Sélectionnez un évènement climatique : ",
    options=df2["Entity"].drop_duplicates(),
)

# Create figure with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
fig.add_trace(
    go.Scatter(
        x=df1["Year"],
        y=df1["Annual CO₂ emissions including land-use change"],
        name="émissions de co²",
        line=dict(color="blue"),
    ),
    secondary_y=False,
)

if df_filter:
    fig.add_trace(
        go.Scatter(
            x=df2[df2["Entity"] == df_filter]["Year"],
            y=df2[df2["Entity"] == df_filter]["Disasters"],
            name="nombre d'évènements extrêmes",
            line=dict(color="red"),
        ),
        secondary_y=True,
    )

# Add figure title
fig.update_layout(
    title_text="""Évolution du nombre d'évènements climatiques extrêmes
    et des émissions de CO²"""
)

# Set x-axis title
fig.update_xaxes(title_text="Year")

# Set y-axes titles
fig.update_yaxes(title_text="émissions de CO2", secondary_y=False)
fig.update_yaxes(title_text="évènements extrêmes", secondary_y=True)

st.plotly_chart(fig)
