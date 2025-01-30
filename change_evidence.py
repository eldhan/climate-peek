import streamlit as st
import plotly.express as px
from functions import load_dataset


# Load datasets required for graph comparisons
df1, metadata1 = load_dataset("annual-temperature-anomalies")
df2, metadata2 = load_dataset("global-precipitation-anomaly")

st.header("Mise en évidence du changement climatique ")
df_filter = st.selectbox(
    label="Sélectionnez un filtre : ", options=df1["Entity"].drop_duplicates()
)
col1, col2 = st.columns(2)
with col1:
    st.subheader("Anomalies de température dans l'atmosphère")
    if df_filter:
        fig1 = px.line(
            df1[df1["Entity"] == df_filter],
            x="Year",
            y="temperature_anomaly",
            hover_name="Entity",
        )
        st.plotly_chart(fig1)

with col2:
    st.subheader("Anomalies précipitations")
    if df_filter:
        fig2 = px.line(
            df2[df2["Entity"] == df_filter],
            x="Year",
            y="precipitation_anomaly",
            hover_name="Entity",
        )
        st.plotly_chart(fig2)
