import pandas as pd
from geopy.geocoders import GoogleV3
from geopy.exc import GeocoderTimedOut
from utils.database import save_to_csv
from dotenv import load_dotenv
import os

# Read the DataFrame
# df = pd.read_csv('data/propiedades_final.csv')
load_dotenv()

def geocode_addresses(df):
    # Geocoding using Google Maps Geocoding API
    geolocator = GoogleV3(api_key=os.environ['GOOGLE_MAPS_API_KEY'])

    def geocode_property(row):
        try:
            full_address = f"{row['Código Postal']} {row['Dirección Mapa']}"
            location = geolocator.geocode(full_address, timeout=20)

            if location:
                return f"{location.latitude}, {location.longitude}"
            else:
                return None
        except GeocoderTimedOut:
            print(f"Geocoding timed out for address: {full_address}")
            return None
        except Exception as e:
            print(f"Error during geocoding for address {full_address}: {e}")
            return None


    # Apply geocoding to get coordinates
    df['Coordinates'] = df.apply(geocode_property, axis=1)

    save_to_csv(df, 'data/propiedades_geocoded.csv')
    return df


# # Call the function to geocode addresses
# geocoded_df = geocode_addresses(df)
