import pandas as pd
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def transform_staged_csv(input_csv: str, output_csv: str):
    print(f"📥 Leyendo archivo de staging: {input_csv}")
    df = pd.read_csv(input_csv)

    print(f"📊 Antes de limpiar:")
    print(df.info())
    print(df.head())

    # 1️⃣ Renombra bien si tiene typo
    if 'population_as_of_1_juanary' in df.columns:
        df = df.rename(columns={'population_as_of_1_juanary': 'population_as_of_1_january'})

    # 2️⃣ Limpieza básica
    df['country_name'] = df['country_name'].astype(str).str.strip()
    df['variant'] = df['variant'].astype(str).str.strip()

    # 3️⃣ Convierte población a número
    df['population_as_of_1_january'] = pd.to_numeric(df['population_as_of_1_january'], errors='coerce')

    # ⚠️ Haz dropna SOLO de columnas que existan
    df = df.dropna(subset=['country_name', 'population_as_of_1_january'])

    # 4️⃣ Crear columna 'population'
    df['population'] = df['population_as_of_1_january'] * 1000

    # 5️⃣ Elimina la columna intermedia
    df = df.drop(columns=['population_as_of_1_january'])

    # 6️⃣ Reordenar columnas si quieres
    df = df[['country_code', 'country_name', 'year', 'variant', 'population', 'last_updated']]

    print(f"📊 Transformado: {df.shape[0]} filas")
    print(df.head())

    # 7️⃣ Guardar transformado
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    df.to_csv(output_csv, index=False)
    print(f"✅ Archivo transformado guardado en: {output_csv}")

if __name__ == '__main__':
    STAGING_DIR = os.getenv('DATA_STAGING_PATH', 'airflow/data/staging/')
    PROCESSED_DIR = os.getenv('DATA_PROCESSED_PATH', 'airflow/data/processed/')

    IN = os.path.join(STAGING_DIR, 'staging_population_wpp.csv')
    OUT = os.path.join(PROCESSED_DIR, 'processed_population_wpp.csv')

    transform_staged_csv(IN, OUT)


