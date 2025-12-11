# Vistas

from django.shortcuts import render, redirect
from django.http import HttpResponse

def index(request):
    return render(request, 'se_core/index.html')

def acercade(request):
    return render(request, 'se_core/acercade.html')

def misionvision(request):
    return render(request, 'se_core/misionvision.html')

def contactanos(request):
    return render(request, 'se_core/contactanos.html')

def iniciosesion(request):
    return render(request, 'se_core/inicio_frm.html')

def loginn(request):
    correo = request.POST['correo']
    clave = request.POST['clave']
    
    if correo == "mateorojas@gmail.com" and clave == "12345":
        return HttpResponse(f"Usuario invalido - Correo: {correo}, Clave: {clave}")
    else:
        mensaje = " Datos no validos... Intente de nuevo."
        contexto = {'mensaje': mensaje}
        return render(request, 'se_core/inicio_frm.html', contexto)

