import streamlit as st
import requests
from datetime import datetime
import pytz
from bs4 import BeautifulSoup
import re
import pandas as pd
from helium import *

months= {"Jan": "janvier",
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
    "Dec": "décembre"}

st.header("Données climatique du moment")
city = st.text_input("Choisissez une ville","nantes")
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Températures")
    if city:
        link = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={st.secrets["open_weather_data_api_key"]}"
        coor = requests.get(link).json()
        lon = coor[0]["lon"]
        lat = coor[0]["lat"]
        urlnow = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={st.secrets["open_weather_data_api_key"]}"
        r = requests.get(urlnow).json()

        dt = r["dt"]
        utctime = datetime.utcfromtimestamp(dt)
        timezone = pytz.timezone("Europe/Paris")
        now = pytz.utc.localize(utctime).astimezone(timezone)

        rn = now
        moois = months[rn.strftime("%b")]
        rn = f"{rn.day} {moois} {rn.year} {rn.hour}:{rn.minute}:{rn.second}"

        C = int(round((r["main"]["temp"] - 273.15)))
        nom = r["name"]
        st.write(f'{rn} | {nom}: {C}°C')

        Clist = []
        nowlist = []
        for year in range(4):
            now = now.replace(year=now.year - 10)
            naw = now.strftime("%Y-%m-%d %H:%M:%S")
            naw = datetime.strptime(naw, "%Y-%m-%d %H:%M:%S")
            unix = int(naw.timestamp())
            urldecade = f"https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={lat}&lon={lon}&dt={unix}&appid={st.secrets["open_weather_data_api_key"]}"
            r2 = requests.get(urldecade).json()

            if r2.get("data"):
                dt2 = r2["data"][0]["dt"]
                utctime2 = datetime.utcfromtimestamp(dt2)
                timezone2 = pytz.timezone("Europe/Paris")
                dt2 = pytz.utc.localize(utctime2).astimezone(timezone2)
                mooois = months[dt2.strftime("%b")]
                dt2 = f"{dt2.day} {mooois} {dt2.year} {dt2.hour}:{dt2.minute}:{dt2.second}"
            else:
                dt2 = "Pas de Données"

            nowlist.append(dt2)
            if r2.get("data"):
                C2 = int(round((r2["data"][0]["temp"] - 273.15)))
            else:
                C2 = "Pas de Données"

            if isinstance(C2, int):
                Clist.append(f"{C2}°C")
            else:
                Clist.append(C2)

        st.write(pd.DataFrame({"Date": nowlist, "Temperature": Clist}))

with col2:
    st.markdown("#### Concentration en CO2")
    url = start_firefox("https://www.co2.earth/daily-co2", headless=True)
    click("6 Decades")
    page_source = url.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    tab = soup.find("div", {"id": "DecadeDailyPanel"})
    kill_browser()

    date = re.search(r"<td><span>(.*)</span> </td>", str(tab)).group(1)
    date = datetime.strptime(date, "%b. %d, %Y")
    mois = months[date.strftime("%b")]
    date = f"{date.day} {mois} {date.year}"
    ppm = re.search(r'<td class="alt-col"><span>(.*)</span></td>', str(tab)).group(1)
    tabledate = re.findall(r"<td>(\w{3}\.\s\d+\,\s\d+)</td>", str(tab))
    tableppm = re.findall(r'<td class="alt-col">(\d{3}\..+|Unavailable)</td>', str(tab))
    change = re.findall(r"<td><span class=.*>(.*) </span></td>", str(tab))
    change = change[1:]

    def fr(txt):
        if txt == "n/a":
            return "Pas de Données"
        else:
            return re.sub(r"([\d.]+ ppm) increase (\([\d.]+ %\)) *", r"Augmentation de \1 \2", txt)
    change = [fr(txt) for txt in change]

    def fr2(txt):
        if txt == "Unavailable":
            return "Pas de Données"
        else:
            return txt
    tableppm = [fr2(txt) for txt in tableppm]
    ppm = "Pas de Données" if ppm == "Unavailable" else ppm

    def dateuh(dat3):
        dat3 = datetime.strptime(dat3, "%b. %d, %Y")
        m0is = months[dat3.strftime("%b")]
        dat3 = f"{dat3.day} {m0is} {dat3.year}"
        return dat3
    tabledate = [dateuh(dat3) for dat3 in tabledate]

    st.write(f"{date} | {ppm}")
    st.write(pd.DataFrame({"Date": tabledate, "PPM": tableppm, "augmentation": change}))
