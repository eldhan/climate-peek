import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd


st.header("Les causes de l'augmentation de l'effet de serre")

st.write("L'augmentation des émissions de gaz à effet de serre est fortement liée aux activités humaines.")

# CORRELATION ENTRE LES EMISSIONS DE CO2 ET LES ACTIVITES HUMAINES
# Chargement des données
df_gaz = pd.read_csv("datasets/global-warming-by-gas-and-source.csv")

# Garder uniquement les données mondiales
df_gaz = df_gaz[df_gaz["Entity"] == "World"]

# Sélectionner les colonnes des émissions
gas_columns = df_gaz.columns[3:]  # Exclure 'Entity', 'Code' et 'Year'

# PAGE DISPLAY

st.subheader("Les sources d'émissions des GES")

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
    title_text="Évolution de la température mondiale en fonction des GES",
    xaxis_title="Année",
    yaxis_title="Changement de température (°C)",
    legend_title="Types d'émissions",
    legend=dict(orientation="h", y=-0.2),
)

# Affichage du graphique
st.plotly_chart(fig)

# Ajouter un espace entre les paragraphes
st.markdown("<br><br>", unsafe_allow_html=True)

# CORRELATION ENTRE LA DEFORESTATION ET LES EMISSIONS DE CO2
st.subheader("La perte de surfaces boisées")

df_co2 = pd.read_csv("datasets/annual-co2-including-land-use.csv")
df_forest = pd.read_csv("datasets/tree-cover-loss.csv")

# on ne garde que les données mondiales
df_co2 = df_co2[df_co2["Entity"] == "World"]
df_forest = df_forest[df_forest["Entity"] == "World"]

df_co2 = df_co2.drop(df_co2[df_co2["Year"] < 2001].index)

# Create figure with secondary y-axis
fig2 = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
fig2.add_trace(
    go.Scatter(x= df_co2["Year"], y= df_co2["Annual CO₂ emissions including land-use change"], name= "émissions de co² mondiales", line=dict(color="blue")),
    secondary_y=False,
)


fig2.add_trace(
    go.Scatter(x= df_forest["Year"], y= df_forest["Total tree cover loss"], name= "perte annuelle mondiale de surfaces boisées", mode = "lines", line=dict(color="red")),
    secondary_y=True,
)

# Add figure title
fig2.update_layout(
    title_text="Évolution de la perte mondiale de surfaces boisées vs les émissions de CO² mondiales",
    legend=dict(orientation="h", y=-0.2)
)

# Set x-axis title
fig2.update_xaxes(title_text="Année")

# Set y-axes titles
fig2.update_yaxes(title_text="émissions de CO2", secondary_y=False)
fig2.update_yaxes(title_text="perte de surfaces boisées", secondary_y=True)

st.plotly_chart(fig2)
