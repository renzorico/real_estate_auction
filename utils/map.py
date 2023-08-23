import folium
import pandas as pd

def create_property_map(df):
    # Initialize the map centered at the first property's coordinates
    map_center = df['Coordinates'].iloc[0]
    m = folium.Map(location=map_center, zoom_start=12)

    # Add markers for each property
    for index, property_data in df.iterrows():
        if property_data['Coordinates']:
            coords = property_data['Coordinates']
            folium.Marker(coords, popup=property_data['Dirección']).add_to(m)

    return m

def main():
    # Read the main_df DataFrame
    main_df = pd.read_csv('data/propiedades_final_geocoded.csv')

    # Create the property map
    property_map = create_property_map(main_df)

    # Save the map to an HTML file
    property_map.save('property_map.html')

if __name__ == "__main__":
    main()
