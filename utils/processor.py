import pandas as pd
import re

# def merge_data(properties_data, bienes_data):
#     # Combine properties_data and bienes_data using the 'Identificador' column
#     main_df = properties_data.merge(bienes_data, on='Identificador', how='inner')

#     # Data preprocessing and cleaning
#     main_df = preprocess_data(main_df)

    # return main_df

# Explanation:

#     The function process_data takes two DataFrames properties_data and bienes_data as input. These DataFrames contain property information and bienes (goods) information, respectively.
#     Using the .merge() method with the on='Identificador' argument, the function combines the two DataFrames based on the 'Identificador' column (assuming this column contains unique identifiers for each property) using an inner join (how='inner'). This results in a DataFrame main_df that contains combined property and bienes information.
#     The function then proceeds to preprocess and clean the data in the main_df DataFrame by calling the preprocess_data function. This is a function you would define to handle specific data preprocessing tasks, such as converting date formats, handling missing values, and standardizing address formats.
#     Finally, the function returns the preprocessed and cleaned DataFrame main_df, which contains combined and processed property and bienes information ready for further analysis or export.

def preprocess_data(df):
    # Perform data preprocessing and cleaning here
    df = (
        process_datetime_column(
            process_datetime_column(df, 'Fecha de inicio'),
            'Fecha de conclusión'
        )
        .pipe(standardized_address)
        .pipe(convert_numeric_columns)
        .pipe(fillna_values)
    )
    # Apply the formatting function to the 'Descripción' column
    df['Descripción'] = df['Descripción'].apply(format_description)
    # Convert 'Localidad' and 'Provincia' columns to uppercase
    df[['Localidad', 'Provincia']] = df[['Localidad', 'Provincia']].applymap(str.upper)
    # Create the "Dirección Mapa" column
    df['Dirección Mapa'] = df['Dirección'].apply(extract_address)
    return df

# Explanation:

#     The function preprocess_data takes a DataFrame df as input, which is the combined DataFrame containing property and bienes information.
#     Within this function, three preprocessing steps are applied to the DataFrame in sequence: address standardization, numeric column conversion, and filling NaN values.
#     The standardized_address(df) function is called to apply address standardization to the 'Dirección' column of the DataFrame. This function replaces or standardizes the street address terms in a consistent format.
#     The convert_numeric_columns(df) function is called to perform appropriate conversion of numeric columns in the DataFrame.

def process_datetime_column(df, column_name):
    df[column_name] = df[column_name].apply(
        lambda date_string: pd.to_datetime(date_string.split('CET')[0].strip(), format='%d-%m-%Y %H:%M:%S').date()
    )
    return df

def standardized_address(df):
    # Create a mapping of first words to standardized forms
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

    # Function to apply standardization to an address
    def apply_standardization(address):
        if isinstance(address, str):
            words = address.split()
            standardized_words = [standardized_mapping.get(word, word.upper()) for word in words]
            return ' '.join(standardized_words)
        return address

    # Apply standardization to the 'Dirección' column
    df['Dirección'] = df['Dirección'].apply(apply_standardization)

    return df

# Explanation:

#     Define the standardized_mapping dictionary with standardized forms of first words in addresses.
#     Define an inner function apply_standardization to apply standardization to a single address.
#     Inside apply_standardization, split the address into words and get the first word.
#     Look up the standardized form of the first word using standardized_mapping. If not found, keep the original.
#     Reconstruct the address with the standardized first word and the remaining words.
#     Apply the apply_standardization function to the 'Dirección' column of the DataFrame.
#     Return the modified DataFrame.

def convert_numeric_columns(df):
    # List of columns to convert to float
    columns_to_convert = [
        'Valor subasta', 'Tasación','Puja mínima', 'Tramos entre pujas','Importe del depósito', 'Cantidad reclamada'
    ]
    # Loop through columns and perform necessary conversions
    for col in columns_to_convert:
        df[col] = df[col].apply(
            lambda x: x.replace(' €', '').replace('.', '').replace(',', '.') if isinstance(x, str) else x
        )
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # List of special columns with special handling
    special_numeric_columns = ['Puja mínima', 'Tramos entre pujas']

    # Loop through special columns and perform necessary conversions
    for col in special_numeric_columns:
        df[col] = df[col].apply(lambda x: 0 if x == 'Sin tramos' else x)
        df[col] = df[col].apply(
            lambda x: x.replace(' €', '').replace('.', '').replace(',', '.') if isinstance(x, str) else x
        )
        df[col] = pd.to_numeric(df[col], errors='coerce')
    # Fill NaN values in specific columns
    columns_to_fill = [
        'Valor subasta', 'Puja mínima', 'Cantidad reclamada', 'Tasación',
        'Tramos entre pujas', 'Importe del depósito'
    ]
    df[columns_to_fill] = df[columns_to_fill].fillna(0)
    df['Cuenta expediente'] = df['Cuenta expediente'].fillna('0123 4567 89 0987 65')

    return df

