# test_connection.py
from sqlalchemy import create_engine

DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/wpp_etl_db"

engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    result = conn.execute("SELECT 1;")
    print(result.fetchone())
