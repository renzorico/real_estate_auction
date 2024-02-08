import requests
import pandas as pd
from bs4 import BeautifulSoup
from scripts.scraper import fetch_property_data, fetch_property_bienes_data
from scripts.new_processor import preprocess_data
from scripts.geocoding import geocode_addresses
from scripts.map import create_property_map
from utils.url_generator import generate_property_urls
from config import BASE_URL, START_RANGE, END_RANGE, STEP


def main():
    response = requests.get(BASE_URL.format(START_RANGE, 0))
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")

    END_RANGE = fetch_result_number(soup)
    property_data_list = [
        fetch_data(soup)
        for _ in generate_property_urls(BASE_URL, START_RANGE, END_RANGE, STEP)
    ]
    main_df = preprocess_data(main_df)

    main_df = geocode_addresses(main_df)

    property_map = create_property_map(main_df)
    property_map.save("data/property_map.html")

    return main_df


def fetch_result_number(soup):
    result_p_tag = soup.find("div", class_="paginar").find("p")
    result_text = result_p_tag.get_text(strip=True)
    result_number = int(result_text.split()[-1])

    return result_number


def fetch_data(soup):
    response = requests.get(
        generate_property_urls(BASE_URL, START_RANGE, END_RANGE, STEP)
    )
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")

    properties_list = [
        a["title"] for a in soup.find_all("a", class_="resultado-busqueda-link-otro")
    ]

    # property_data_df = fetch_property_data(properties_list)
    # bienes_data_df = fetch_property_bienes_data(properties_list)
    # bienes_data_df.drop(columns="Cantidad reclamada", inplace=True)

    # # Merge property and bienes data
    # main_df = property_data_df.merge(bienes_data_df, on="Identificador", how="inner")

    # return main_df
    return properties_list


if __name__ == "__main__":
    main()
