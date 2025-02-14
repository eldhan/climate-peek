import streamlit as st
import requests
from datetime import datetime
import pytz
import re
import pandas as pd


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

st.header("Données climatique du moment")
city = st.text_input("Choisissez une ville")
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Températures")
    if city:
        # Get city coordinates
        coordinates_endpoint = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={st.secrets["open_weather_data_api_key"]}"
        coord = requests.get(coordinates_endpoint).json()
        lon = coord[0]["lon"]
        lat = coord[0]["lat"]

        # Get current weather for the city
        current_weather_endpoint = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={st.secrets["open_weather_data_api_key"]}"
        r = requests.get(current_weather_endpoint).json()

        # Get current date and time of the city localized for Europe/Paris
        date = r["dt"]
        utctime = datetime.utcfromtimestamp(date)
        timezone = pytz.timezone("Europe/Paris")
        current_datetime = pytz.utc.localize(utctime).astimezone(timezone)

        # Format the date and time for a nicer display
        month = months[current_datetime.strftime("%b")]
        formatted_datetime = f"{current_datetime.day} {month} {current_datetime.year} {current_datetime.hour}:{current_datetime.minute}:{current_datetime.second}"

        # Convert temperature to celsius degrees
        celsius_degree = int(round((r["main"]["temp"] - 273.15)))
        city_name = r["name"]
        st.write(f"{formatted_datetime} | {city_name}: {celsius_degree}°C")

        temperatures = []
        dates = []
        start_year = current_datetime.year
        # Fetch and display dates and temperature for the 4 previous decades
        for decade in range(10, 50, 10):
            decade_datetime = current_datetime.replace(year=start_year - decade)
            formatted_decade_datetime = decade_datetime.strftime("%Y-%m-%d %H:%M:%S")
            formatted_decade_datetime = datetime.strptime(
                formatted_decade_datetime, "%Y-%m-%d %H:%M:%S"
            )
            formatted_decade_datetime = int(
                formatted_decade_datetime.timestamp()
            )  # format the date to Unix

            # Get data from the API
            timemachine_endpoint = f"https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={lat}&lon={lon}&dt={formatted_decade_datetime}&appid={st.secrets["open_weather_data_api_key"]}"
            r2 = requests.get(timemachine_endpoint).json()

            if r2.get("data"):
                date2 = r2["data"][0]["dt"]
                utctime2 = datetime.utcfromtimestamp(date2)
                timezone2 = pytz.timezone("Europe/Paris")
                date2 = pytz.utc.localize(utctime2).astimezone(timezone2)
                month2 = months[date2.strftime("%b")]
                date2 = f"{date2.day} {month2} {date2.year} {date2.hour}:{date2.minute}:{date2.second}"
            else:
                date2 = "Pas de données"

            dates.append(date2)
            if r2.get("data"):
                celsius_degree2 = int(round((r2["data"][0]["temp"] - 273.15)))
            else:
                celsius_degree2 = "Pas de données"

            if isinstance(celsius_degree2, int):
                temperatures.append(f"{celsius_degree2}°C")
            else:
                temperatures.append(celsius_degree2)

        st.write(pd.DataFrame({"Date": dates, "Temperature": temperatures}))
    else:
        st.write("Veuillez sélectionner une ville.")

with col2:
    st.markdown("#### Concentration en CO2")
    if st.session_state.data_retrieved == True:
        st.write(f"{st.session_state.date} | {st.session_state.ppm}")
        st.write(
            pd.DataFrame(
                {
                    "Date": st.session_state.tabledate,
                    "PPM": st.session_state.tableppm,
                    "augmentation": st.session_state.change,
                }
            )
        )
    else: 
        st.write("Erreur")

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("#### Les prédictions jusqu'en 2100")
col3, col4 = st.columns(2)
with col3:
    st.image("assets/ab.png")
with col4:
    st.image("assets/cd.png")

st.write("Source: https://www.ipcc.ch/report/ar6/wg1/figures/summary-for-policymakers/figure-spm-8")