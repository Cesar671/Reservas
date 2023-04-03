import datetime
import json
import pytest

from django.test import TestCase
from reservas_wally.models import Reserva, ReservaManager
from reservas_wally.models import Cliente, ClienteManager
from reservas_wally.models import Hora, HoraManager

from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse


class ReservaTest(TestCase):
    NOMBRE = 'jhamil'
    TELEFONO = 77777777
    HORA_INICIO = datetime.time(9, 30)
    CANCHA = '1'

    @classmethod
    def setUpTestData(cls):
        cli = ClienteManager.create(nombre=cls.NOMBRE, telefono=cls.TELEFONO)
        reserva = ReservaManager.create(fecha_reserva=datetime.datetime.today().strftime('%Y-%m-%d'), idCliente=cli, cancha=cls.CANCHA)
        hora = HoraManager.create(hora_inicio=cls.HORA_INICIO, idReserva=reserva)

    def test_verificar_datos_reserva(self):
        reserva = Reserva.objects.get(id=1)
        cliente = reserva.idCliente
        self.assertEqual(cliente.nombre, self.NOMBRE)
        self.assertEqual(cliente.telefono, self.TELEFONO)

    def test_verificar_hora_reserva(self):
        hora = Hora.objects.get(id=1)
        hora_especifica = hora.hora_inicio
        self.assertEqual(self.HORA_INICIO, hora_especifica)


class ViewReservasTest(TestCase):
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

    @classmethod
    def setUpTestData(cls):
        for data in cls.DATA_RESERVAS:
            cliente = data.get('cliente')
            nombre = cliente.get('nombre')
            telefono = cliente.get('telefono')
            fecha_reserva = data.get('fecha_reserva')
            cancha = data.get('cancha')
            hora_inicio = data.get('hora_reserva')

            cli = ClienteManager.create(nombre=nombre, telefono=telefono)
            reserva = ReservaManager.create(fecha_reserva=fecha_reserva, idCliente=cli, cancha=cancha)
            hora = HoraManager.create(hora_inicio=hora_inicio, idReserva=reserva)

    def test_obtener_todas_las_reservas(self):
        cantidad_actual = len(self.DATA_RESERVAS)
        cli = APIClient()
        url = reverse('reserva-all')
        json_data = cli.get(url).data
        data = json.loads(json_data)
        cantidad_esperada = len(data)
        self.assertEqual(cantidad_esperada, cantidad_actual)
        self.assertEqual(status.HTTP_200_OK, 200)

    def test_verificar_coincidencia_por_telefono_void(self):
        payload = {
            'telefono': 87654321,
            'id': "",
            'nombre': "",
            'fecha_reserva': "",
        }

        cli = APIClient()
        url = reverse('reserva-resultado')
        data = cli.post(url, payload)
        json_data = json.loads(data.data)
        self.assertEquals(len(json_data), 0)
        self.assertEqual(status.HTTP_200_OK, 200)

    def test_verificar_coincidencia_por_telefono_true(self):
        payload = {
            'telefono': 77777777,
            'id': "",
            'nombre': "",
            'fecha_reserva': "",
        }
        cli = APIClient()
        url = reverse('reserva-resultado')
        data = cli.post(url, payload).data

        tam = len(json.loads(data))

        self.assertEquals(tam, 1)
        self.assertEqual(status.HTTP_200_OK, 200)

    def test_verificar_coincidencia_por_nombre_true(self):
        payload = {
            'telefono': "",
            'id': "",
            'nombre': "carlos",
            'fecha_reserva': "",
        }
        cli = APIClient()
        url = reverse('reserva-resultado')
        data = cli.post(url, payload).data

        tam = len(json.loads(data))

        self.assertEquals(tam, 2)
        self.assertEqual(status.HTTP_200_OK, 200)

    def test_verificar_coincidencia_por_nombre_void(self):
        payload = {
            'telefono': "",
            'id': "",
            'nombre': "sergio",
            'fecha_reserva': "",
        }
        cli = APIClient()
        url = reverse('reserva-resultado')
        data = cli.post(url, payload).data

        tam = len(json.loads(data))

        self.assertEquals(tam, 0)
        self.assertEqual(status.HTTP_200_OK, 200)

    def test_verificar_todo_vacio_void(self):
        payload = {
            'telefono': "",
            'id': "",
            'nombre': "",
            'fecha_reserva': "",
        }
        cli = APIClient()
        url = reverse('reserva-resultado')
        data = cli.post(url, payload).data

        tam = len(json.loads(data))

        self.assertEquals(tam, 0)
        self.assertEqual(status.HTTP_200_OK, 200)

    def test_verificar_coincidencias_multiples(self):
        payload = {
            'telefono': "12345678",
            'id': "",
            'nombre': "carlos",
            'fecha_reserva': "",
        }
        cli = APIClient()
        url = reverse('reserva-resultado')
        data = cli.post(url, payload).data

        tam = len(json.loads(data))

        self.assertEquals(tam, 2)
        self.assertEqual(status.HTTP_200_OK, 200)

    def test_verificar_coincidencias_vacio(self):
        payload = {
            'telefono': "",
            'id': "",
            'nombre': "",
            'fecha_reserva': "",
        }
        cli = APIClient()
        url = reverse('reserva-resultado')
        data = cli.post(url, payload).data

        tam = len(json.loads(data))

        self.assertEquals(tam, 0)
        self.assertEqual(status.HTTP_200_OK, 200)


class ViewReservasFechaTest(TestCase):

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

    @classmethod
    def setUpTestData(cls):
        for data in cls.DATA_RESERVAS:
            cliente = data.get('cliente')
            nombre = cliente.get('nombre')
            telefono = cliente.get('telefono')
            fecha_reserva = data.get('fecha_reserva')
            cancha = data.get('cancha')
            hora_inicio = data.get('hora_reserva')

            cli = ClienteManager.create(nombre=nombre, telefono=telefono)
            reserva = ReservaManager.create(fecha_reserva=fecha_reserva, idCliente=cli, cancha=cancha)
            hora = HoraManager.create(hora_inicio=hora_inicio, idReserva=reserva)

    def test_prueba_url_metodo_post(self):
        payload = {
            'fecha_actual': datetime.datetime(2022, 9, 11, tzinfo=None).strftime('%Y-%m-%d'),
        }

        cli = APIClient()
        url = reverse('reservas-dia')
        response = cli.post(url, payload)
        response_json = response.data
        data = json.loads(response_json)
        tam = len(data)
        self.assertEqual(tam, 2)
        self.assertEqual(response.status_code, 200)

    def test_prueba_url_void(self):
        payload = {
            'fecha_actual': datetime.datetime(2022, 11, 11, tzinfo=None).strftime('%Y-%m-%d'),
        }
        cli = APIClient()
        url = reverse('reservas-dia')
        response = cli.post(url, payload)
        response_json = response.data
        data = json.loads(response_json)
        tam = len(data)
        self.assertEqual(tam, 0)
        self.assertEqual(response.status_code, 200)

    def test_prueba_url_null(self):
        payload = {
            'fecha_actual': "",
        }
        cli = APIClient()
        url = reverse('reservas-dia')
        response = cli.post(url, payload)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


