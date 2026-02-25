from django .core.management.base import BaseCommand
from core.models import ServiceType

class Command(BaseCommand):
    help = 'Sembrar datos iniciales en la base de datos'

    def handle(self, *args, **options):
        # Seed ServiceType
        self.seed_service_types()
        self.stdout.write(self.style.SUCCESS('Datos iniciales sembrados exitosamente.'))


    def seed_service_types(self):
        service_types = [
            {'name': 'Manicure'},
            {'name': 'Pedicure'},
            {'name': 'Maquillaje'}
        ]
        for service_type in service_types:
            service_type, created = ServiceType.objects.get_or_create(**service_type)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Tipo de Servicio "{service_type.name}" creado.'))
            else:
                self.stdout.write(self.style.WARNING(f'Tipo de Servicio "{service_type.name}" ya existe.'))