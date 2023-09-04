import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd

# Read the DataFrame with geocoded coordinates
df = pd.read_csv('data/propiedades_geocoded.csv')

# Select only the desired columns
columns_to_keep = ['Identificador', 'Tipo de subasta', 'Fecha de inicio', 'Fecha de conclusión','Cantidad reclamada', 'Valor subasta', 'Tasación', 'Tramos entre pujas',
'Importe del depósito', 'Localidad','Provincia','Dirección Mapa', 'Coordinates']
df = df[columns_to_keep]

# Get unique values for 'Tipo de subasta' and 'Provincia'
auction_types = df['Tipo de subasta'].unique()
provinces = df['Provincia'].unique()

# Create Streamlit app interface
st.sidebar.header('Filtros')

# Filter options in the sidebar
selected_auction_type = st.sidebar.selectbox('Seleccionar tipo de subasta', ['TODOS'] + list(auction_types))
selected_province = st.sidebar.selectbox('Seleccionar provincia', ['TODOS'] + list(provinces))
apply_filters = st.sidebar.button('Confirmar', key="apply_button")

# Apply the filters to the DataFrame
if apply_filters:
    if selected_auction_type == 'TODOS' and selected_province == 'TODOS':
        filtered_df = df
    elif selected_auction_type == 'TODOS':
        filtered_df = df[df['Provincia'] == selected_province]
    elif selected_province == 'TODOS':
        filtered_df = df[df['Tipo de subasta'] == selected_auction_type]
    else:
        filtered_df = df[(df['Tipo de subasta'] == selected_auction_type) & (df['Provincia'] == selected_province)]
else:
    filtered_df = df

# Display the DataFrame with applied filters
st.write('## Propiedades disponibles')
st.dataframe(filtered_df)

# Calculate the center based on median latitude and longitude of filtered data
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

if not filtered_df.empty:
    median_latitude = filtered_df['Coordinates'].apply(get_latitude).median()
    median_longitude = filtered_df['Coordinates'].apply(get_longitude).median()

    # Display the map
    st.write('## Mapa propiedades disponibles')
    m = folium.Map(location=[median_latitude, median_longitude], zoom_start=12, min_zoom=3, max_zoom=15)
    for index, row in filtered_df.iterrows():
        coordinates = row['Coordinates']
        if isinstance(coordinates, str):
            latitude, longitude = map(float, coordinates.split(', '))
            folium.Marker([latitude, longitude], popup=row['Identificador']).add_to(m)
    folium_static(m)
else:
    st.write("No hay propiedades disponibles para esta selección.")
