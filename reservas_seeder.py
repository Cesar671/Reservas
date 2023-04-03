
import sqlite3
import json
import datetime

PersonaA = {
        'nombre': 'jhamil',
        'telefono': 77777777,
    }

PersonaB = {
        'nombre': 'carlos',
        'telefono': 12345678
    }

DATA_RESERVAS = [
        {
            'cliente': PersonaA,
            'fecha_reserva': datetime.datetime(2022, 9, 11, tzinfo=None).strftime('%Y-%m-%d'),
            'hora_reserva': datetime.time(9, 30),
            'cancha': '1',
        }, {
            'cliente': PersonaB,
            'fecha_reserva': datetime.datetime(2022, 9, 11, tzinfo=None).strftime('%Y-%m-%d'),
            'hora_reserva': datetime.time(9, 30),
            'cancha': '2',
        }, {
            'cliente': PersonaB,
            'fecha_reserva': datetime.datetime(2022, 10, 11, tzinfo=None).strftime('%Y-%m-%d'),
            'hora_reserva': datetime.time(14, 30),
            'cancha': '1',
        }
    ]

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()
cursor.row_factory = sqlite3.Row
reservas = 'reservas_wally_reserva'
cliente = 'reservas_wally_cliente'
hora = 'reservas_wally_hora'
statement = f"SELECT * from {reservas}"
resposne = cursor.execute(statement)
response_json = json.dumps([dict(x) for x in resposne])



print(response_json)
