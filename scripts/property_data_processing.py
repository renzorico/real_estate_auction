import pandas as pd
import requests
from bs4 import BeautifulSoup
from config.constants import PROPERTY_BIENES_URL, PROPERTY_PRUEBA, BIENES_PRUEBA

def fetch_property_bienes_data(properties_list):
    bienes_data_list = []
    for property_info in properties_list:
        if property_info.startswith('Subasta SUB-'):
            property_id = property_info.split(' ')[-1]

            response = requests.get(BIENES_PRUEBA)
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
                                column_name = th.get_text(strip=True)  # Strip leading/trailing whitespaces
                                column_value = td.get_text(strip=True)
                                property_data[column_name] = column_value
                    bienes_data_list.append(property_data)
    bienes_df = pd.DataFrame(bienes_data_list)
    bienes_df.rename(columns={'Property ID': 'Identificador'}, inplace=True)
    columns_to_drop = ['Título jurídico', 'Información adicional', 'Valor Subasta', 'Valor de tasación','Importe del depósito', 'Puja mínima', 'Tramos entre pujas', 'Cantidad reclamada','Cuota', 'Parcela','IDUFIR']

    # Strip any leading/trailing whitespaces from column names
    columns_to_drop = [col.strip() for col in columns_to_drop]

    print(bienes_df.columns)
    bienes_df.drop(columns=columns_to_drop, inplace=True)


    return bienes_df

def preprocess_bienes_data(bienes_df):
    main_df = bienes_df.copy()  # Make a copy of the bienes_df
    main_df = main_df.dropna(subset=['Dirección', 'Código Postal'])
    main_df['Localidad'] = main_df['Localidad'].fillna('Consuela')
    main_df.fillna('No consta', inplace=True)
    columns_to_convert = ['Dirección', 'Código Postal', 'Localidad', 'Provincia']
    main_df[columns_to_convert] = main_df[columns_to_convert].apply(lambda x: x.str.upper())

    return main_df
