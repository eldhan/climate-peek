import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from functions import get_dataset


st.header("Les impacts terrestres du changement climatique")

st.markdown(
    "L’augmentation des émissions de GES a d’énormes conséquences sur la planète, notamment au niveau du climat."
)
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

    # PAGE DISPLAY

    st.subheader("Les anomalies de température et de précipitations")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(
            """
        Les anomalies au niveau des températures et des précipitations augmentent de plus en plus, suivant la courbe de croissance des émissions de CO2. On l’a dit, les températures mondiales augmentent à cause de l’effet de serre qui s’intensifie. L’air étant plus chaud, il contient plus d’humidité, faisant s’accroître les pluies.
        """
        )

    with col2:

        st.image("assets/innondation.jpg")

    on = st.toggle("Comparer deux zones")

    if not on:
        df_filter = st.selectbox(
            label="Sélectionnez un filtre : ", options=filter_options, index=world_index
        )
        if df_filter:
            df0 = df[df["Entity"] == df_filter]
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(
                go.Scatter(
                    x=df0["Year"],
                    y=df0["Temperature anomaly"],
                    name="anomalies de température (degrés)",
                    line=dict(color="red"),
                ),
                secondary_y=False,
            )
            fig.add_trace(
                go.Scatter(
                    x=df0["Year"],
                    y=df0["Annual precipitation anomaly"] / 100,
                    name="anomalies de précipitations (cm)",
                    line=dict(color="orange"),
                ),
                secondary_y=False,
            )
            fig.add_trace(
                go.Scatter(
                    x=df1["Year"],
                    y=df1["Annual CO₂ emissions including land-use change"],
                    name="émissions de co² dans le monde (milliards de tonnes)",
                    line=dict(color="blue"),
                ),
                secondary_y=True,
            )
            fig.update_layout(legend=dict(orientation="h", y=-0.2))
            st.plotly_chart(fig)
    else:
        col1, col2 = st.columns(2)
        with col1:
            df_filter = st.selectbox(
                label="Sélectionnez un filtre : ",
                options=filter_options,
                index=world_index,
            )
            if df_filter:
                df2 = df[df["Entity"] == df_filter]
                fig = make_subplots(specs=[[{"secondary_y": True}]])
                fig.add_trace(
                    go.Scatter(
                        x=df2["Year"],
                        y=df2["Temperature anomaly"],
                        name="anomalies de température (degrés)",
                        line=dict(color="red"),
                    ),
                    secondary_y=False,
                )
                fig.add_trace(
                    go.Scatter(
                        x=df2["Year"],
                        y=df2["Annual precipitation anomaly"] / 100,
                        name="anomalies de précipitations (cm)",
                        line=dict(color="orange"),
                    ),
                    secondary_y=False,
                )
                fig.add_trace(
                    go.Scatter(
                        x=df1["Year"],
                        y=df1["Annual CO₂ emissions including land-use change"],
                        name="émissions de co² dans le monde (milliards de tonnes)",
                        line=dict(color="blue"),
                    ),
                    secondary_y=True,
                )
                fig.update_layout(legend=dict(orientation="h", y=-0.2))
                st.plotly_chart(fig, key="filter11")

        with col2:
            df_filter2 = st.selectbox(
                label="Sélectionnez un filtre : ", options=filter_options, key="filter2"
            )

            if df_filter:
                df2 = df[df["Entity"] == df_filter]
                fig = make_subplots(specs=[[{"secondary_y": True}]])
                fig.add_trace(
                    go.Scatter(
                        x=df2["Year"],
                        y=df2["Temperature anomaly"],
                        name="anomalies de température (degrés)",
                        line=dict(color="red"),
                    ),
                    secondary_y=False,
                )
                fig.add_trace(
                    go.Scatter(
                        x=df2["Year"],
                        y=df2["Annual precipitation anomaly"] / 100,
                        name="anomalies de précipitations (cm)",
                        line=dict(color="orange"),
                    ),
                    secondary_y=False,
                )
                fig.add_trace(
                    go.Scatter(
                        x=df1["Year"],
                        y=df1["Annual CO₂ emissions including land-use change"],
                        name="émissions de co² dans le monde (milliards de tonnes)",
                        line=dict(color="blue"),
                    ),
                    secondary_y=True,
                )
                fig.update_layout(legend=dict(orientation="h", y=-0.2))
                st.plotly_chart(fig, key="filter22")
