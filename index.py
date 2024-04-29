import os
import requests
import schedule
import time
from dotenv import load_dotenv

load_dotenv()

def get_ocupacion(id):
   
    url = f'https://eos-access.empark.com/integration/cuma/boards/occupancy/{id}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as error:
        print("Error en la solicitud:", error)
        raise

def get_ocupacion_m():
    return get_ocupacion(os.environ.get('idM'))

def get_ocupacion_c():
    return get_ocupacion(os.environ.get('idC'))

plataforma = os.environ.get('plataforma')


dispositivos = [
    {
        'accessToken': os.environ.get('tokenM'),
        'id': os.environ.get('idM'),
        'nombre': "Pablo Medina",
        'totales': 0,
        'libres': 0,
        'ocupado': 0,
        'ocupacion': 0,
    },
    {
        'accessToken': os.environ.get('tokenC'),
        'id': os.environ.get('idC'),
        'nombre': "Catedral",
        'totales': 0,
        'libres': 0,
        'ocupado': 0,
        'ocupacion': 0,
    }
]

def publish_telemetry(dispositivo):
    #print(dispositivo)
    try:
        data = get_ocupacion(dispositivo['id'])
        ocupadas, totales = map(int, data['occupancy'][0].split(':'))
        
        dispositivo['totales'] = totales
        dispositivo['ocupado'] = ocupadas
        dispositivo['libres'] = totales - ocupadas
        dispositivo['ocupacion'] = (ocupadas / totales) * 100

        telemetry_data = {
            'libres': dispositivo['libres'],
            'ocupado': dispositivo['ocupado'],
            'ocupacion': dispositivo['ocupacion'],
        }
        
        url_telemetry = f'http://{plataforma}/api/v1/{dispositivo["accessToken"]}/telemetry'
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        requests.post(url_telemetry, json=telemetry_data, headers=headers)

        attribute_data = {'totales': dispositivo['totales']}
        url_attributes = f'http://{plataforma}/api/v1/{dispositivo["accessToken"]}/attributes'
        requests.post(url_attributes, json=attribute_data, headers=headers)

        print(f"¡Datos de {dispositivo['nombre']} enviados correctamente como telemetría y atributos!")
    except Exception as error:
        print(f"Error al enviar los datos de {dispositivo['nombre']}:", error)

def job():
    for dispositivo in dispositivos:
        print(f"Iniciando la carga de datos telemétricos de {dispositivo['nombre']}...")
        publish_telemetry(dispositivo)

schedule.every(5).minutes.do(job)

if __name__ == "__main__":
    job()  # Ejecutar inmediatamente al iniciar
    while True:
        schedule.run_pending()
        time.sleep(1)
