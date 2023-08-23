import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

df = pd.read_csv('data/propiedades_final.csv')# , dtype={'Código Postal': str})

def geocode_addresses(df):
    # Geocoding using address
    geolocator = Nominatim(user_agent="property_geocoder")

    def geocode_property(row):
        try:
            full_address = f"{row['Dirección Mapa']} {row['Código Postal']}"

            location = geolocator.geocode(full_address, timeout=20) # type: ignore
            if location:
                return location.latitude, location.longitude # type: ignore
            else:
                return None
        except GeocoderTimedOut:
            print(f"Geocoding timed out for address: {full_address}") # type: ignore
            return None
        except Exception as e:
            print(f"Error during geocoding for address {full_address}: {e}") # type: ignore
            return None

    # # Apply geocoding to get coordinates
    df['Coordinates'] = df.apply(geocode_property, axis=1)
    return df
