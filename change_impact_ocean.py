import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from functions import get_dataset


st.header("Les impacts océaniques du changement climatique")
# DATA PREPARATION
# Load datasets required for graph comparisons
dataset_temperature = get_dataset("annual-temperature-anomalies")
dataset_precipitation = get_dataset("global-precipitation-anomaly")
dataset_co2 = get_dataset("annual-co2-including-land-use")
if (
    dataset_temperature != "error"
    and dataset_precipitation != "error"
    and dataset_co2 != "error"
):
    df_temperature_anomaly = pd.read_csv(f"datasets/{dataset_temperature}")
    df_precipation_anomaly = pd.read_csv(f"datasets/{dataset_precipitation}")
    df_co2 = pd.read_csv(f"datasets/{dataset_co2}")

    # Merge the datasets together to display them on the same graph
    df_anomalies = pd.merge(
        df_temperature_anomaly,
        df_precipation_anomaly,
        how="inner",
        on=["Entity", "Code", "Year"],
    )
    df = pd.merge(df_anomalies, df_co2, how="inner", on=["Entity", "Code", "Year"])

    # Prepare filters
    filter_options = df["Entity"].drop_duplicates()
    world_index = 175

    # Dataframe for world values only
    df1 = df[df["Entity"] == "World"]

    # Remove aggregated categories from the dataframe
    df_co2 = df_co2[df_co2["Code"].notna()]
    df_co2 = df_co2[df_co2["Entity"] == "World"]

st.markdown(
    "Les océans, poumons bleus de la Terre, subissent de plein fouet le réchauffement climatique : leurs eaux se réchauffent, s’acidifient et montent, mettant en péril la vie marine."
)

# MONTEE DES EAUX
st.subheader("La montée du niveau des océans")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(
        "La montée des eaux, accélérée par la fonte des glaces et le réchauffement des océans, redessine les côtes et menace des millions de personnes."
    )
    st.markdown(
        """
    Littoraux grignotés par l’érosion, inondations plus fréquentes, habitats naturels en danger : l’équilibre fragile entre terre et mer est bouleversé. Pour protéger les populations et préserver la biodiversité, il devient essentiel d’agir, en adaptant nos infrastructures et en renforçant les écosystèmes côtiers.
    """
    )

with col2:

    st.image("assets/erosion.jpeg")

dataset_sea_levels = get_dataset("sea-level")
if dataset_sea_levels != "error":
    df3 = pd.read_csv(f"datasets/{dataset_sea_levels}")
    df3["Day"] = pd.to_datetime(df3["Day"])
    df3["Year"] = df3["Day"].dt.year
    df3 = df3.drop_duplicates(subset="Year", keep="last")

    # Create figure with secondary y-axis
    fig2 = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig2.add_trace(
        go.Scatter(
            x=df_co2["Year"],
            y=df_co2["Annual CO₂ emissions including land-use change"],
            name="émissions de co² mondiales",
            line=dict(color="blue"),
        ),
        secondary_y=False,
    )

    fig2.add_trace(
        go.Scatter(
            x=df3["Year"],
            y=df3[
                "Global sea level as an average of Church and White (2011) and UHSLC data"
            ],
            name="niveau des océans",
            line=dict(color="red"),
        ),
        secondary_y=True,
    )

    # Add figure title
    fig2.update_layout(
        title_text="Évolution du niveau moyen des océans vs les émissions de CO² mondiales",
        legend=dict(orientation="h", y=-0.2),
    )

    # Set x-axis title
    fig2.update_xaxes(title_text="Année")

    # Set y-axes titles
    fig2.update_yaxes(title_text="émissions de CO2", secondary_y=False)
    fig2.update_yaxes(title_text="niveau des océans", secondary_y=True)

    st.plotly_chart(fig2)
else:
    st.write("Une erreur a été rencontré.")

# Ajouter un espace entre les paragraphes
st.markdown("<br><br>", unsafe_allow_html=True)

# TEMPERATURE DES OCEANS
st.subheader("L'augmentation de la température des océans")

col1, col2 = st.columns([1, 2])

with col1:
    st.image("assets/ocean.jpeg")


with col2:
    st.markdown(
        "Le réchauffement des océans bouleverse les écosystèmes marins et fragilise la vie sous-marine."
    )
    st.markdown(
        """
    Coraux blanchis, migrations forcées des espèces, perturbation des courants : l’équilibre des océans est en danger. Cette hausse des températures intensifie aussi les tempêtes et aggrave la montée des eaux. Face à ces menaces, protéger les océans et limiter le réchauffement climatique est plus que jamais une urgence.
    """
    )

