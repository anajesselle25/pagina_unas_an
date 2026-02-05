from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ServiceType, Service, Reservation, ServiceReservation

# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(ServiceType)
admin.site.register(Service)
admin.site.register(Reservation)
admin.site.register(ServiceReservation)

