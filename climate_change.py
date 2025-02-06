import streamlit as st
import plotly.express as px
import pandas as pd


st.header("Climate Peek")
st.subheader("Un aperçu du changement climatique")
st.write(
    "Analyse de l'impact du changement climatique sur les conditions météorologiques à travers le monde et mise en évidence des tendances de pollution de l'air dans différentes régions."
)


# DATA PREPARATION
# Load dataset
df = pd.read_csv("datasets/annual-co2-including-land-use.csv")
# Sort dataset by year to correctly animate the graph
df = df.sort_values(by="Year", ascending=True)
# Remove aggregated categories from the dataframe
df = df[df["Code"].notna()]
df = df[df["Entity"] != "World"]

# PAGE DISPLAY
fig = px.choropleth(
    df,
    locations="Code",
    color="Annual CO₂ emissions including land-use change",
    range_color=[0, df["Annual CO₂ emissions including land-use change"].max()],
    hover_name="Entity",
    color_continuous_scale="YlOrRd",
    projection="natural earth",
    title="Émissions de CO₂",
    labels={"Annual CO₂ emissions including land-use change": "Émissions CO₂"},
    animation_frame="Year",
)
fig.update_layout(transition={"duration": 0}, width=900, height=600)
st.plotly_chart(fig)
