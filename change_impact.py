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

st.subheader("Les évènements climatiques extrêmes vs les émissions de CO²")
# Load dataset
df1, metadata1 = load_dataset("annual-co2-including-land-use")
df2, metadata2 = load_dataset("number-of-natural-disaster-events")
# Sort dataset by year to correctly animate the graph
df1 = df1.sort_values(by="Year", ascending=True)
# Remove aggregated categories from the dataframe
df1 = df1[df1["Code"].notna()]
df1 = df1[df1["Entity"] == "World"]

df2 = df2[(df2["Entity"] == "Flood") | (df2["Entity"] == "Drought") | (df2["Entity"] == "Wildfire") | (df2["Entity"] == "Extreme temperature") | (df2["Entity"] == "Extreme weather")]
df_filter = st.selectbox(
    label="Sélectionnez un filtre : ", options=df2["Entity"].drop_duplicates()
)

# Create figure with secondary y-axis
fig2 = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
fig2.add_trace(
    go.Scatter(x= df1["Year"], y= df1["emissions_total_including_land_use_change"], name= "émissions de co²", line=dict(color="blue")),
    secondary_y=False,
)

if df_filter:
  fig2.add_trace(
      go.Scatter(x=df2[df2["Entity"] == df_filter]["Year"], y= df2[df2["Entity"] == df_filter]["n_events"], name= "nombre d'évènements extrêmes", line=dict(color="red")),
      secondary_y=True,
  )

# Add figure title
fig2.update_layout(
    title_text="Évolution du nombre d'évènements climatiques extrêmes et des émissions de CO²"
)

# Set x-axis title
fig2.update_xaxes(title_text="Year")

# Set y-axes titles
fig2.update_yaxes(title_text="émissions de CO2", secondary_y=False)
fig2.update_yaxes(title_text="évènements extrêmes", secondary_y=True)

st.plotly_chart(fig2)

