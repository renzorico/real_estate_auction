import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd

# Read the DataFrame with geocoded coordinates
df = pd.read_csv('data/propiedades_geocoded.csv')

# Display the DataFrame
st.write('## Properties Data')
st.dataframe(df)

# Calculate the center based on median latitude and longitude
def get_latitude(coord):
    if isinstance(coord, str):
        return float(coord.split(',')[0])
    else:
        return coord

def get_longitude(coord):
    if isinstance(coord, str):
        return float(coord.split(',')[1])
    else:
        return coord

median_latitude = df['Coordinates'].apply(get_latitude).median()
median_longitude = df['Coordinates'].apply(get_longitude).median()

# Display the map
st.write('## Property Map')
m = folium.Map(location=[median_latitude, median_longitude], zoom_start=12)
for index, row in df.iterrows():
    coordinates = row['Coordinates']
    if isinstance(coordinates, str):
        latitude, longitude = map(float, coordinates.split(', '))
        folium.Marker([latitude, longitude], popup=row['Dirección Mapa']).add_to(m)
folium_static(m)
