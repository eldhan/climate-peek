import streamlit as st


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
    title="Causes du changement",
    url_path="change-evidence",
    default=False,
)

change_impact_terre = st.Page(
    page="change_impact_terre.py",
    title="Impacts terrestres",
    url_path="change-impact_terre",
    default=False,
)

change_impact_ocean = st.Page(
    page="change_impact_ocean.py",
    title="Impacts océaniques",
    url_path="change-impact_ocean",
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
    st.image("assets/climate_peek.webp")
    pg = st.navigation(
        [
            climate_change,
            change_evidence,
            change_impact_terre,
            change_impact_ocean,
            today,
        ]
    )
# Apply css
css = "assets/style.css"
load_css(css)
# Start the app
pg.run()
