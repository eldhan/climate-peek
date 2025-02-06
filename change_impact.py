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


# Chargement des données
df_gaz = pd.read_csv("datasets/global-warming-by-gas-and-source.csv")

# Garder uniquement les données mondiales
df_gaz = df_gaz[df_gaz["Entity"] == "World"]

# Sélectionner les colonnes des émissions
gas_columns = df_gaz.columns[3:]  # Exclure 'Entity', 'Code' et 'Year'

# PAGE DISPLAY
st.header("Impact des gaz à effet de serre sur le réchauffement climatique")
st.subheader("Évolution de l'augmentation de la température mondiale")

# Traduction des légendes
translations = {
    "Change in global mean surface temperature caused by nitrous oxide emissions from fossil fuels and industry": "N₂O - Industrie",
    "Change in global mean surface temperature caused by nitrous oxide emissions from agriculture and land use": "N₂O - Agriculture",
    "Change in global mean surface temperature caused by methane emissions from fossil fuels and industry": "CH₄ - Industrie",
    "Change in global mean surface temperature caused by methane emissions from agriculture and land use": "CH₄ - Agriculture",
    "Change in global mean surface temperature caused by CO₂ emissions from fossil fuels and industry": "CO₂ - Industrie",
    "Change in global mean surface temperature caused by CO₂ emissions from agriculture and land use": "CO₂ - Agriculture",
}

# Appliquer les traductions aux colonnes
df_gaz.rename(columns=translations, inplace=True)
translated_columns = list(translations.values())  # Liste des nouvelles légendes

# figure Plotly
fig = go.Figure()

# Ajouter chaque type d'émission avec les noms traduits
for gas in translated_columns:
    fig.add_trace(go.Scatter(x=df_gaz["Year"], y=df_gaz[gas], mode="lines", name=gas))

# Personnalisation du graphique
fig.update_layout(
    title_text="Évolution de l'impact des gaz à effet de serre sur la température mondiale",
    xaxis_title="Année",
    yaxis_title="Changement de température (°C)",
    legend_title="Types d'émissions",
    legend=dict(orientation="h", y=-0.2),
)

# Affichage du graphique
st.plotly_chart(fig)
