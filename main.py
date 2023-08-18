import pandas as pd
from scripts.web_scraping import fetch_property_ids
from scripts.property_data_processing import fetch_property_bienes_data, preprocess_bienes_data
from scripts.data_preprocessing import preprocess_data
from scripts.geocoding import geocode_dataframe

# Fetch property IDs
properties_list = fetch_property_ids()

# Create a DataFrame
df = pd.DataFrame(properties_list, columns=['Identificador'])

# Fetch property bienes data
bienes_data = fetch_property_bienes_data(properties_list)

# Create a DataFrame for bienes data
bienes_df = pd.DataFrame(bienes_data)

# Preprocess property bienes data
preprocessed_bienes_df = preprocess_bienes_data(bienes_df)

# Merge the main DataFrame with bienes data
main_df = df.merge(preprocessed_bienes_df, on='Identificador', how='inner')

# Preprocess data
df = preprocess_data(main_df)

# Geocode addresses
geocode_dataframe(df)
