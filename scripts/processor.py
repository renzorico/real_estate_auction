import pandas as pd
import re


def preprocess_data(df):
    # Perform data preprocessing and cleaning here
    df = (
        process_datetime_column(
            process_datetime_column(df, "Fecha de inicio"), "Fecha de conclusión"
        )
        .pipe(standardized_address)
        .pipe(create_direccion_mapa_column)
        .pipe(convert_numeric_columns)
        .pipe(fillna_values)
        .pipe(remove_invalid_rows)
    )
    # Apply the formatting function to the 'Descripción' column
    df["Descripción"] = df["Descripción"].apply(format_description)
    # Convert 'Localidad' and 'Provincia' columns to uppercase
    df[["Localidad", "Provincia"]] = df[["Localidad", "Provincia"]].applymap(str.upper)
    # Create the "Dirección Mapa" column
    df["Dirección Mapa"] = df["Dirección"].apply(extract_address)
    return df

def process_datetime_column(df, column_name):
    df[column_name] = df[column_name].apply(
        lambda date_string: pd.to_datetime(
            date_string.split("CET")[0].strip(), format="%d-%m-%Y %H:%M:%S"
        ).date()
    )
    return df


def create_direccion_mapa_column(df):
    df["Dirección Mapa"] = df["Dirección"].apply(extract_address)
    return df


def remove_invalid_rows(df):
    # Drop rows with missing 'Dirección Mapa' or 'Código Postal' values
    df = df.dropna(subset=["Dirección Mapa", "Código Postal"])
    return df


def standardized_address(df):
    # Create a mapping of first words to standardized forms
    standardized_mapping = {
        "C/": "CALLE",
        "CL": "CALLE",
        "AV.": "AVENIDA",
        "CL.": "CALLE",
        "C/COSTERETA,": "CALLE COSTERETA",
        "UR": "URBANIZACION",
        "C.": "CALLE",
        "CM": "CAMINO",
        "CR": "CALLE",
        "C/SANTIAGO": "CALLE SANTIAGO",
        "PA": "PASAJE",
        "AV": "AVENIDA",
        "PJ": "PASAJE",
        "C/VIRGEN": "CALLE VIRGEN",
        "CALLE:": "CALLE",
        "PZ": "PLAZA",
        "PG": "POLIGONO",
        "POLÍGONO": "POLIGONO",
        "C/BLASCO": "CALLE BLASCO",
        "C/CHILE": "CALLE CHILE",
        "C/TEIDE": "CALLE TEIDE",
        "C/ALFONSO": "CALLE ALFONSO",
        '"EDIFICIO': "EDIFICIO",
        "URB.": "URBANIZACION",
        "C/ANTONIO": "CALLE ANTONIO",
        "URB": "URBANIZACION",
        "C/LUÍS": "CALLE LUIS",
        "C/NICOLÁS": "CALLE NICOLAS",
        "PG.": "POLIGONO",
        "AVDA": "AVENIDA",
        "CTRA": "CARRETERA",
        "CAMI": "CAMINO",
        "C/SANTO": "CALLE SANTO",
        "AVD": "AVENIDA",
        "AVDA.": "AVENIDA",
    }

    # Function to apply standardization to an address
    def apply_standardization(address):
        if isinstance(address, str):
            words = address.split()
            standardized_words = [
                standardized_mapping.get(word, word.upper()) for word in words
            ]

            return " ".join(standardized_words)
        return address

    # Apply standardization to the 'Dirección' column
    df["Dirección"] = df["Dirección"].apply(apply_standardization)

    return df

