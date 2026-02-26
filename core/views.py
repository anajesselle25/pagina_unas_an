from django.shortcuts import render,redirect, get_object_or_404
from .models import Service, ServiceType, Reservation, ServiceReservation
from django.views import View
from django.db.models import Sum, Q
from django.http import HttpResponse
from datetime import date
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, get_user_model, logout
from .forms import LoginForm, RegisterForm
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
def index(request):
    return render(request, 'core/index.html')

def index1(request):
    return render(request, 'core/index1.html')

class ServiceCreateView(LoginRequiredMixin,View):
    template_name = 'core/servicio.html'

    def get(self, request, *args, **kwargs):
        service_types = ServiceType.objects.all()
        if request.user.is_authenticated:
            return redirect('login')
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
    paginate_by = 2

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        service_type =request.GET.get('service_type')
        services = Service.objects.all()

        if query:
            services = services.filter(
                Q(name__icontains=query)  |
                Q(description__icontains=query)   |
                Q(price__icontains=query)
            ).distinct()
        
        if service_type:
            services = services.filter(service_type__id=service_type)

        paginator = Paginator(services, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        query_dict=request.GET.copy()
        if 'page' in query_dict:
            del query_dict['page']
        url_params=query_dict.urlencode()

        context = {
            'page_obj': page_obj,
            'services' : page_obj.object_list,
            'query' : query,
            'service_types': ServiceType.objects.all(),
            'service_type': ServiceType.objects.filter(id=service_type).first() if service_type else None, 
            'url_params': url_params
        }
        return render(request, self.template_name, context)
    

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
        try:
            service = get_object_or_404(Service, id=id)
            service.delete()
        #redirige a la lista de servicios despues de la eliminacion
            return redirect('maquillaje')
        except Exception as e:
            return HttpResponse("No se puede eliminar el servicio")



    
class ReservationCreateView(LoginRequiredMixin,View):
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
        
        return render(request, 'core/reservacion_success.html', {'reservation':new_reservation})

class ReservationSuccessView(View):
    # template_name = 'core/reservacion.html'

    def get(self, request,reservation_id, *args, **kwargs):
        reservation = Reservation.objects.get(id=reservation_id)
        return HttpResponse(reservation)
        # return render(request, self.template_name, {'reservations' : reservation})

class UserLoginView(View):
    template_name = 'core/login.html'

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        if request.user.is_authenticated:
            return redirect('maquillaje')
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('maquillaje')
            else:
                return render(request, self.template_name, {
                    'form': form,
                    'error_message': 'Nombre de Usuario o Contraseña Incorrectos.'
                })
        return render(request, self.template_name, {'form': form})
    

class UserRegisterView(View):
    template_name = 'core/registro.html'

    def get(self, request, *args, **kwargs):
        form = RegisterForm()
        if request.user.is_authenticated:
            return redirect('maquillaje')
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            User = get_user_model()
            user = User.objects.create_user(username=username, email=email, password=password)

            login(request, user)

            return redirect('maquillaje')
        
        return render(request, self.template_name, {'form': form})
    
class UserLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)

        return redirect('login')
    

class ReservationListView(View):
    template_name = 'core/mis_reservaciones.html'
    paginate_by = 3 

    def get(self,request, *args, **kwargs):
        query = request.GET.get('q')
        current_user = request.user
        reservations = Reservation.objects.filter(user=current_user)

        if query:
            reservations = reservations.filter(total_price=query)

        paginator = Paginator(reservations, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'page_obj': page_obj,
            'reservations' : page_obj.object_list,
            'query' : query,
        }

        return render(request, self.template_name, context )
    
class ReservationListAdminView(View):
    template_name = 'core/reservaciones.html'
    paginate_by = 3 

    def get(self,request, *args, **kwargs):
        query = request.GET.get('q')
        reservations = Reservation.objects.all()

        if  query:
            reservations = reservations.filter(
                Q(user__username__icontains=query),
                Q(total_price=query)
            ).distinct()

        paginator = Paginator(reservations, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'page_obj': page_obj,
            'reservations' : page_obj.object_list,
            'query' : query,
        }

        return render(request, self.template_name, context )
    
class ReservationDeleteView(View):
    template_name = 'core/reservation_confirm_delete.html'

    def get(self, request, id, *args, **kwargs):
        reservation = get_object_or_404(Reservation, id=id)

        return render(request, self.template_name, {'reservation': reservation})

    def post(self, request, id, *args, **kwargs):
        try:
            reservation = get_object_or_404(Reservation, id=id)
            reservation.delete()
        #redirige a la lista de servicios despues de la eliminacion
            return redirect('mis_reservaciones')
        except Exception as e:
            return HttpResponse("No se puede eliminar la reservacion")
        
class CompletedReservation(View):
    def post(self, request, id, *args, **kwargs):
        reservation = get_object_or_404(Reservation, id=id)
        reservation.completed = True
        reservation.save()
        return redirect('mis_reservaciones')
