from django.shortcuts import render,redirect, get_object_or_404
from .models import Service, ServiceType, Reservation, ServiceReservation
from django.views import View
from django.db.models import Sum
from django.http import HttpResponse
from datetime import date

# Create your views here.
def index(request):
    return render(request, 'core/index.html')

def index1(request):
    return render(request, 'core/index1.html')

def login(request):
    return render(request, 'core/login.html')

def registro(request):
    return render(request, 'core/registro.html')

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
        errors = {} #diccionario para errores por campo

        if not name:
            errors['name'] = "El nombre es requerido"

        if not service:
            errors['service'] = "El servicio es requerido"

        if not price:
            errors['price'] = "El precio es requerido"

        if not image:
            errors['image'] = "La imagen es requerida"

        if errors:
            service_types = ServiceType.objects.all()
            return render( request, self.template_name, {
                'service_types': service_types,
                'errors': errors,
            })

        new_service = Service.objects.create(
            name=name,
            price=price,
            description=description,
            service_type=service,
            image=image
            
        )
        return redirect('maquillaje')
    

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
    
class ReservationCreateView(View):
    template_name = 'core/reservacion.html'

    def get(self, request, *args, **kwargs):
        services = Service.objects.all()
        today= date.today().strftime('%Y-%m-%d')
        return render(request, self.template_name, {
            'services' : services, 'today': today
        })
    
    def post(self, request, *args, **kwargs):

        current_user = request.user

        reservation_date= request.POST.get("reservation_date")
        reservation_time=request.POST.get("reservation_time")

        selected_services_ids = request.POST.getlist('services')

        selected_services =Service.objects.filter(id__in=selected_services_ids)

        print(selected_services)

        total_price = selected_services.aggregate(Sum('price'))['price__sum'] or 0
        print(total_price)


        new_reservation = Reservation.objects.create(
            reservation_date = reservation_date,
            reservation_time = reservation_time,
            total_price= total_price,
            user= current_user
        )

        for service in selected_services:
            ServiceReservation.objects.create(
                reservation=new_reservation,
                service=service
            )
        
        return redirect('reservacion_success', reservation_id=new_reservation.id)

class ReservationSuccessView(View):
    # template_name = 'core/reservacion.html'

    def get(self, request,reservation_id, *args, **kwargs):
        reservation = Reservation.objects.get(id=reservation_id)
        return HttpResponse(reservation)
        # return render(request, self.template_name, {'reservations' : reservation})

