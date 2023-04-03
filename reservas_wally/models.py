from django.db import models
import abc
import datetime


class Manager(metaclass=abc.ABCMeta):
    @staticmethod
    @abc.abstractmethod
    def create(**kwargs) -> models.Model:
        pass


class ClienteManager(Manager):

    @staticmethod
    def create(**kwargs) -> models.Model:
        """ nombre telefono """

        cli = Cliente(
            nombre=kwargs.get('nombre'),
            telefono=kwargs.get('telefono'),
            fecha_registro=datetime.datetime.today().strftime('%Y-%m-%d %H:%M'),
        )
        cli.save()
        return cli


class ReservaManager(Manager):

    @staticmethod
    def create(**kwargs) -> models.Model:
        """ fecha_reserva idCliente """

        reserva = Reserva(
            fecha_registro=datetime.datetime.today().strftime('%Y-%m-%d %H:%M'),
            fecha_reserva=kwargs.get('fecha_reserva'),
            idCliente=kwargs.get('idCliente'),
            cancha=kwargs.get('cancha'),
        )
        reserva.save()
        return reserva


class HoraManager(Manager):

    @staticmethod
    def create(**kwargs) -> models.Model:
        """ hora_inicio idReserva """

        hora = Hora(
            hora_inicio=kwargs.get('hora_inicio'),
            idReserva=kwargs.get('idReserva'),
            fecha_registro=datetime.datetime.today().strftime('%Y-%m-%d %H:%M'),
        )
        hora.save()
        return hora


class Cliente(models.Model):
    nombre = models.CharField(max_length=50, null=False)
    telefono = models.IntegerField(default=0)
    fecha_registro = models.DateTimeField(null=False)
    frecuente = models.BooleanField(default=False)

    def convert_dict(self):
        dictionary = {
            'nombre': self.nombre,
            'telefono': self.telefono,
            'fecha_registro': str(self.fecha_registro),
            'frecuente': self.frecuente,
            'id': self.pk
        }
        return dictionary


class Reserva(models.Model):
    CANCELADO = 'ca'
    PAGADO = 'pa'
    PENDIENTE = 'pe'

    CHOICES_STATES = [
        (CANCELADO, 'cancelado'),
        (PAGADO, 'pagado'),
        (PENDIENTE, 'pendiente'),
    ]

    CANCHA_1 = '1'
    CANCHA_2 = '2'

    CHOICES_CANCHAS = [
        (CANCHA_1, 'CANCHA 1'),
        (CANCHA_2, 'CANCHA 2')
    ]

    cancha = models.CharField(max_length=1, choices=CHOICES_CANCHAS, default=CANCHA_1)
    fecha_registro = models.DateTimeField(null=False)
    fecha_reserva = models.DateField(null=False)
    cantidad_a_pagar = models.IntegerField(default=0)
    estado = models.CharField(choices=CHOICES_STATES, max_length=2, default=PENDIENTE)
    idCliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def convert_dict(self):

        clientes = self.idCliente.convert_dict()
        horas = Hora.objects.filter(idReserva=self.pk)
        dict_horas = [x.convert_dict() for x in horas]

        dictionary = {
            'cancha': self.cancha,
            'fecha_registro': str(self.fecha_registro),
            'fecha_reserva': str(self.fecha_reserva),
            'cantidad_a_pagar': self.cantidad_a_pagar,
            'estado': self.estado,
            'cliente': clientes,
            'horas': dict_horas,
        }

        return dictionary


class Hora(models.Model):
    hora_inicio = models.TimeField(null=False)
    fecha_registro = models.DateTimeField(null=False)
    idReserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)

    def convert_dict(self):
        dictionary = {
            'id': self.pk,
            'hora_inicio': str(self.hora_inicio),
            'fecha_registro': str(self.fecha_registro),
            'idReserva': self.idReserva.pk,
        }
        return dictionary





