from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator

# Create your models here.

#-------------------------------------------------------------------
#Usuario
#-------------------------------------------------------------------
class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    addres = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS= ["phone_number"]

    class Meta:
        db_table= "users"
        verbose_name='Usuario'
        verbose_name_plural= 'Usuarios'

    def __str__(self):
        return f"{self.username} ({self.email})"


#-------------------------------------------------------------------
#Tipo de Servicio
#-------------------------------------------------------------------

class ServiceType(models.Model):
    name = models.CharField(max_length=200)
    class Meta:
        db_table= 'service_types'
        verbose_name = 'Tipo_Servicio'
        verbose_name_plural= 'Tipo_Servicios'
    
    def __str__(self):
        return (f'Tipo de Servicio: {self.name}')


#-------------------------------------------------------------------
#Servicio
#-------------------------------------------------------------------

class Service(models.Model):
    service_type = models.ForeignKey(ServiceType, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(
        verbose_name='Descripcion detalla',
        max_length= 500,
        blank=True,
        null=True
    )

    image = models.ImageField(
        verbose_name= 'Imagen',
        upload_to= 'core/services',
        validators=[FileExtensionValidator(allowed_extensions=['jpg','jpeg','png','webp'])],
        blank= True,
        null=True
    )
    class Meta:
        db_table = 'services'
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'
        
    def __str__(self):
        return f"El servicio de {self.service.name} tiene un precio  de {self.service.price} "
    
    def delete(self, *args, **kwargs):
        if self.image:
            self.image.delete() #borra el archivo fisico del disco
        super().delete(*args, **kwargs)  #borra el registro del modelo de la DB

#-------------------------------------------------------------------
#Reservacion
#-------------------------------------------------------------------

class Reservation(models.Model):
    user = models.ForeignKey(User,on_delete=models.PROTECT,related_name='reservations')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    reservation_date = models.DateField()
    reservation_time = models.TimeField()

    class Meta:
        db_table = 'reservations'
        verbose_name = 'Reservación'
        verbose_name_plural = 'Reservaciones'       

    def __str__(self):
        return f"Reservación #{self.id} - {self.user.first_name} {self.user.last_name}"


#-------------------------------------------------------------------
#Servicio Reservacion
#-------------------------------------------------------------------

class ServiceReservation(models.Model):
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    reservation = models.ForeignKey(Reservation, on_delete=models.PROTECT)

    class Meta:
        db_table = 'service_reservations'
        unique_together= [['service', 'reservation']]

    def __str__(self):
        return f"{self.service.name} tiene un precio total de {self.service.price} "
    

