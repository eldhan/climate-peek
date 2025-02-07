import streamlit as st
from functions import check_datasets


def load_css(file_name: str) -> None:
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


climate_change = st.Page(
    page="climate_change.py",
    title="Climate Peek",
    url_path="climate-change",
    default=False,
)

change_evidence = st.Page(
    page="change_evidence.py",
    title="Indicateurs du changement",
    url_path="change-evidence",
    default=False,
)

change_impact = st.Page(
    page="change_impact.py",
    title="Impact du changement",
    url_path="change-impact",
    default=False,
)

today = st.Page(
    page="today.py",
    title="Et aujourd'hui ?",
    url_path="today",
    default=False,
)

# Define the navigation
st.set_page_config(layout="wide")
with st.sidebar:
    pg = st.navigation([climate_change, change_evidence, change_impact, today])
# Apply css
css = "assets/style.css"
load_css(css)
# List of datasets
DATASETS = [
    "annual-co2-including-land-use",
    "annual-temperature-anomalies",
    "global-precipitation-anomaly",
    "number-of-natural-disaster-events",
]
check_datasets(DATASETS)
# Start the app
pg.run()