dataset_sea_surface = get_dataset("sea-surface-temperature-anomaly")
if dataset_sea_surface != "error":
    # on transforme les dates en années
    df4 = pd.read_csv(f"datasets/{dataset_sea_surface}")

    # supprimer la virgule dans l'année
    # df4['Year'] = df4['Year'] = df4['Year'].astype(str).str.replace(',', '').astype(int)
    df4 = df4[df4["Entity"] == "Global"]

    # Create figure with secondary y-axis
    fig3 = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig3.add_trace(
        go.Scatter(
            x=df_co2["Year"],
            y=df_co2["Annual CO₂ emissions including land-use change"],
            name="émissions de co² mondiales",
            line=dict(color="blue"),
        ),
        secondary_y=False,
    )

    fig3.add_trace(
        go.Scatter(
            x=df4["Year"],
            y=df4["Sea surface temperature anomaly (relative to 1961-90 average)"],
            name="anomalies de températures",
            line=dict(color="red"),
        ),
        secondary_y=True,
    )

    # Add figure title
    fig3.update_layout(
        title_text="Évolution de la température moyenne des océans vs les émissions de CO² mondiales",
        legend=dict(orientation="h", y=-0.2),
    )

    # Set x-axis title
    fig3.update_xaxes(title_text="Année")

    # Set y-axes titles
    fig3.update_yaxes(title_text="émissions de CO2", secondary_y=False)
    fig3.update_yaxes(title_text="température moyenne des océans", secondary_y=True)

    st.plotly_chart(fig3)
else:
    st.write("Une erreur a été rencontré.")

# Ajouter un espace entre les paragraphes
st.markdown("<br><br>", unsafe_allow_html=True)

# ACIFIFICATION
st.subheader("L'acidification des océans")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(
        "L’acidification des océans, causée par l’absorption croissante du CO₂ atmosphérique, perturbe profondément les écosystèmes marins."
    )
    st.markdown(
        """
    En abaissant le pH de l’eau, elle fragilise les organismes calcifiants comme les coraux, les mollusques et certains crustacés, compromettant leur capacité à construire leurs coquilles et squelettes. Cette transformation chimique bouleverse la chaîne alimentaire et menace les ressources halieutiques dont dépendent des millions de personnes. À mesure que l’acidité des océans augmente, la biodiversité marine s’affaiblit, mettant en péril la pêche et l’équilibre écologique global. Agir pour limiter les émissions de CO₂ est essentiel pour préserver la santé des océans et leur rôle vital dans la régulation du climat.
    """
    )

with col2:

    st.image("assets/coraux.jpeg")

dataset_seawaterph = get_dataset("seawater-ph")
if dataset_seawaterph != "error":
    df5 = pd.read_csv(f"datasets/{dataset_seawaterph}")

    # on transforme les dates en années
    df5["Day"] = pd.to_datetime(df5["Day"])
    df5["Year"] = df5["Day"].dt.year
    df5 = df5.drop_duplicates(subset="Year", keep="last")

    df_co2 = df_co2.drop(df_co2[df_co2["Year"] < 1988].index)

    # Create figure with secondary y-axis
    fig4 = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig4.add_trace(
        go.Scatter(
            x=df_co2["Year"],
            y=df_co2["Annual CO₂ emissions including land-use change"],
            name="émissions de co² mondiales",
            line=dict(color="blue"),
        ),
        secondary_y=False,
    )

    fig4.add_trace(
        go.Scatter(
            x=df5["Year"],
            y=df5["Rolling yearly average of ocean pH levels"],
            name="pH moyen annuel",
            line=dict(color="red"),
        ),
        secondary_y=True,
    )

    # Add figure title
    fig4.update_layout(
        title_text="Évolution du ph moyen annuel de l'océan à Hawaï vs les émissions de CO² mondiales",
        legend=dict(orientation="h", y=-0.2),
    )

    # Set x-axis title
    fig4.update_xaxes(title_text="Année")

    # Set y-axes titles
    fig4.update_yaxes(title_text="émissions de CO2", secondary_y=False)
    fig4.update_yaxes(title_text="pH des océans", secondary_y=True)

    st.plotly_chart(fig4)
else:
    st.write("Une erreur a été rencontré.")

# Ajouter un espace entre les paragraphes
st.markdown("<br><br>", unsafe_allow_html=True)
