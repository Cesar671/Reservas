from django.shortcuts import render

def getReservasDiaView(request, fecha):

    return render(request, 'index.html')