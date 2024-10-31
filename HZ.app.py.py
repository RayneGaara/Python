
import streamlit as st
import pandas as pd
import folium
from folium import plugins
from geopy.geocoders import Nominatim
from streamlit_folium import folium_static




# Пример данных о полетах
flights_AIRPORT = pd.DataFrame({
    'ORIGIN_AIRPORT': ['JFK', 'LAX', 'SFO'],
    'DESTINATION_AIRPORT': ['LAX', 'JFK', 'ORD']
})

# Инициализация геолокатора
geolocator = Nominatim(user_agent="geoapiExercises")

# Получаю координаты аэропортов
def get_coordinates(airport_code):
    try:
        location = geolocator.geocode(f"{airport_code} Airport")
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except Exception:
        return None, None

# Получаю координаты для вылета и назначения
flights_AIRPORT[['DEPARTURE_LAT', 'DEPARTURE_LON']] = flights_AIRPORT['ORIGIN_AIRPORT'].apply(get_coordinates).apply(pd.Series)
flights_AIRPORT[['DESTINATION_LAT', 'DESTINATION_LON']] = flights_AIRPORT['DESTINATION_AIRPORT'].apply(get_coordinates).apply(pd.Series)

# Создаю карту
m = folium.Map(location=[20, 0], zoom_start=2)

# Добавляю полеты на карту
for index, row in flights_AIRPORT.iterrows():
    departure_lat = row['DEPARTURE_LAT']
    departure_lon = row['DEPARTURE_LON']
    destination_lat = row['DESTINATION_LAT']
    destination_lon = row['DESTINATION_LON']

    if (
        departure_lat is not None and 
        departure_lon is not None and 
        destination_lat is not None and 
        destination_lon is not None
    ):
        # Добавляю линии между аэропортами
        folium.PolyLine(
            locations=[[departure_lat, departure_lon],
                       [destination_lat, destination_lon]],
            color='blue',
            weight=2.5,
            opacity=1
        ).add_to(m)

        # Добавляю маркеры для аэропортов
        folium.Marker(
            location=[departure_lat, departure_lon],
            popup=row['ORIGIN_AIRPORT'],
            icon=folium.Icon(color='green')
        ).add_to(m)

        folium.Marker(
            location=[destination_lat, destination_lon],
            popup=row['DESTINATION_AIRPORT'],
            icon=folium.Icon(color='red')
        ).add_to(m)

# Отображение карты в Streamlit
st.title('Полеты на карте')
folium_static(m)
