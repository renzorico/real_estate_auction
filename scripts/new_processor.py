import pandas as pd
import re


def preprocess_data(df):
    df = (
        process_datetime_column(df, "Fecha de inicio")
        .pipe(standardized_address)
        .pipe(create_direccion_mapa_column)
        .pipe(convert_numeric_columns)
        .pipe(fillna_values)
        .pipe(remove_invalid_rows)
    )
    df["Descripción"] = df["Descripción"].apply(format_description)
    df[["Localidad", "Provincia"]] = df[["Localidad", "Provincia"]].apply(lambda x: x.map(str.upper))
    df["Dirección Mapa"] = df["Dirección"].apply(extract_address)
    return df


def process_datetime_column(df, column_name):
    df[column_name] = pd.to_datetime(
        df[column_name].str.split("CET").str[0].str.strip(), format="%d-%m-%Y %H:%M:%S"
    ).dt.date
    return df


def create_direccion_mapa_column(df):
    df["Dirección Mapa"] = df["Dirección"].apply(extract_address)
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
    columns_to_convert = [
        "Valor subasta",
        "Tasación",
        "Puja mínima",
        "Tramos entre pujas",
        "Importe del depósito",
        "Cantidad reclamada",
    ]

    for col in columns_to_convert:
        df[col] = pd.to_numeric(
            df[col].replace({" €": "", ",": "", "\.": ""}, regex=True), errors="coerce"
        )

    special_numeric_columns = ["Puja mínima", "Tramos entre pujas"]
    for col in special_numeric_columns:
        df[col] = (
            df[col]
            .replace("Sin tramos", 0)
            .apply(
                lambda x: pd.to_numeric(
                    x.replace({" €": "", ",": "", "\.": ""}, regex=True),
                    errors="coerce",
                )
                if isinstance(x, str)
                else x
            )
        )

    df[["Valor subasta", "Puja mínima", "Cantidad reclamada", "Tasación", "Tramos entre pujas", "Importe del depósito"]] = df[
        ["Valor subasta", "Puja mínima", "Cantidad reclamada", "Tasación", "Tramos entre pujas", "Importe del depósito"]
    ].fillna(0)

    df["Cuenta expediente"] = df["Cuenta expediente"].fillna("0123 4567 89 0987 65")

    return df


def fillna_values(df):
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

    # Check if the columns exist before filling NaN values
    existing_columns = df.columns.intersection(columns_to_fill_with_no_consta)
    df[existing_columns] = df[existing_columns].fillna("No consta")

    columns_to_fill_with_zero = [
        "Valor subasta",
        "Puja mínima",
        "Cantidad reclamada",
        "Tasación",
        "Tramos entre pujas",
        "Importe del depósito",
    ]
    df[columns_to_fill_with_zero] = df[columns_to_fill_with_zero].fillna(0)

    df["Cuenta expediente"] = df["Cuenta expediente"].fillna("0123 4567 89 0987 65")

    df["Lotes"] = df["Lotes"].replace("Sin lotes", 0)
    df["Lotes"] = df["Lotes"].astype(int)

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
        "SANTA CAÑOCLAR",
        "NO",
        "CLOSA",
        "GRAN",
        "LA",
        "SUERTE",
    ]

    # Filter out rows with specified first words in the address
    df = df[~df["Dirección"].str.split().str[0].isin(words_to_filter)]

    return df



def format_description(description):
    formatted_words = [
        word.capitalize() if "." not in word else word.replace(".", ". ").title()
        for word in description.split()
    ]
    return " ".join(formatted_words)


def extract_address(address):
    match = re.match(r"^(.*?\d+)\b", str(address))
    return match.group(1) if match else address


# Add the remove_invalid_rows function
def remove_invalid_rows(df):
    df = df.dropna(subset=["Dirección Mapa", "Código Postal"])
    return df
