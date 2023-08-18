import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def fetch_property_data(properties_list):
    data_list = []

    for property_id_full in properties_list:
        property_id = property_id_full.split(" ")[1]

        property_url = f"https://subastas.boe.es/detalleSubasta.php?idSub={property_id}"

        response = requests.get(property_url)
        soup = BeautifulSoup(response.text, "html.parser")

        table_div = soup.find("div", id="idBloqueDatos1")
        if table_div:
            table = table_div.find("table")
            rows = table.find_all("tr")

            property_data = {}
            for row in rows:
                cols = row.find_all(["th", "td"])
                header = cols[0].get_text(strip=True)
                value = cols[1].get_text(strip=True) if len(cols) > 1 else ""
                property_data[header] = value

            data_list.append(property_data)

    df = pd.DataFrame(data_list)
    return df

def fetch_property_bienes_data(properties_list):
    data_list = []

    for property_info in properties_list:
        if property_info.startswith('Subasta SUB-'):
            property_id = property_info.split(' ')[-1]

            url = f'https://subastas.boe.es/reg/detalleSubasta.php?idSub={property_id}&ver=3&idBus=_aGZaODZVK09aRlgzcFpxSzQ4SWlXa3ZOSDdnaFNaMkg1OWV0U2pHWjFwUEc2aHo5TVl3QjNtUnJUQ1FGS2ZoYmdoYS94cncxU1ZhYjNYMXFndzdyaVNvUlZpSUJHdm83eEVla3UyMElJYjJFcHpGdFB4N0RWQ20xRThPNFFrUStieGtWOWhaTlJuNGtqUXlyV3V3dFdYbWFPd3BGMnh3dlZaK2tXaElFQjVvZmhiUkdFMTJJYTYrUnRsMkU0enNHektmOUZRdnpYQmZHcERYRlY2bUdDVHE1UFZaLzJRS1BDMFlPNVhCb2R1SEYrOGljOW85djdqdE1zeWZySnNZQS8wTkhSS1lvWkxVMGJ5enJkWUhLdEhmYc9--50&idLote=&numPagBus='

            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            div_id_bloque_datos3 = soup.find('div', id='idBloqueDatos3')
            if div_id_bloque_datos3:
                data_divs = div_id_bloque_datos3.find_all('div', class_='bloque')
                for data_div in data_divs:
                    property_data = {'Descripción': property_info, 'Property ID': property_id}

                    property_table = data_div.find('table')
                    if property_table:
                        rows = property_table.find_all('tr')
                        for row in rows:
                            th = row.find('th')
                            td = row.find('td')
                            if th and td:
                                property_data[th.get_text(strip=True)] = td.get_text(strip=True)

                    data_list.append(property_data)

    bienes_df = pd.DataFrame(data_list)
    bienes_df.rename(columns={'Property ID':'Identificador'}, inplace=True)
    columns_to_drop = ['Título jurídico', 'Información adicional', 'Valor Subasta', 'Valor de tasación', 'Importe del depósito', 'Puja mínima', 'Tramos entre pujas', 'IDUFIR']
    bienes_df = bienes_df.drop(columns=columns_to_drop)
    return bienes_df
