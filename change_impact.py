import streamlit as st
import plotly.express as px
from functions import load_dataset
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# DATA PREPARATION
# Load dataset
df, metadata = load_dataset("annual-co2-including-land-use")
# Sort dataset by year to correctly animate the graph
df = df.sort_values(by="Year", ascending=True)
# Remove aggregated categories from the dataframe
df = df[df["Code"].notna()]
df = df[df["Entity"] != "World"]

# PAGE DISPLAY
st.header("Les impacts du changement climatique")
st.subheader("Le CO²")
fig = px.choropleth(
    df,
    locations="Code",
    color="emissions_total_including_land_use_change",
    range_color=[0, df["emissions_total_including_land_use_change"].max()],
    hover_name="Entity",
    color_continuous_scale="YlOrRd",
    projection="natural earth",
    title="Émissions de CO₂",
    labels={"emissions_total_including_land_use_change": "Émissions CO₂"},
    animation_frame="Year",
)
fig.update_layout(transition={"duration": 0}, width=900, height=600)
st.plotly_chart(fig)



st.subheader("Les sécheresses")
# Load dataset
df1, metadata1 = load_dataset("annual-co2-including-land-use")
df2, metadata2 = load_dataset("number-of-natural-disaster-events")
# Sort dataset by year to correctly animate the graph
df1 = df1.sort_values(by="Year", ascending=True)
# Remove aggregated categories from the dataframe
df1 = df1[df1["Code"].notna()]
df1 = df1[df1["Entity"] == "World"]

df2 = df2[df2["Entity"] == "Drought"]

# Create figure with secondary y-axis
fig2 = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
fig2.add_trace(
    go.Scatter(x= df1["Year"], y= df1["emissions_total_including_land_use_change"], name= "CO²", line=dict(color="blue")),
    secondary_y=False,
)

fig2.add_trace(
    go.Scatter(x=df2["Year"], y= df2["n_events"], name= "sécheresses", line=dict(color="red")),
    secondary_y=True,
)

# Add figure title
fig2.update_layout(
    title_text="Évolution du nombre de sécheresses et des émissions de CO²"
)

# Set x-axis title
fig2.update_xaxes(title_text="Year")

# Set y-axes titles
fig2.update_yaxes(title_text="émissions de CO2", secondary_y=False)
fig2.update_yaxes(title_text="sécheresses", secondary_y=True)

st.plotly_chart(fig2)
