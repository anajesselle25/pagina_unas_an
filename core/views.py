from django.shortcuts import render,redirect, get_object_or_404
from .models import Service, ServiceType
from django.views import View

# Create your views here.
def index(request):
    return render(request, 'core/index.html')

def index1(request):
    return render(request, 'core/index1.html')

def login(request):
    return render(request, 'core/login.html')

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
    

class ServiceListView(View):
    template_name = 'core/maquillaje.html'

    def get(self, request, *args, **kwargs):
        services = Service.objects.all()
        return render(request, self.template_name, {'services': services})
    
class ServiceDetailView(View):
    template_name = 'core/service_detail.html'

    def get(self, request, id, *args, **kwargs):
        #get object or 404 es una buena practica para manejar productos no encontrados
        service = get_object_or_404(Service, id=id)
        return render(request, self.template_name, {'s': service})
    

class ServiceUpdateView(View):
    template_name = 'core/service_update.html'

    def get(self, request, id, *args, **kwargs):
        service = get_object_or_404(Service, id=id)
        service_types = ServiceType.objects.all()  #necesario para el select de servicio
        return render(request, self.template_name, {'service': service, 'service_types': service_types})
    
    def post(self, request, id,*args, **kwargs):
        service = get_object_or_404(Service, id=id)
        name= request.POST.get("name")
        price=request.POST.get("price")
        description=request.POST.get("description", "")
        service_type_id= request.POST.get("service_type")
        service_type= ServiceType.objects.filter(id=service_type_id).first() if service_type_id else None
        new_image_file = request.FILES.get('image')

        service.name = name
        service.price=price
        service.description=description
        service.service_type=service_type
        if new_image_file:
            if service.image and service.image.name:
                service.image.delete(save=False)
                #save=false previene que se guarde el modelo de antes
                #asignar la nueva imagen al campo del modelo
            service.image= new_image_file
        service.save()

        return redirect('maquillaje')
    
class ServiceDeleteView(View):
    template_name = 'core/service_confirm_delete.html'

    def get(self, request, id, *args, **kwargs):
        service = get_object_or_404(Service, id=id)
        return render(request, self.template_name, {'service': service})
    
    def post(self, request, id, *args, **kwargs):
        service = get_object_or_404(Service, id=id)
        service.delete()
        #redirige a la lista de servicios despues de la eliminacion
        return redirect('maquillaje')