# Explanation:

#     Create a list of columns_to_convert that contains the names of numeric columns to be converted.
#     Loop through the columns in columns_to_convert.
#     In the loop, apply a lambda function to replace unnecessary characters and convert to numeric type.
#     Create a list special_numeric_columns containing columns that need special handling.
#     Loop through special_numeric_columns and apply a lambda function to replace 'Sin tramos' with 0.
#     Apply the same numeric conversion process as before to special_numeric_columns.
#     Create a list columns_to_fill with columns that need NaN values filled.
#     Loop through columns_to_fill and fill NaN values with 0 for numeric columns and a default value for 'Cuenta expediente'.
#     Return the modified DataFrame.

# Note: Replace the code inside columns_to_convert, special_numeric_columns, and columns_to_fill lists with the appropriate column names from your dataset.

def fillna_values(df):
    # Columns to fill with 'No consta'
    columns_to_fill_with_no_consta = ['Localidad', 'Forma adjudicación', 'Provincia', 'Tipo de subasta', 'Vivienda habitual','Situación posesoria','Visitable','IDUFIR','Inscripción registral','Información adicional','Cargas','Título jurídico','Valor Subasta','Valor de tasación']
    df[columns_to_fill_with_no_consta] = df[columns_to_fill_with_no_consta].fillna('No consta')

    # Fill NaN values in specific columns with 0
    columns_to_fill_with_zero = [
        'Valor subasta', 'Puja mínima', 'Cantidad reclamada', 'Tasación',
        'Tramos entre pujas', 'Importe del depósito'
    ]
    df[columns_to_fill_with_zero] = df[columns_to_fill_with_zero].fillna(0)

    # Fill NaN values in 'Cuenta expediente'
    df['Cuenta expediente'] = df['Cuenta expediente'].fillna('0123 4567 89 0987 65')

    # Replace 'Sin lotes' with 0
    df['Lotes'] = df['Lotes'].replace('Sin lotes', 0)

    # Convert the 'Lotes' column to integer type
    df['Lotes'] = df['Lotes'].astype(int)

    # List of first words to filter out
    words_to_filter = [
        'LG', 'TN', 'PEBRES', 'VIVIENDA', 'CP', 'MN', '30005', 'PD', 'AR', 'CN',
        'GREGORIO', 'NUEVA', 'POU', 'RAMON', 'PARAJE', 'PARTIDA', 'DISEMINADO',
        'SAN', 'PEREIJO.', 'SANTA', 'CAÑOCLAR', 'NO', 'CLOSA', 'GRAN', 'LA', 'SUERTE'
    ]

    # Filter out rows with the specified first words in the address
    df = df[~df['Dirección'].str.split().str[0].isin(words_to_filter)]

    return df

# Explanation:

#     Create a list columns_to_fill_with_no_consta containing columns where NaN values should be filled with 'No consta'.
#     Fill the specified columns with 'No consta' using the .fillna() method.
#     Create a list columns_to_fill_with_zero with columns that need NaN values filled with 0.
#     Fill the specified columns with 0 using the .fillna() method.
#     Fill NaN values in the 'Cuenta expediente' column with a default value using the .fillna() method.
#     Return the modified DataFrame.

def format_description(description):
    formatted_words = []
    words = description.split()

    for word in words:
        # Capitalize the first letter
        formatted_word = word[0].upper() + word[1:].lower()

        # If the word contains a '.', capitalize the next letter
        if '.' in word:
            formatted_word = formatted_word.replace('.', '. ').title()

        formatted_words.append(formatted_word)

    formatted_description = ' '.join(formatted_words)
    return formatted_description


def extract_address(address):
    match = re.match(r'^(.*?\d+)\b', str(address))
    if match:
        return match.group(1)
    return address