else:
    st.write("Une erreur a été rencontré")
    # Ajouter un espace entre les paragraphes
st.markdown("<br><br>", unsafe_allow_html=True)

# Load dataset
dataset_disasters = get_dataset("number-of-natural-disaster-events")
if dataset_disasters != "error":
    df2 = pd.read_csv(f"datasets/{dataset_disasters}")

    # Remove aggregated categories from the dataframe
    df_co2 = df_co2[df_co2["Code"].notna()]
    df_co2 = df_co2[df_co2["Entity"] == "World"]

    df2 = df2[
        (df2["Entity"] == "Flood")
        | (df2["Entity"] == "Drought")
        | (df2["Entity"] == "Wildfire")
        | (df2["Entity"] == "Extreme temperature")
        | (df2["Entity"] == "Extreme weather")
    ]

    st.subheader("Les évènements climatiques extrêmes")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.image("assets/innondation.jpg")

    with col2:
        st.markdown(
            """
        Ce dérèglement des températures et des précipitations dû à l’augmentation de l’effet de serre provoque une augmentation des évènements climatiques extrêmes comme les sécheresses, les inondations ou encore les cyclones.
        """
        )

    df_filter = st.selectbox(
        label="Sélectionnez un évènement climatique : ",
        options=df2["Entity"].drop_duplicates(),
    )

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Scatter(
            x=df_co2["Year"],
            y=df_co2["Annual CO₂ emissions including land-use change"],
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
        title_text="Évolution du nombre d'évènements climatiques extrêmes et des émissions de CO²",
        legend=dict(orientation="h", y=-0.2),
    )
    st.plotly_chart(fig)

else:
    st.write("Une erreur a été rencontré.")
# Ajouter un espace entre les paragraphes
st.markdown("<br><br>", unsafe_allow_html=True)

# FONTE DES GLACES
st.subheader("La fonte des glaces")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(
        """
    On parle de fonte des glaces pour désigner l’accélération rapide de la disparition des glaciers durant les dernières décennies. Avec le réchauffement climatique, les glaces fondent de plus en plus tôt (trois fois plus rapidement qu’avant) et ont de plus en plus de mal à se reformer en hiver. Selon certaines études, plus de 28 000 tonnes de glaces ont disparu depuis 1994.
    """
    )

with col2:

    st.image("assets/glace.jpg")

dataset_icesheet = get_dataset("ice-sheet-mass-balance")
if dataset_icesheet != "error":
    df6 = pd.read_csv(f"datasets/{dataset_icesheet}")

    # on transforme les dates en années
    df6["Day"] = pd.to_datetime(df6["Day"])
    df6["Year"] = df6["Day"].dt.year
    df6 = df6.drop_duplicates(subset="Year", keep="last")

    df_co2 = df_co2.drop(df_co2[df_co2["Year"] < 2002].index)

    # Create figure with secondary y-axis
    fig5 = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig5.add_trace(
        go.Scatter(
            x=df_co2["Year"],
            y=df_co2["Annual CO₂ emissions including land-use change"],
            name="émissions de co² mondiales",
            line=dict(color="blue"),
        ),
        secondary_y=False,
    )

    fig5.add_trace(
        go.Scatter(
            x=df6["Year"],
            y=df6["Cumulative change in mass in the ice sheets, according to NASA/JPL"],
            name="masse de glace",
            mode="lines",
            line=dict(color="red"),
        ),
        secondary_y=True,
    )

    # Add figure title
    fig5.update_layout(
        title_text="Évolution de la masse de glace au Groenland vs les émissions de CO² mondiales",
        legend=dict(orientation="h", y=-0.2),
    )

    # Set x-axis title
    fig5.update_xaxes(title_text="Année")

    # Set y-axes titles
    fig5.update_yaxes(title_text="émissions de CO2", secondary_y=False)
    fig5.update_yaxes(title_text="masse annuelle de glace", secondary_y=True)

    st.plotly_chart(fig5)
else:
    st.write("Une erreur a été rencontré")
