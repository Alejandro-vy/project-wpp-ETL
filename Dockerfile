# Extiende la imagen oficial de Airflow
FROM apache/airflow:2.5.1

# Cambia a usuario airflow para instalar paquetes desde PyPI
USER airflow

# Copia el archivo de requisitos
COPY requirements.txt ./

# Instala las dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Vuelve a usuario airflow (ya estaba)
USER airflow
