from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from reservas_wally.models import Reserva
from reservas_wally.models import Cliente
from rest_framework import status
from django.core import serializers
import json
from django.db import models
from reservas_wally import models as modelsReserva


class APIReserva(APIView):

    def get(self, format=None):
        datas = Reserva.objects.all()
        data_json = serializers.serialize('json', datas)
        return Response(data_json, status=status.HTTP_200_OK)


class APIGETReserva(APIView):

    def post(self, request):
        data = request.data
        by_name = self.buscarReservas(data.get('nombre'), idCliente__nombre=data.get('nombre'))
        by_id = self.buscarReservas(data.get('id'), id=data.get('id'))
        by_telf = self.buscarReservas(data.get('telefono'), idCliente__telefono=data.get('telefono'))

        self.interseccion(by_name, by_id)
        self.interseccion(by_id, by_telf)

        json_response = json.dumps(by_telf)

        return Response(json_response, status=status.HTTP_200_OK)

    @staticmethod
    def interseccion(lista_1: list, lista_2: list):
        """ une los datos de lista_1 y lista_2 sin repetir datos, lo vacía en lista_2 """
        for data in lista_1:
            if data not in lista_2:
                lista_2.append(data)

    def buscarReservas(self, dato, **kwargs):
        """ Buscamos especificamente en Reserva con los datos enviados y si esta vacio entonces retorna [] """
        return self.buscar(Reserva, **kwargs) if dato != "" else []

    def buscar(self, clase, **kwargs):
        """ busca en la clase dada con los argumentos dados """
        response = clase.objects.filter(**kwargs)
        lista = [x.convert_dict() for x in response]
        return lista


class APIGETReservaFecha(APIView):

    def post(self, request):
        data = request.data

        if not data.get('fecha_actual') or \
                data.get('fecha_actual') == "" or \
                data.get('fecha_actual') == "null":
            return Response([], status=status.HTTP_204_NO_CONTENT)

        responses = Reserva.objects.filter(fecha_reserva=data.get('fecha_actual'))
        datas = [x.convert_dict() for x in responses]
        data_json = json.dumps(datas)
        return Response(data_json, status=status.HTTP_200_OK)