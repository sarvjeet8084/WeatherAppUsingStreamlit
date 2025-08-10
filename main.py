import streamlit as st
import requests
from datetime import datetime
from streamlit_folium import st_folium
import folium
import plotly.graph_objects as go

# --- CONFIG ---
API_KEY = "326864ea00fd86b2bb96c062eb4202e7"  # Replace with your valid key

# --- WEATHER FUNCTIONS ---
def get_weather_data(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
        res = requests.get(url, timeout=5)
        res.raise_for_status()
        return res.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Network/API error: {e}")
        return None

def display_map(lat, lon):
    m = folium.Map(location=[lat, lon], zoom_start=10)
    folium.Marker([lat, lon], tooltip="Location").add_to(m)
    return m

def plot_24h_forecast(data):
    times = [datetime.fromtimestamp(item["dt"]) for item in data.get("list", [])[:8]]
    temps = [item["main"]["temp"] for item in data.get("list", [])[:8]]
    
    fig = go.Figure()
    if times and temps:
        fig.add_trace(go.Scatter(x=times, y=temps, mode="lines+markers", name="Temp (°C)"))
        fig.update_layout(title="Next 24h Forecast", xaxis_title="Time", yaxis_title="Temp (°C)")
    else:
        st.warning("Not enough forecast data to plot.")
    return fig

def get_5_day_forecast(data):
    forecast = {}
    for item in data.get("list", []):
        dt_txt = item.get("dt_txt", "")
        date = dt_txt.split()[0] if dt_txt else ""
        if dt_txt.endswith("12:00:00"):
            if date not in forecast:
                forecast[date] = {
                    "temp": item["main"]["temp"],
                    "desc": item["weather"][0]["description"].title(),
                    "icon": item["weather"][0]["icon"]
                }
    return forecast

# --- STREAMLIT UI ---
st.set_page_config(page_title="Weather Forecast App", layout="wide")
st.title("🌦️ Weather Forecast App with Map")

# Store data in session_state to persist after reruns
if "data" not in st.session_state:
    st.session_state.data = None

city = st.text_input("Enter City Name", "").strip()

if st.button("Get Forecast"):
    if not city:
        st.warning("Please enter a valid city name.")
    else:
        st.session_state.data = get_weather_data(city)

# Display results if data exists
if st.session_state.data:
    data = st.session_state.data
    col1, col2 = st.columns(2)
    lat = data.get("city", {}).get("coord", {}).get("lat")
    lon = data.get("city", {}).get("coord", {}).get("lon")

    if lat is not None and lon is not None:
        with col1:
            st_folium(display_map(lat, lon), width=600, height=400)

    if "list" in data and data["list"]:
        with col2:
            current = data["list"][0]
            st.metric("Temperature", f"{current['main']['temp']} °C")
            st.metric("Humidity", f"{current['main']['humidity']} %")
            st.metric("Wind Speed", f"{current['wind']['speed']} m/s")

        st.plotly_chart(plot_24h_forecast(data), use_container_width=True)

        st.subheader("🌤️ 5-Day Forecast")
        forecast = get_5_day_forecast(data)
        if forecast:
            cols = st.columns(len(forecast))
            for i, (date, f) in enumerate(forecast.items()):
                with cols[i]:
                    st.markdown(f"**{datetime.strptime(date, '%Y-%m-%d').strftime('%a %d %b')}**")
                    st.image(f"http://openweathermap.org/img/wn/{f['icon']}@2x.png")
                    st.metric(label="Temp (°C)", value=f"{f['temp']:.1f}")
                    st.caption(f["desc"])
        else:
            st.info("Forecast data not available.")
    else:
        st.error("Forecast list is empty.")
