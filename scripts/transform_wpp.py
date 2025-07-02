import pandas as pd
import os
from datetime import date
from dotenv import load_dotenv

# Carga variables de entorno si las tienes
load_dotenv()

def transform_staging(input_csv: str, output_csv: str):
    """
    Lee el archivo de staging, realiza limpieza y guarda archivo limpio.
    """

    print(f"🔍 Leyendo archivo de staging: {input_csv}")
    df = pd.read_csv(input_csv)

    print("📊 Antes de limpiar:")
    print(df.info())
    print(df.head())

    # ================================
    # 1️⃣ Limpieza básica
    # ================================
    # Elimina filas con población nula o país nulo
    df = df.dropna(subset=['country_name', 'population'])

    # Quita espacios en blanco alrededor de los nombres de países
    df['country_name'] = df['country_name'].str.strip()

    # Asegura que population sea numérica y positiva
    df['population'] = pd.to_numeric(df['population'], errors='coerce')
    df = df[df['population'] > 0]

    # ================================
    # 2️⃣ Conversión de tipos
    # ================================
    df['population'] = df['population'].astype(int)

    # ================================
    # 3️⃣ Añadir metadatos si quieres
    # ================================
    df['transformed_at'] = date.today()

    # ================================
    # 4️⃣ Guarda el archivo limpio
    # ================================
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    df.to_csv(output_csv, index=False)

    print(f"✅ Transformación completada. Archivo guardado en {output_csv}")
    print(f"🔢 Filas finales: {len(df)}")


if __name__ == '__main__':
    # Define rutas (puedes usar .env o dejarlas fijas para local)
    STAGING_PATH = os.getenv('DATA_STAGING_PATH', 'airflow/data/staging/')
    WAREHOUSE_PATH = os.getenv('DATA_WAREHOUSE_PATH', 'airflow/data/warehouse/')

    input_csv = os.path.join(STAGING_PATH, 'staging_population_wpp.csv')
    output_csv = os.path.join(WAREHOUSE_PATH, 'population_wpp_clean.csv')

    transform_staging(input_csv, output_csv)

