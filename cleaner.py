import pandas as pd
import os
import re

def clean_data(file_path):
    ext = os.path.splitext(file_path)[-1]
    if ext == '.csv':
        df = pd.read_csv(file_path)
    elif ext in ['.xls', '.xlsx']:
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format.")

    # Standardize column names
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    # Strip whitespace in string fields
    str_cols = df.select_dtypes(include='object').columns
    df[str_cols] = df[str_cols].apply(lambda col: col.str.strip())

    # Clean full_name
    if 'full_name' in df.columns:
        df['full_name'] = df['full_name'].str.title()

    # Clean email
    if 'e-mail_address' in df.columns:
        df['e-mail_address'] = df['e-mail_address'].apply(
            lambda x: x.lower() if isinstance(x, str) else x
        )
        df['e-mail_address'] = df['e-mail_address'].apply(
            lambda x: x if isinstance(x, str) and re.fullmatch(r"[^@]+@[^@]+\.[^@]+", x) else None
        )

    # Clean start_date
    if 'start_date' in df.columns:
        df['start_date'] = pd.to_datetime(df['start_date'], errors='coerce').dt.date

    # Clean revenue
    if 'revenue($)' in df.columns:
        df['revenue($)'] = df['revenue($)'].replace({r'\$': '', ',': '', 'N/A': None, 'NULL': None}, regex=True)
        df['revenue($)'] = pd.to_numeric(df['revenue($)'], errors='coerce')

    # Clean region
    if 'region' in df.columns:
        df['region'] = df['region'].str.title()

    # Clean and deduplicate notes
    if 'notes' in df.columns:
        df['notes'] = df['notes'].fillna('').astype(str).str.strip()
        df['notes'] = df['notes'].replace(r'\s+', ' ', regex=True)

    # ✅ Drop invalid rows
    df.dropna(subset=['full_name', 'e-mail_address', 'start_date'], inplace=True)

    # ✅ Group and aggregate
    agg_funcs = {
        'start_date': 'max',
        'revenue($)': 'sum',
        'region': 'first',
        'notes': lambda x: '; '.join(sorted(set(filter(None, x))))
    }

    df = df.groupby(['full_name', 'e-mail_address'], as_index=False).agg(agg_funcs)

    return df

def save_cleaned_data(df, output_path):
    df.to_excel(output_path, index=False)

if __name__ == "__main__":
    input_file = "input/messy_file.xlsx"  # or "messy_file_100.xlsx"
    output_file = "output/cleaned_file.xlsx"

    print(f"📥 Cleaning file: {input_file}")
    df_cleaned = clean_data(input_file)
    print("✅ Final cleaned row count:", len(df_cleaned))

    os.makedirs("output", exist_ok=True)
    print(f"💾 Saving to: {os.path.abspath(output_file)}")
    save_cleaned_data(df_cleaned, output_file)
    print("🎉 Cleaned file successfully saved!")
