import os
import shutil
import requests
import re
from datetime import datetime
import json

nuevo_path = os.path.dirname(os.path.realpath(__file__)) + '/Nuevos/'
cargado_path = os.path.dirname(os.path.realpath(__file__)) + '/Cargados/'

for file in os.listdir(nuevo_path):
    try:
        nombre_sensor = file.split(' ')[0]
        time = file.split(' ')[1].replace('.', ':')
        date = file.split(' ')[2].replace('.txt', '')
        dateTime = date + ' ' + time
        dateTime = datetime.strptime(dateTime, '%Y-%m-%d %H:%M')
        mediciones = []
        with open(nuevo_path + file) as f:
            lectura = [x for x in f.read().split(';') if x]
            lectura = [re.findall(r'\d+|\D+', medicion)for medicion in lectura]
            for medicion in lectura:
                mediciones.append({'tipo': medicion[0], 'valor': medicion[1]})
        nuevaLectura = {
            'nombre_sensor': nombre_sensor,
            'fecha_lectura': dateTime,
            'lectura': json.dumps(mediciones)
        }
        print(lectura)
        r = requests.post(
            'http://127.0.0.1:8000/api/sensor/create', data=nuevaLectura)
        shutil.move(nuevo_path+file, cargado_path)
    except:
        print('')
