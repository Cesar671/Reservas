from django.urls import path
from reservas_wally.views import APIReserva
from reservas_wally.views import APIGETReserva
from reservas_wally.views import APIGETReservaFecha
urlpatterns = [
    path('getReservas', APIReserva.as_view(), name='reserva-all'),
    path('getResultado', APIGETReserva.as_view(), name='reserva-resultado'),
    path('getReservasDia', APIGETReservaFecha.as_view(), name='reservas-dia'),
]