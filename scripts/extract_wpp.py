import pandas as pd
from datetime import date
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()


def fetch_and_stage_excel(
    excel_path: str,
    sheet_name: str,
    output_csv: str
):
    # 1. Carga la hoja "Medium variant", saltando las filas de metadata
    df = pd.read_excel(
        excel_path,
        sheet_name=sheet_name,
        header=16,        # la fila 17 (0-indexed=16) contiene los nombres de columna
        engine='openpyxl'
    )

    # 2. Selecciona y renombra solo las columnas que necesitas
    df = df[[
        'Region, subregion, country or area *',
        'Location code',
        'Total Population, as of 1 January (thousands)'
    ]].rename(columns={
        'Region, subregion, country or area *': 'country_name',
        'Location code': 'country_code',
        'Total Population, as of 1 January (thousands)': 'population_as_of_1_january'
    })

    # 3. Añade metadatos
    df['year'] = 2024
    df['variant'] = 'Medium'
    df['last_updated'] = date.today()

    # 4. Asegura la carpeta de salida
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)

    # 5. Guarda el CSV de staging
    df.to_csv(output_csv, index=False)
    print(f"🟢 CSV de staging generado en {output_csv} con {len(df)} filas.")

if __name__ == '__main__':
    RAW_DIR = os.getenv('DATA_RAW_PATH', 'airflow/data/raw/')
    STAGING_DIR = os.getenv('DATA_STAGING_PATH', 'airflow/data/staging/')

    RAW = os.path.join(RAW_DIR, 'WPP2024_GEN_F01_DEMOGRAPHIC_INDICATORS_FULL.xlsx')
    OUT = os.path.join(STAGING_DIR, 'staging_population_wpp.csv')

    fetch_and_stage_excel(RAW, 'Medium variant', OUT)

    print(f"📌 RAW_DIR: {RAW_DIR}")
    print(f"📌 STAGING_DIR: {STAGING_DIR}")
    print(f"📌 Archivo salida: {OUT}")


