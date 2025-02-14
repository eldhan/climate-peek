import streamlit as st
import plotly.express as px
import pandas as pd
from functions import get_dataset, check_datasets


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
# List of datasets
DATASETS = [
    "total-ghg-emissions",
    "annual-co2-including-land-use",
    "annual-temperature-anomalies",
    "global-precipitation-anomaly",
    "number-of-natural-disaster-events",
    "global-warming-by-gas-and-source",
    "ice-sheet-mass-balance",
    "sea-level",
    "sea-surface-temperature-anomaly",
    "seawater-ph",
    "tree-cover-loss",
]
check_datasets(DATASETS)
# Load dataset
dataset_ghg = get_dataset("total-ghg-emissions")
if dataset_ghg != "error":
    df = pd.read_csv(f"datasets/{dataset_ghg}")
    # DATA PREPARATION
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
            "Annual greenhouse gas emissions in CO₂ equivalents": "Émissions GES (équivalent CO₂)",
            "Year": "Année",
        },
        animation_frame="Year",
    )
    fig.update_layout(transition={"duration": 0}, width=900, height=600)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.write("Une erreur a été rencontré")

# Préchargement du webscrapping helium pour la page today

import requests
from datetime import datetime
import pytz
from bs4 import BeautifulSoup
import re
from helium import start_firefox, click, kill_browser

def format_data(txt):
    if txt == "n/a":
        return "Pas de Données"
    else:
        return re.sub(
            r"([\d.]+ ppm) increase (\([\d.]+ %\)) *", r"Augmentation de \1 \2", txt
        )


def translate_no_data_fr(txt):
    if txt == "Unavailable":
        return "Pas de données"
    else:
        return txt


def format_date_table(table_date):
    table_date = datetime.strptime(table_date, "%b. %d, %Y")
    table_months = months[table_date.strftime("%b")]
    table_date = f"{table_date.day} {table_months} {table_date.year}"
    return table_date


months = {
    "Jan": "janvier",
    "Feb": "février",
    "Mar": "mars",
    "Apr": "avril",
    "May": "mai",
    "Jun": "juin",
    "Jul": "juillet",
    "Aug": "août",
    "Sep": "septembre",
    "Oct": "octobre",
    "Nov": "novembre",
    "Dec": "décembre",
}

# Initialize session states
if "data_retrieved" not in st.session_state:
    st.session_state.data_retrieved = False
    st.session_state.date = False
    st.session_state.tabledate = False
    st.session_state.change = False
    st.session_state.tableppm = False
    st.session_state.ppm = False


if st.session_state.data_retrieved is False:
    url = start_firefox("https://www.co2.earth/daily-co2", headless=True)
    click("6 Decades")
    page_source = url.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    tab = soup.find("div", {"id": "DecadeDailyPanel"})
    kill_browser()

    date = re.search(r"<td><span>(.*)</span> </td>", str(tab)).group(1)
    date = datetime.strptime(date, "%b. %d, %Y")
    month = months[date.strftime("%b")]
    ppm = re.search(r'<td class="alt-col"><span>(.*)</span></td>', str(tab)).group(
        1
    )
    tabledate = re.findall(r"<td>(\w{3}\.\s\d+\,\s\d+)</td>", str(tab))
    tableppm = re.findall(
        r'<td class="alt-col">(\d{3}\..+|Unavailable)</td>', str(tab)
    )
    change = re.findall(r"<td><span class=.*>(.*) </span></td>", str(tab))
    change = change[1:]

    st.session_state.date = f"{date.day} {month} {date.year}"
    st.session_state.change = [format_data(txt) for txt in change]
    st.session_state.tableppm = [translate_no_data_fr(txt) for txt in tableppm]
    st.session_state.ppm = translate_no_data_fr(ppm)
    st.session_state.tabledate = [format_date_table(table_date) for table_date in tabledate]
    st.session_state.data_retrieved = True