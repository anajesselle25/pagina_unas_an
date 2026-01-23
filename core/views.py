from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'core/index.html')

def index1(request):
    return render(request, 'core/index1.html')

def login(request):
    return render(request, 'core/login.html')

def maquillaje(request):
    return render(request, 'core/maquillaje.html')

def registro(request):
    return render(request, 'core/registro.html')

def reservacion(request):
    return render(request, 'core/reservacion.html')