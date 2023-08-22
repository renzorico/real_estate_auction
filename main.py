import requests
import pandas as pd
from bs4 import BeautifulSoup
from utils.scraper import fetch_property_data, fetch_property_bienes_data
from utils.processor import preprocess_data
from utils.database import save_to_excel, save_to_csv
from utils.map import generate_property_map

def main():
    # (Just for testing purposes)
    # property_ids_url = 'https://subastas.boe.es/reg/subastas_ava.php?accion=Mas&id_busqueda=_ZURMUzR4WmN2Uk1VS1dkeEo1ZmFId0ppTUxjVVVQclNub3BnckVtQzdxeDJEY2Z6V2dOWVJRT0pqTlFlS01YVUUzZFdISmJpeTBEQVN1TVpnSGpodzNTYkhxNWo3ejY4eGNQVGZ1dHhCQ1hXM0lFZG1tMEhETGtBSE13ZGtiREZOSUh1d3RXMWFIZkVqNCtGbUhtWm1nd0Q4QWNYYkJrZHpqdzVDVFNOY094MFZkdkF5U2kvSXQ4Z0N4STBZakNwV0hnUnByWG5mMXRTZStidnc3YlByaEMvZXFSVkdDZXlJazF0eDlTK0hETTdMT0h4S3p6NEJJd21hdHEreXpZZVhyclFsdFI4RTRNVlBJbGlGbThicTNpT1NTWGVaNVRvRlpnMGN3Ky8xeHJHQmJDaGxBR0g3Um12V2FsbEJaZnM,-0-50'

    # (Complete dataset)
    property_ids_url = 'https://subastas.boe.es/reg/subastas_ava.php?accion=Mas&id_busqueda=_Y0wyY1ppR3hqa2xCZjhyNDREcndPME1hRHdnbXJaWkV4ME9mbW5XN0RIekkyMkpHdGErVHNZYURoUjViSlJua0JMQzltMS9nVXNUMjlFa1VBbG4yT2hoSGNEUGw5WjhoaGZtQzQrSHJGVTFqS2RUODJkL0RaMUxGSEpwemhPeU5DL1o3aW1NYmVpVG93S3d6UHAzWXNXS0c3VWlsQTBuRU9zL0FjQW1jSGRnamEzTFU2aERSUzVFZDBmS0NLNjljeTZOanZNWWxjNEVoZHZhc2pwU2hKZUJGTEg1T3ViREVLTGhlRXp4MjZXZHhjWkN2YmcxQ0NXNHNxNExJVmYrSGFaSDdoRU0xL0Q2OE9VR1R2c2ZSOEE9PQ,,-0-500'


    # Fetch the HTML content
    response = requests.get(property_ids_url)
    html_content = response.text
    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Extract property IDs from the <a> elements with class 'resultado-busqueda-link-otro'
    properties_list = [a['title'] for a in soup.find_all('a', class_='resultado-busqueda-link-otro')]

    # Fetch property data
    property_data_df = fetch_property_data(properties_list)

    # Fetch bienes data
    bienes_data_df = fetch_property_bienes_data(properties_list)

    # Merge property and bienes data
    main_df = property_data_df.merge(bienes_data_df, on='Identificador', how='inner')
    save_to_excel(main_df, 'data/propiedades_raw.xlsx')

    # Data preprocessing and cleaning
    main_df = preprocess_data(main_df)
    # Save the final DataFrame to Excel
    save_to_excel(main_df, 'data/propiedades_final.xlsx')
    save_to_csv(main_df, 'data/propiedades_final.csv')

    # map_df = pd.read_csv('propiedades_final.csv', dtype={'Código Postal': str})

if __name__ == "__main__":
    main()