def convert_numeric_columns(df):
    # List of columns to convert to float
    columns_to_convert = [
        "Valor subasta",
        "Tasación",
        "Puja mínima",
        "Tramos entre pujas",
        "Importe del depósito",
        "Cantidad reclamada",
    ]

    for col in columns_to_convert:
        # Check if the column exists in the DataFrame
        if col in df.columns:
            df[col] = df[col].apply(
                lambda x: x.replace(" €", "").replace(".", "").replace(",", ".")
                if isinstance(x, str)
                else x
            )
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # List of special columns with special handling
    special_numeric_columns = ["Puja mínima", "Tramos entre pujas"]

    for col in special_numeric_columns:
        # Check if the column exists in the DataFrame
        if col in df.columns:
            df[col] = df[col].apply(lambda x: 0 if x == "Sin tramos" else x)
            df[col] = df[col].apply(
                lambda x: x.replace(" €", "").replace(".", "").replace(",", ".")
                if isinstance(x, str)
                else x
            )
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Fill NaN values in specific columns
    columns_to_fill = [
        "Valor subasta",
        "Puja mínima",
        "Cantidad reclamada",
        "Tasación",
        "Tramos entre pujas",
        "Importe del depósito",
    ]
    df[columns_to_fill] = df[columns_to_fill].fillna(0)
    df["Cuenta expediente"] = df["Cuenta expediente"].fillna("0123 4567 89 0987 65")

    return df

def fillna_values(df):
    try:
        # Columns to fill with 'No consta'
        columns_to_fill_with_no_consta = [
            "Localidad",
            "Forma adjudicación",
            "Provincia",
            "Tipo de subasta",
            "Vivienda habitual",
            "Situación posesoria",
            "Visitable",
            "IDUFIR",
            "Inscripción registral",
            "Información adicional",
            "Cargas",
            "Título jurídico",
            "Valor Subasta",
            "Valor de tasación",
        ]
        df[columns_to_fill_with_no_consta] = df[columns_to_fill_with_no_consta].fillna(
            "No consta"
        )

        # Fill NaN values in specific columns with 0
        columns_to_fill_with_zero = [
            "Valor subasta",
            "Puja mínima",
            "Cantidad reclamada",
            "Tasación",
            "Tramos entre pujas",
            "Importe del depósito",
        ]
        df[columns_to_fill_with_zero] = df[columns_to_fill_with_zero].fillna(0)

        # Fill NaN values in 'Cuenta expediente'
        df["Cuenta expediente"] = df["Cuenta expediente"].fillna("0123 4567 89 0987 65")

        # Replace 'Sin lotes' with 0
        df["Lotes"] = df["Lotes"].replace("Sin lotes", 0)

        # Convert the 'Lotes' column to integer type
        df["Lotes"] = df["Lotes"].astype(int)

        # List of first words to filter out
        words_to_filter = [
            "LG",
            "TN",
            "PEBRES",
            "VIVIENDA",
            "CP",
            "MN",
            "30005",
            "PD",
            "AR",
            "CN",
            "GREGORIO",
            "NUEVA",
            "POU",
            "RAMON",
            "PARAJE",
            "PARTIDA",
            "DISEMINADO",
            "SAN",
            "PEREIJO.",
            "SANTA",
            "CAÑOCLAR",
            "NO",
            "CLOSA",
            "GRAN",
            "LA",
            "SUERTE",
        ]

        # Filter out rows with the specified first words in the address
        df = df[~df["Dirección"].str.split().str[0].isin(words_to_filter)]

    except Exception as e:
        # Handle the exception (print an error message, log, etc.)
        print(f"Error in fillna_values: {e}")

    return df

def format_description(description):
    formatted_words = []
    words = description.split()

    for word in words:
        # Capitalize the first letter
        formatted_word = word[0].upper() + word[1:].lower()

        # If the word contains a '.', capitalize the next letter
        if "." in word:
            formatted_word = formatted_word.replace(".", ". ").title()

        formatted_words.append(formatted_word)

    formatted_description = " ".join(formatted_words)
    return formatted_description


def extract_address(address):
    match = re.match(r"^(.*?\d+)\b", str(address))
    if match:
        return match.group(1)
    return address
