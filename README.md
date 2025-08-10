🎯 What This Code Does
This is a Streamlit-based Weather Forecast App that:
•	Fetches real-time weather & 5-day forecast data from the OpenWeatherMap API
•	Displays the location on an interactive Folium map
•	Plots a 24-hour temperature trend using Plotly
•	Shows a stylish 5-day forecast with icons & metrics
________________________________________
🛠 Core Components Explained
1️⃣ Imports & API Setup
python
CopyEdit
import streamlit as st
import requests
from datetime import datetime
from streamlit_folium import st_folium
import folium
import plotly.graph_objects as go
•	streamlit → For creating the web app UI
•	requests → Fetch weather data from API
•	datetime → Format and manage timestamps
•	folium & streamlit_folium → Interactive maps
•	plotly → Stylish graphs for temperature trends
•	API_KEY → Your personal OpenWeatherMap access key 🔑
________________________________________
2️⃣ Fetching Weather Data
python
CopyEdit
def get_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
•	Sends a request to OpenWeatherMap for the 5-day forecast (in metric units 🌡)
•	Handles network errors gracefully using try-except
•	Returns JSON data for later processing
________________________________________
3️⃣ Displaying the Location on a Map
python
CopyEdit
def display_map(lat, lon):
    m = folium.Map(location=[lat, lon], zoom_start=10)
    folium.Marker([lat, lon], tooltip="Location").add_to(m)
•	Centers the map on the city’s coordinates
•	Adds a marker pin at the exact location 📍
•	Integrated with Streamlit via st_folium
________________________________________
4️⃣ 24-Hour Temperature Plot
python
CopyEdit
def plot_24h_forecast(data):
    times = [datetime.fromtimestamp(item["dt"]) for item in data["list"][:8]]
    temps = [item["main"]["temp"] for item in data["list"][:8]]
•	Extracts first 8 forecast entries (3-hour intervals → ~24 hours)
•	Uses Plotly line + marker chart for a polished look
•	Displays temperature trends 📈
________________________________________
5️⃣ Generating the 5-Day Forecast
python
CopyEdit
if dt_txt.endswith("12:00:00"):
    forecast[date] = {
        "temp": item["main"]["temp"],
        "desc": item["weather"][0]["description"].title(),
        "icon": item["weather"][0]["icon"]
    }
•	Picks only the midday forecast (to keep consistency)
•	Saves temperature, description, and weather icon ☀️🌧️🌩️
________________________________________
6️⃣ Streamlit UI Layout
•	st.set_page_config → Wide layout for side-by-side view
•	City input → User types city name
•	Map on left, weather details on right using:
python
CopyEdit
col1, col2 = st.columns(2)
•	Displays:
o	Map
o	Current temperature, humidity, wind speed
o	24-hour temperature graph
o	5-day forecast with icons and captions
________________________________________
🌟 UI Flow
1.	User enters city name → Clicks "Get Forecast"
2.	API fetches forecast → Saves data in st.session_state (so UI doesn’t reset on refresh)
3.	Map + Current Weather Metrics show up
4.	Interactive 24-hour Plotly chart appears
5.	5-Day forecast cards display neatly in columns
________________________________________
✨ Why This App Feels Modern
•	Interactive map instead of static location
•	Plotly charts for better visualization
•	Responsive two-column layout
•	Dynamic weather icons for a friendly UI
•	Error handling so it won’t crash on bad input


🚀 How to Run the Weather App
1️⃣ Save the File
Copy your code into a Python file.

Save it as:

bash
Copy
Edit
main.py

2️⃣ Install Required Packages
Open your terminal (Command Prompt, Anaconda Prompt, or PowerShell) and run:

bash
Copy
Edit
pip install streamlit requests folium streamlit-folium plotly
3️⃣ Run the App
Navigate to your project folder in terminal:


bash
Copy
Edit

streamlit run main.py

4️⃣ Open in Browser
After running, Streamlit will show a link like:

nginx
Copy
Edit
Local URL: http://localhost:8501
🔗 Click the link or copy-paste it into your browser.

5️⃣ Use the App
Type a city name in the input box

Click Get Forecast


View the map, current weather, 24-hour temperature graph, and 5-day forecast.

<img width="1783" height="638" alt="image" src="https://github.com/user-attachments/assets/63d50c27-0ab7-4ca0-bf08-172712ba7598" />
<img width="1823" height="879" alt="image" src="https://github.com/user-attachments/assets/d8c803d7-2175-459c-b6b1-26e119ef6ce7" />
<img width="1642" height="545" alt="image" src="https://github.com/user-attachments/assets/37aa8a37-a5f3-4bd3-a335-2ab6b6c9408c" />


