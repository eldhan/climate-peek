import streamlit as st
import plotly.express as px
from functions import load_dataset


st.header("Les impacts du changement climatique")
st.subheader("Le CO²")
# Load dataset
df, metadata = load_dataset("annual-co2-including-land-use")
# Sort dataset by year to correctly animate the graph
df = df.sort_values(by="Year", ascending=True)
# Remove aggregated categories from the dataframe
df = df[df["Code"].notna()]

fig = px.choropleth(
    df,
    locations="Code",
    color="emissions_total_including_land_use_change",
    hover_name="Entity",
    color_continuous_scale="Reds",
    projection="natural earth",
    title="Émissions de CO₂",
    labels={"emissions_total_including_land_use_change": "Émissions CO₂"},
    animation_frame="Year",
)
fig.update_layout(transition={"duration": 5})
st.plotly_chart(fig)
