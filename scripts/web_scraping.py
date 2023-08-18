import requests
from bs4 import BeautifulSoup
import pandas as pd
from config.constants import PROPERTY_IDS_URL, PROPERTY_BIENES_URL, PROPERTY_PRUEBA, BIENES_PRUEBA

def fetch_property_ids():
    response = requests.get(PROPERTY_IDS_URL)
    soup = BeautifulSoup(response.text, "html.parser")
    properties_list = [a['title'] for a in soup.find_all('a', class_='resultado-busqueda-link-otro')]
    return properties_list

def fetch_property_bienes_data(property_id):
    url = f"https://subastas.boe.es/reg/detalleSubasta.php?idSub={property_id}&ver=3&idBus=_aGZaODZVK09aRlgzcFpxSzQ4SWlXa3ZOSDdnaFNaMkg1OWV0U2pHWjFwUEc2aHo5TVl3QjNtUnJUQ1FGS2ZoYmdoYS94cncxU1ZhYjNYMXFndzdyaVNvUlZpSUJHdm83eEVla3UyMElJYjJFcHpGdFB4N0RWQ20xRThPNFFrUStieGtWOWhaTlJuNGtqUXlyV3V3dFdYbWFPd3BGMnh3dlZaK2tXaElFQjVvZmhiUkdFMTJJYTYrUnRsMkU0enNHektmOUZRdnpYQmZHcERYRlY2bUdDVHE1UFZaLzJRS1BDMFlPNVhCb2R1SEYrOGljOW85djdqdE1zeWZySnNZQS8wTkhSS1lvWkxVMGJ5enJkWUhLdEhmYy9JY3g0YlF3YnpZdWo1aVhlOGs9-0-50&idLote=&numPagBus="

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    div_id_bloque_datos3 = soup.find('div', id='idBloqueDatos3')
    if div_id_bloque_datos3:
        data_divs = div_id_bloque_datos3.find_all('div', class_='bloque')
        data_list = []

        for data_div in data_divs:
            property_data = {'Property ID': property_id}

            property_table = data_div.find('table')
            if property_table:
                rows = property_table.find_all('tr')
                for row in rows:
                    th = row.find('th')
                    td = row.find('td')
                    if th and td:
                        property_data[th.get_text(strip=True)] = td.get_text(strip=True)

            data_list.append(property_data)

        return data_list
    else:
        return []
