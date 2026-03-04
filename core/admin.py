from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ServiceType, Service, Reservation, ServiceReservation

# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(ServiceType)
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'description')
    search_fields = ('name', 'description', 'type_service__nombre')
    list_editable = ('price',)
    list_filter = ('service_type', )
    # list_per_page = 5
    exclude = ('description', )

admin.site.register(Reservation)
admin.site.register(ServiceReservation)

