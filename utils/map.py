import folium
import pandas as pd

def create_property_map(df):
    # Extract latitude and longitude from the first row of the 'Coordinates' column
    first_coordinates = df['Coordinates'].iloc[0]

    # Check if the coordinates are already in float format (no parentheses)
    if isinstance(first_coordinates, float):
        map_center = [first_coordinates, df['Coordinates'].iloc[1]]
    else:
        map_center = [float(coord) for coord in first_coordinates.replace('(', '').replace(')', '').split(', ')]

    # Create a Folium map centered at the extracted coordinates
    m = folium.Map(location=map_center, zoom_start=12)

    # Add markers for each property's coordinates
    for index, row in df.iterrows():
        coordinates = row['Coordinates']
        if isinstance(coordinates, str):
            latitude, longitude = map(float, coordinates.replace('(', '').replace(')', '').split(', '))
            folium.Marker([latitude, longitude], popup=row['Dirección Mapa']).add_to(m)

    return m

def main():
    # Read the main_df DataFrame
    main_df = pd.read_csv('data/propiedades_geocoded.csv')

    # Create the property map
    property_map = create_property_map(main_df)

    # Save the map to an HTML file
    property_map.save('data/final_map.html')

if __name__ == "__main__":
    main()
