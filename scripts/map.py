import folium
import pandas as pd

def create_property_map(df):
    # Extract latitude and longitude from the first row of the 'Coordinates' column
    first_coordinates = df['Coordinates'].iloc[0]

    # Check if the coordinates are already in float format (no parentheses) and not None
    if first_coordinates is not None:
        if isinstance(first_coordinates, float):
            map_center = [float(coord) for coord in str(first_coordinates).split(',')]
        else:
            map_center = [float(coord) for coord in first_coordinates.replace('(', '').replace(')', '').split(', ')]
    else:
        # Handle the case where first_coordinates is None (no data available)
        map_center = [0, 0]  # You can set a default center here

    # Create a Folium map centered at the extracted coordinates
    m = folium.Map(location=map_center, zoom_start=12)

    # Add markers for each property's coordinates
    for index, row in df.iterrows():
        coordinates = row['Coordinates']
        latitude, longitude = map(float, coordinates.split(', '))
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
