import pandas as pd
import os

def clean_airbnb_data(input_path, output_path):
    """
    Loads the raw Airbnb data CSV, cleans it, and saves a cleaned CSV.
    """
    
    # 1. Load the raw data
    df = pd.read_csv(input_path)
    print(f"Original data shape: {df.shape}")

    # 2. Remove duplicate rows if any
    before = df.shape[0]
    df = df.drop_duplicates()
    print(f"Removed {before - df.shape[0]} duplicate rows.")

    # 3. Strip whitespace in column names (clean any typo/format issues)
    df.columns = [col.strip() for col in df.columns]

    # 4. Handle missing values:
    # -eg.  For 'name' and 'host_name', replace missing with 'Unknown'
    df['name'] = df['name'].fillna('Unknown')
    df['host_name'] = df['host_name'].fillna('Unknown')
    df['reviews_per_month'] = df['reviews_per_month'].fillna(0)

    # 5. Parse 'last_review' to datetime format 
    df['last_review'] = pd.to_datetime(df['last_review'], errors='coerce')

    # 6. Remove rows with invalid or unrealistic 'price'
    # Here keep only listings with price > 0 and <= 1000 
    df = df[(df['price'] > 0) & (df['price'] <= 1000)]
    print(f"Data shape after price filtering: {df.shape}")

    # 8. Create new time-based columns from 'last_review' for easier analysis:
    df['last_review_year'] = df['last_review'].dt.year
    df['last_review_month'] = df['last_review'].dt.month_name()
    df['last_review_dayofweek'] = df['last_review'].dt.day_name()

    # 9. Reset index so data is clean and orderly
    df = df.reset_index(drop=True)

    df.to_csv(output_path, index=False)
    print(f"Cleaned data saved to: {output_path}")


if __name__ == "__main__":
    raw_file = "D:/PROJECT/PANDAS/data/AB_NYC_2019.csv"             # your original raw file path
    cleaned_file = "D:/PROJECT/PANDAS/data/cleaned_airbnb_2019.csv"  # path for cleaned output

    if os.path.exists(raw_file):
        clean_airbnb_data(raw_file, cleaned_file)
    else:
        print(f"File not found: {raw_file}")
