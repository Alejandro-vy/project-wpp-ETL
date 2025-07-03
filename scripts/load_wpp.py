import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv
from io import StringIO

# 1. Carga variables de entorno
load_dotenv()

DB_USER = os.getenv("PG_USER")
DB_PASS = os.getenv("PG_PASSWORD")
DB_HOST = os.getenv("PG_HOST", "localhost")
DB_PORT = os.getenv("PG_PORT", "5432")
DB_NAME = os.getenv("PG_DB")

def load_with_copy(csv_path: str, table_name: str):
    # 2. Lee el CSV completo
    df = pd.read_csv(csv_path)
    print(f"📊 Filas a cargar: {len(df)}")

    # 3. Renombra columnas para que coincidan con la tabla
    df = df.rename(columns={
        'population': 'population_as_of_1_january',
        'last_updated': 'last_update'
    })

    # 4. Asegura orden de columnas según la tabla en Postgres
    cols = [
        'country_name',
        'country_code',
        'population_as_of_1_january',
        'year',
        'variant',
        'last_update'
    ]
    df = df[cols]

    # 5. Conecta a Postgres
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )
    cur = conn.cursor()

    # 6. Usa COPY para cargar desde un buffer en memoria
    buffer = StringIO()
    df.to_csv(buffer, index=False, header=False)
    buffer.seek(0)

    copy_sql = f"""
        COPY {table_name} ({', '.join(cols)})
        FROM STDIN WITH (FORMAT CSV)
    """
    cur.copy_expert(copy_sql, buffer)
    conn.commit()

    cur.close()
    conn.close()
    print("✅ Datos cargados correctamente con COPY.")

if __name__ == '__main__':
    PROCESSED_DIR = 'airflow/data/processed/'
    CSV_FILE = os.path.join(PROCESSED_DIR, 'processed_population_wpp.csv')
    load_with_copy(CSV_FILE, 'population')




