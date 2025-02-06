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
    et des émissions de CO²""",
    legend=dict(orientation="h", y=-0.2)
)

# Set x-axis title
fig.update_xaxes(title_text="Year")

# Set y-axes titles
fig.update_yaxes(title_text="émissions de CO2", secondary_y=False)
fig.update_yaxes(title_text="évènements extrêmes", secondary_y=True)

st.plotly_chart(fig)


# MONTEE DES EAUX
st.subheader("La montée du niveau des océans")

#df3, metadata3 = load_dataset("sea-level")
df3 = pd.read_csv("datasets/sea-level.csv")
df3["Day"] = pd.to_datetime(df3["Day"])
df3["Year"] = df3["Day"].dt.year
df3 = df3.drop_duplicates(subset = "Year", keep = "last")


# Create figure with secondary y-axis
fig2 = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
fig2.add_trace(
    go.Scatter(x= df1["Year"], y= df1["Annual CO₂ emissions including land-use change"], name= "émissions de co² mondiales", line=dict(color="blue")),
    secondary_y=False,
)


fig2.add_trace(
    go.Scatter(x= df3["Year"], y= df3["Global sea level as an average of Church and White (2011) and UHSLC data"], name= "niveau des océans", line=dict(color="red")),
    secondary_y=True,
)

# Add figure title
fig2.update_layout(
    title_text="Évolution du niveau moyen des océans vs les émissions de CO² mondiales",
    legend=dict(orientation="h", y=-0.2)
)

# Set x-axis title
fig2.update_xaxes(title_text="Année")

# Set y-axes titles
fig2.update_yaxes(title_text="émissions de CO2", secondary_y=False)
fig2.update_yaxes(title_text="niveau des océans", secondary_y=True)

st.plotly_chart(fig2)


# TEMPERATURE DES OCEANS
st.subheader("L'augmentation de la température des océans")

# on transforme les dates en années
df4 = pd.read_csv("datasets/sea-surface-temperature-anomaly.csv")
#df4, metadata4 = load_dataset("sea-surface-temperature-anomaly")

# supprimer la virgule dans l'année
#df4['Year'] = df4['Year'] = df4['Year'].astype(str).str.replace(',', '').astype(int)
df4 = df4[df4['Entity'] == 'Global']

# Create figure with secondary y-axis
fig3 = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
fig3.add_trace(
    go.Scatter(x= df1["Year"], y= df1["Annual CO₂ emissions including land-use change"], name= "émissions de co² mondiales", line=dict(color="blue")),
    secondary_y=False,
)


fig3.add_trace(
    go.Scatter(x= df4["Year"], y= df4["Sea surface temperature anomaly (relative to 1961-90 average)"], name= "pH moyen annuel", line=dict(color="red")),
    secondary_y=True,
)

# Add figure title
fig3.update_layout(
    title_text="Évolution de la température moyenne des océans vs les émissions de CO² mondiales",
    legend=dict(orientation="h", y=-0.2)
)

# Set x-axis title
fig3.update_xaxes(title_text="Année")

# Set y-axes titles
fig3.update_yaxes(title_text="émissions de CO2", secondary_y=False)
fig3.update_yaxes(title_text="température moyenne des océans", secondary_y=True)

st.plotly_chart(fig3)


# ACIFIFICATION
st.subheader("L'acidification des océans")

# on transforme les dates en années
df5 = pd.read_csv("datasets/seawater-ph.csv")
#df5, metadata5 = load_dataset("seawater-ph")
df5["Day"] = pd.to_datetime(df5["Day"])
df5["Year"] = df5["Day"].dt.year
df5 = df5.drop_duplicates(subset = "Year", keep = "last")

df1 = df1.drop(df1[df1["Year"] < 1988].index)

# Create figure with secondary y-axis
fig4 = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
fig4.add_trace(
    go.Scatter(x= df1["Year"], y= df1["Annual CO₂ emissions including land-use change"], name= "émissions de co² mondiales", line=dict(color="blue")),
    secondary_y=False,
)


fig4.add_trace(
    go.Scatter(x= df5["Year"], y= df5["Rolling yearly average of ocean pH levels"], name= "pH moyen annuel", line=dict(color="red")),
    secondary_y=True,
)

# Add figure title
fig4.update_layout(
    title_text="Évolution du ph moyen annuel de l'océan à Hawaï vs les émissions de CO² mondiales",
    legend=dict(orientation="h", y=-0.2)
)

# Set x-axis title
fig4.update_xaxes(title_text="Année")

# Set y-axes titles
fig4.update_yaxes(title_text="émissions de CO2", secondary_y=False)
fig4.update_yaxes(title_text="pH des océans", secondary_y=True)

st.plotly_chart(fig4)


# FONTE DES GLACES
st.subheader("La fonte des glaces")

# on transforme les dates en années
df6 = pd.read_csv("datasets/ice-sheet-mass-balance.csv")
#df6, metadata6= load_dataset("ice-sheet-mass-balance")
df6["Day"] = pd.to_datetime(df6["Day"])
df6["Year"] = df6["Day"].dt.year
df6 = df6.drop_duplicates(subset = "Year", keep = "last")

df1 = df1.drop(df1[df1["Year"] < 2002].index)

# Create figure with secondary y-axis
fig5 = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
fig5.add_trace(
    go.Scatter(x= df1["Year"], y= df1["Annual CO₂ emissions including land-use change"], name= "émissions de co² mondiales", line=dict(color="blue")),
    secondary_y=False,
)


fig5.add_trace(
    go.Scatter(x= df6["Year"], y= df6["Cumulative change in mass in the ice sheets, according to NASA/JPL"], name= "masse de glace", mode = "lines", line=dict(color="red")),
    secondary_y=True,
)

# Add figure title
fig5.update_layout(
    title_text="Évolution de la masse de glace au Groenland vs les émissions de CO² mondiales",
    legend=dict(orientation="h", y=-0.2)
)

# Set x-axis title
fig5.update_xaxes(title_text="Année")

# Set y-axes titles
fig5.update_yaxes(title_text="émissions de CO2", secondary_y=False)
fig5.update_yaxes(title_text="masse annuelle de glace", secondary_y=True)

st.plotly_chart(fig5)