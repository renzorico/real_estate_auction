def save_to_csv(df, filename):
    # Save the DataFrame to an Excel file
    df.to_csv(filename, index=False)
