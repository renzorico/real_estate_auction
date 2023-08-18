import pandas as pd
import re
from config.constants import STANDARDIZED_MAPPING

def parse_datetime(date_string):
    return pd.to_datetime(date_string.split('CET')[0].strip(), format='%d-%m-%Y %H:%M:%S')

def clean_numeric_columns(df):
    numeric_columns = ['Cantidad reclamada', 'Valor subasta', 'Tasación', 'Importe del depósito']
    for col in numeric_columns:
        df[col] = df[col].apply(lambda x: x.replace(' €', '').replace('.', '').replace(',', '.') if isinstance(x, str) else x)
        df[col] = pd.to_numeric(df[col], errors='coerce')

    special_numeric_columns = ['Puja mínima', 'Tramos entre pujas']
    for col in special_numeric_columns:
        df[col] = df[col].apply(lambda x: 0 if x == 'Sin tramos' else x)
        df[col] = df[col].apply(lambda x: x.replace(' €', '').replace('.', '').replace(',', '.') if isinstance(x, str) else x)
        df[col] = pd.to_numeric(df[col], errors='coerce')

    return df

def clean_data(df):
    df.drop('Forma adjudicación', axis=1, inplace=True)

    df['Fecha de inicio'] = df['Fecha de inicio'].apply(parse_datetime)
    df['Fecha de conclusión'] = df['Fecha de conclusión'].apply(parse_datetime)

    df['Fecha de inicio'] = df['Fecha de inicio'].dt.date
    df['Fecha de conclusión'] = df['Fecha de conclusión'].dt.date

    df = clean_numeric_columns(df)

    columns_to_fill = ['Valor subasta', 'Puja mínima', 'Cantidad reclamada', 'Tasación', 'Tramos entre pujas', 'Importe del depósito']
    df[columns_to_fill] = df[columns_to_fill].fillna(0)
    df['Cuenta expediente'] = df['Cuenta expediente'].fillna('0123 4567 89 0987 65')

    df['Lotes'] = df['Lotes'].replace('Sin lotes', 0)
    df['Lotes'] = df['Lotes'].astype(int)

    return df

def standardize_address(address):
    # Mapping of first words to standardized forms
    standardized_mapping = {
        'CL': 'CALLE',
        'LUGAR': 'LUGAR',
        'CAMINO': 'CAMINO',
        'CALLE': 'CALLE',
        'AV.': 'AVENIDA',
        'CL.': 'CALLE',
        'C/': 'CALLE',
        'C/COSTERETA,': 'CALLE COSTERETA',
        'UR': 'URBANIZACION',
        'C.': 'CALLE',
        'CM': 'CAMINO',
        'CR': 'CALLE',
        'C/SANTIAGO': 'CALLE SANTIAGO',
        'PA': 'PASAJE',
        'CARRETERA': 'CARRETERA',
        'AV': 'AVENIDA',
        'PJ': 'PASAJE',
        'C/VIRGEN': 'CALLE VIRGEN',
        'CALLE:': 'CALLE',
        'PARQUE': 'PARQUE',
        'PZ': 'PLAZA',
        'POLIGONO': 'POLIGONO',
        'PG': 'POLIGONO',
        'POLÍGONO': 'POLIGONO',
        'PLAZA': 'PLAZA',
        'C/BLASCO': 'CALLE BLASCO',
        'PASAJE': 'PASAJE',
        'C/CHILE': 'CALLE CHILE',
        'C/TEIDE': 'CALLE TEIDE',
        'C/ALFONSO': 'CALLE ALFONSO',
        '"EDIFICIO': 'EDIFICIO',
        'CL/': 'CALLE',
        'AVENIDA': 'AVENIDA',
        'NUMERO': 'NUMERO',
        'URB.': 'URBANIZACION',
        'C/ANTONIO': 'CALLE ANTONIO',
        'URB': 'URBANIZACION',
        'RONDA': 'RONDA',
        'RAMBLA': 'RAMBLA',
        'URBANIZACION': 'URBANIZACION',
        'C/LUÍS': 'CALLE LUIS',
        'C/NICOLÁS': 'CALLE NICOLAS',
        'PG.': 'POLIGONO',
        'AVDA': 'AVENIDA',
        'TRAVESIA': 'TRAVESIA',
        'RAMAL': 'RAMAL',
        'CTRA': 'CARRETERA',
        'PASEO': 'PASEO',
        'SOLAR': 'SOLAR',
        'CAMI': 'CAMINO',
        'C/SANTO': 'CALLE SANTO',
        'AVD': 'AVENIDA',
        'PARCELA': 'PARCELA',
        'AVDA.': 'AVENIDA'
    }

    # Apply standardization to the 'Dirección' column
    return ' '.join([standardized_mapping.get(address.split()[0], address.split()[0].upper())] + address.split()[1:])


def extract_address(address):
    match = re.match(r'^(.*?\d+)\b', address)
    if match:
        return match.group(1)
    return address

def preprocess_data(df):
    df = clean_data(df)
    df['Dirección'] = df['Dirección'].apply(extract_address)
    df['Código Postal'] = df['Código Postal'].str.replace('CP', '').str.strip()
    df['Localidad'] = df['Localidad'].str.replace('No consta', 'Consuela')
    df.fillna('No consta', inplace=True)

    columns_to_convert = ['Dirección', 'Código Postal', 'Localidad', 'Provincia']
    df[columns_to_convert] = df[columns_to_convert].apply(lambda x: x.str.upper())

    return df
