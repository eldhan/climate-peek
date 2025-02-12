import streamlit as st
import plotly.express as px
import pandas as pd
from functions import get_dataset


with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("# Climate Peek")
st.markdown("### Un aperçu du changement climatique")
st.markdown("<br>", unsafe_allow_html=True)

# Créer deux colonnes
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(
        "Analyse de l'impact du changement climatique sur les conditions météorologiques à travers le monde et mise en évidence des tendances de pollution de l'air dans différentes régions."
    )
    st.markdown(
        """
    Certains gaz présents dans l’atmosphère, comme le CO2, la vapeur d’eau ou encore le méthane, retiennent la chaleur du soleil, et sans eux, la température moyenne de la planète serait de -18°C ! C’est ce qu’on appelle **l’effet de serre**, et on nomme ces gaz les GES (Gaz à Effet de Serre). Le problème, c’est que les activités humaines telles que la combustion du gaz, du pétrole, la déforestation, etc, émettent énormément de GES. Depuis 1850, la température moyenne de la planète a augmenté de plus de 1°C ! Le CO² représente à lui seul les **⅔ des émissions** de GES.
    """
    )

with col2:

    st.image("assets/climate_peek_intro.jpg")

# DATA PREPARATION
# Load dataset
dataset_ghg = get_dataset("total-ghg-emissions")
if dataset_ghg != "error":
    df = pd.read_csv(f"datasets/{dataset_ghg}")
    # Sort dataset by year to correctly animate the graph
    df = df.sort_values(by="Year", ascending=True)
    # Remove aggregated categories from the dataframe
    df = df[df["Code"].notna()]
    df = df[df["Entity"] != "World"]

    # PAGE DISPLAY
    fig = px.choropleth(
        df,
        locations="Code",
        color="Annual greenhouse gas emissions in CO₂ equivalents",
        range_color=[5e6, 8e9],
        hover_name="Entity",
        color_continuous_scale="YlOrRd",
        projection="natural earth",
        title="Émissions GES",
        labels={
            "Annual greenhouse gas emissions in CO₂ equivalents": "Émissions GES (équivalent CO₂)"
        },
        animation_frame="Year",
    )
    fig.update_layout(transition={"duration": 0}, width=900, height=600)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.write("Une erreur a été rencontré")
