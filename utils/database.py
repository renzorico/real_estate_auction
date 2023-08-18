import pandas as pd

def save_to_excel(df, filename):
    # Save the DataFrame to an Excel file
    df.to_excel(filename, index=False)
