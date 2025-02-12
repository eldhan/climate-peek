import streamlit as st
import requests
from datetime import datetime
import pytz
from bs4 import BeautifulSoup
import re
import pandas as pd
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


def dateuh(dat3):
    dat3 = datetime.strptime(dat3, "%b. %d, %Y")
    m0is = months[dat3.strftime("%b")]
    dat3 = f"{dat3.day} {m0is} {dat3.year}"
    return dat3


# Initialize session states
if "data_retrieved" not in st.session_state:
    st.session_state.data_retrieved = False
    st.session_state.date = False
    st.session_state.date = False
    st.session_state.change = False
    st.session_state.tableppm = False
    st.session_state.ppm = False
    st.session_state.tabledate = False

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

with col2:
    st.markdown("#### Concentration en CO2")
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
        st.session_state.tabledate = [dateuh(dat3) for dat3 in tabledate]
        st.session_state.data_retrieved = True

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
