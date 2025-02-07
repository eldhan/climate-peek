import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd



# DATA PREPARATION
# Load datasets required for graph comparisons
df_temperature_anomaly = pd.read_csv("datasets/annual-temperature-anomalies.csv")
df_precipation_anomaly = pd.read_csv("datasets/global-precipitation-anomaly.csv")
df_co2 = pd.read_csv("datasets/annual-co2-including-land-use.csv")

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
st.header("Les impacts du changement climatique")

on = st.toggle("Comparer deux zones")

st.subheader(
    "Corrélation entre les anomalies de température dans l'atmosphère et de précipitations et les émissions de CO² dans le monde"
)

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
            ),
            secondary_y=False,
        )
        fig.add_trace(
            go.Scatter(
                x=df0["Year"],
                y=df0["Annual precipitation anomaly"] / 100,
                name="anomalies de précipitations (cm)",
            ),
            secondary_y=False,
        )
        fig.add_trace(
            go.Scatter(
                x=df1["Year"],
                y=df1["Annual CO₂ emissions including land-use change"],
                name="émissions de co² dans le monde (milliards de tonnes)",
                line=dict(color="red"),
            ),
            secondary_y=True,
        )
        fig.update_layout(legend=dict(orientation="h", y=-0.2))
        st.plotly_chart(fig)
else:
    col1, col2 = st.columns(2)
    with col1:
        df_filter = st.selectbox(
            label="Sélectionnez un filtre : ", options=filter_options, index=world_index
        )
        if df_filter:
            df2 = df[df["Entity"] == df_filter]
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(
                go.Scatter(
                    x=df2["Year"],
                    y=df2["Temperature anomaly"],
                    name="anomalies de température (degrés)",
                ),
                secondary_y=False,
            )
            fig.add_trace(
                go.Scatter(
                    x=df2["Year"],
                    y=df2["Annual precipitation anomaly"] / 100,
                    name="anomalies de précipitations (cm)",
                ),
                secondary_y=False,
            )
            fig.add_trace(
                go.Scatter(
                    x=df1["Year"],
                    y=df1["Annual CO₂ emissions including land-use change"],
                    name="émissions de co² dans le monde (milliards de tonnes)",
                    line=dict(color="red"),
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
                ),
                secondary_y=False,
            )
            fig.add_trace(
                go.Scatter(
                    x=df2["Year"],
                    y=df2["Annual precipitation anomaly"] / 100,
                    name="anomalies de précipitations (cm)",
                ),
                secondary_y=False,
            )
            fig.add_trace(
                go.Scatter(
                    x=df1["Year"],
                    y=df1["Annual CO₂ emissions including land-use change"],
                    name="émissions de co² dans le monde (milliards de tonnes)",
                    line=dict(color="red"),
                ),
                secondary_y=True,
            )
            fig.update_layout(legend=dict(orientation="h", y=-0.2))
            st.plotly_chart(fig, key="filter22")

# Ajouter un espace entre les paragraphes
st.markdown("<br><br>", unsafe_allow_html=True)

# Load dataset
df2 = pd.read_csv("datasets/number-of-natural-disaster-events.csv")

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


# Ajouter un espace entre les paragraphes
st.markdown("<br><br>", unsafe_allow_html=True)

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
    go.Scatter(x= df_co2["Year"], y= df_co2["Annual CO₂ emissions including land-use change"], name= "émissions de co² mondiales", line=dict(color="blue")),
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


# Ajouter un espace entre les paragraphes
st.markdown("<br><br>", unsafe_allow_html=True)

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
    go.Scatter(x= df_co2["Year"], y= df_co2["Annual CO₂ emissions including land-use change"], name= "émissions de co² mondiales", line=dict(color="blue")),
    secondary_y=False,
)


fig3.add_trace(
    go.Scatter(x= df4["Year"], y= df4["Sea surface temperature anomaly (relative to 1961-90 average)"], name= "anomalies de températures", line=dict(color="red")),
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


# Ajouter un espace entre les paragraphes
st.markdown("<br><br>", unsafe_allow_html=True)

# ACIFIFICATION
st.subheader("L'acidification des océans")

# on transforme les dates en années
df5 = pd.read_csv("datasets/seawater-ph.csv")
#df5, metadata5 = load_dataset("seawater-ph")
df5["Day"] = pd.to_datetime(df5["Day"])
df5["Year"] = df5["Day"].dt.year
df5 = df5.drop_duplicates(subset = "Year", keep = "last")

df_co2 = df_co2.drop(df_co2[df_co2["Year"] < 1988].index)

# Create figure with secondary y-axis
fig4 = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
fig4.add_trace(
    go.Scatter(x= df_co2["Year"], y= df_co2["Annual CO₂ emissions including land-use change"], name= "émissions de co² mondiales", line=dict(color="blue")),
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


# Ajouter un espace entre les paragraphes
st.markdown("<br><br>", unsafe_allow_html=True)

# FONTE DES GLACES
st.subheader("La fonte des glaces")

# on transforme les dates en années
df6 = pd.read_csv("datasets/ice-sheet-mass-balance.csv")
#df6, metadata6= load_dataset("ice-sheet-mass-balance")
df6["Day"] = pd.to_datetime(df6["Day"])
df6["Year"] = df6["Day"].dt.year
df6 = df6.drop_duplicates(subset = "Year", keep = "last")

df_co2 = df_co2.drop(df_co2[df_co2["Year"] < 2002].index)

# Create figure with secondary y-axis
fig5 = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
fig5.add_trace(
    go.Scatter(x= df_co2["Year"], y= df_co2["Annual CO₂ emissions including land-use change"], name= "émissions de co² mondiales", line=dict(color="blue")),
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

