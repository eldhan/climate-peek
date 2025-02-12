import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from functions import get_dataset


st.header("Les causes de l'augmentation de l'effet de serre")

st.markdown(
    "L'augmentation des émissions de gaz à effet de serre est fortement liée aux activités humaines."
)
st.markdown("<br>", unsafe_allow_html=True)

# CORRELATION ENTRE LES EMISSIONS DE CO₂ ET LES ACTIVITES HUMAINES
# Chargement des données
dataset_gaz = get_dataset("global-warming-by-gas-and-source")
if dataset_gaz != "error":
    df_gaz = pd.read_csv(f"datasets/{dataset_gaz}")

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

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(
            "Les émissions mondiales de GES proviennent principalement de la production d’énergie, qui repose encore largement sur les combustibles fossiles (charbon, pétrole, gaz)."
        )
        st.markdown(
            "Le secteur des transports contribue également de manière significative, notamment à travers l’aviation et le transport routier. L'industrie, avec la fabrication du ciment, de l'acier et des produits chimiques, joue aussi un rôle clé dans ces rejets. Enfin, l’agriculture participe à l’augmentation des GES, notamment par la production de méthane issue de l’élevage."
        )

    with col2:

        st.image("assets/usine.jpg")
    # figure Plotly
    fig = go.Figure()

    # Ajouter chaque type d'émission avec les noms traduits
    for gas in translated_columns:
        fig.add_trace(
            go.Scatter(x=df_gaz["Year"], y=df_gaz[gas], mode="lines", name=gas)
        )

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
else:
    st.write("Une erreur a été rencontré")

# Ajouter un espace entre les paragraphes
st.markdown("<br><br>", unsafe_allow_html=True)

# CORRELATION ENTRE LA DEFORESTATION ET LES EMISSIONS DE CO₂
st.subheader("La perte de surfaces boisées")

col1, col2 = st.columns([1, 2])

with col1:
    st.image("assets/foret.jpg")


with col2:
    st.markdown(
        "La déforestation est également  un facteur majeur d’augmentation des émissions de gaz à effet de serre."
    )
    st.markdown(
        "En détruisant les forêts, notamment pour l’agriculture, l’élevage ou l’exploitation du bois, on réduit la capacité de la planète à absorber le CO₂, principal gaz responsable du réchauffement climatique. De plus, la combustion et la décomposition des arbres libèrent directement du dioxyde de carbone dans l’atmosphère."
    )


dataset_co2 = get_dataset("annual-co2-including-land-use")
dataset_forest = get_dataset("tree-cover-loss")
if dataset_co2 != "error" and dataset_forest != "error":
    df_co2 = pd.read_csv(f"datasets/{dataset_co2}")
    df_forest = pd.read_csv(f"datasets/{dataset_forest}")

    # on ne garde que les données mondiales
    df_co2 = df_co2[df_co2["Entity"] == "World"]
    df_forest = df_forest[df_forest["Entity"] == "World"]

    df_co2 = df_co2.drop(df_co2[df_co2["Year"] < 2001].index)

    # Create figure with secondary y-axis
    fig2 = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig2.add_trace(
        go.Scatter(
            x=df_co2["Year"],
            y=df_co2["Annual CO₂ emissions including land-use change"],
            name="émissions de CO₂ mondiales",
            line=dict(color="blue"),
        ),
        secondary_y=False,
    )

    fig2.add_trace(
        go.Scatter(
            x=df_forest["Year"],
            y=df_forest["Total tree cover loss"],
            name="perte annuelle mondiale de surfaces boisées",
            mode="lines",
            line=dict(color="red"),
        ),
        secondary_y=True,
    )

    # Add figure title
    fig2.update_layout(
        title_text="Évolution de la perte mondiale de surfaces boisées vs les émissions de CO₂ mondiales",
        legend=dict(orientation="h", y=-0.2),
    )

    # Set x-axis title
    fig2.update_xaxes(title_text="Année")

    # Set y-axes titles
    fig2.update_yaxes(title_text="émissions de CO₂", secondary_y=False)
    fig2.update_yaxes(title_text="perte de surfaces boisées", secondary_y=True)

    st.plotly_chart(fig2)
else:
    st.write("Une erreur a été rencontré")
