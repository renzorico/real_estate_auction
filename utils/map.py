import pandas as pd
import folium
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

def generate_property_map(map_df):
    # Geocoding using postal code and address
    geolocator = Nominatim(user_agent="property_geocoder")

    def geocode_property(row):
        try:
            address_parts = []

            if not pd.isnull(row['Dirección Mapa']):
                address_parts.append(row['Dirección Mapa'])

            if not pd.isnull(row['Código Postal']):
                address_parts.append(str(row['Código Postal']))

            if not pd.isnull(row['Localidad']):
                address_parts.append(row['Localidad'])

            if not pd.isnull(row['Provincia']):
                address_parts.append(row['Provincia'])

            full_address = ', '.join(address_parts)
            print(f"Geocoding address: {full_address}")

            location = geolocator.geocode(full_address, timeout=20)  # type: ignore
            if location:
                return location.latitude, location.longitude # type: ignore
            else:
                return None
        except GeocoderTimedOut:
            print(f"Geocoding timed out for address: {full_address}")
            return None
        except Exception as e:
            print(f"Error during geocoding for address {full_address}: {e}")
            return None

    # Apply geocoding to get coordinates and drop rows with invalid locations
    map_df['Coordinates'] = map_df.apply(geocode_property, axis=1)
    map_df = map_df.dropna(subset=['Coordinates'])

    # Create a Folium map centered in Spain
    map_center = [40.4168, -3.7038]  # Coordinates for the center of Spain
    property_map = folium.Map(location=map_center, zoom_start=6)

    # Add markers for each property with identifiers as popups
    located_count = 0  # Counter for located properties
    for _, row in map_df.iterrows():
        folium.Marker(
            location=row['Coordinates'],
            popup=row['Identificador'],
        ).add_to(property_map)
        located_count += 1

    # Print the number of located properties
    print(f"Number of located properties: {located_count}")

    # Save the map as an HTML file
    property_map.save('data/properties_map.html')
