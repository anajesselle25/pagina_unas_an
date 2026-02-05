from django.shortcuts import render,redirect
from .models import Service, ServiceType
from django.views import View

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


class ServiceCreateView(View):
    template_name = 'core/servicio.html'

    def get(self, request, *args, **kwargs):
        service_types = ServiceType.objects.all()
        return render(request, self.template_name, {'service_types' : service_types})
    
    def post(self, request, *args, **kwargs):
        name= request.POST.get("name")
        price=request.POST.get("price")
        description=request.POST.get("description", "")
        service_type_id= request.POST.get("service_type")
        service = ServiceType.objects.filter(id=service_type_id).first() if service_type_id else None
        image_file = request.FILES.get('image')
        image = image_file

        new_service = Service.objects.create(
            name=name,
            price=price,
            description=description,
            service_type=service,
            image=image
            
        )
        return redirect('index1')