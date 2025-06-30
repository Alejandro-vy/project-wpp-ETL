import requests
import os

# URL de ejemplo (ajusta la URL oficial)
url = "https://population.un.org/wpp/Download/Files/1_Indicators%20(Standard)/CSV_FILES/WPP2022_TotalPopulationBySex.csv"

# Ruta de destino
data_dir = os.path.join(os.path.dirname(__file__), '..', 'airflow', 'data', 'raw')
os.makedirs(data_dir, exist_ok=True)

file_path = os.path.join(data_dir, 'WPP2022_TotalPopulationBySex.csv')

# Descargar CSV
response = requests.get(url)
with open(file_path, 'wb') as f:
    f.write(response.content)

print(f"Archivo guardado en: {file_path}")

