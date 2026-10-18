from django.core.management.base import BaseCommand
from core.models import ServiceType, Service

class Command(BaseCommand):
    help = 'Sembrar datos iniciales en la base de datos'

    def handle(self, *args, **options):
        # Seed ServiceType
        self.seed_service_types()
        self.seed_services()
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

    def seed_services(self):
        manicure = ServiceType.objects.filter(name='Manicure').first()
        pedicure = ServiceType.objects.filter(name='Pedicure').first()
        maquillaje = ServiceType.objects.filter(name='Maquillaje').first()

        services_data = [
            {
                'service_type': manicure,
                'name': 'Manicura Clásica',
                'price': 15.00,
                'description': 'Limado, pulido, cutícula y esmalte tradicional. Incluye hidratación en manos y masajes relajantes.',
                'image': 'core/services/clasica.jpeg'
            },
            {
                'service_type': manicure,
                'name': 'Manicura en Gel',
                'price': 25.00,
                'description': 'Esmaltado semipermanente que dura hasta 3 semanas con acabado brillante y resistente.',
                'image': 'core/services/gel.jpeg'
            },
            {
                'service_type': manicure,
                'name': 'Uñas Acrílicas',
                'price': 30.00,
                'description': 'Extensiones y esculpido de uñas con acrílico. Diseños personalizados según tus preferencias.',
                'image': 'core/services/acrilicas.jpeg'
            },
            {
                'service_type': manicure,
                'name': 'Nail Art & Diseño',
                'price': 20.00,
                'description': 'Diseños artísticos a mano alzada, pedrería, efectos cromo y decoraciones exclusivas.',
                'image': 'core/services/uñas3.jpeg'
            },
            {
                'service_type': pedicure,
                'name': 'Pedicure Spa',
                'price': 15.00,
                'description': 'Limado, exfoliación, tratamiento de cutículas, esmaltado y masaje relajante de pies.',
                'image': 'core/services/pedicure.jpeg'
            },
            {
                'service_type': maquillaje,
                'name': 'Maquillaje Social',
                'price': 35.00,
                'description': 'Maquillaje profesional elegante y natural para cualquier evento u ocasión social.',
                'image': 'core/services/maquillaje1.jpeg'
            },
            {
                'service_type': maquillaje,
                'name': 'Maquillaje de Noche',
                'price': 40.00,
                'description': 'Maquillaje glamoroso de alta cobertura con pestañas postizas y fijación prolongada.',
                'image': 'core/services/maquillaje.jpeg'
            },
            {
                'service_type': maquillaje,
                'name': 'Maquillaje para Novias',
                'price': 60.00,
                'description': 'Maquillaje exclusivo de larga duración para novias y graduaciones con prueba previa.',
                'image': 'core/services/maquillaje2.jpeg'
            },
        ]
        for s_data in services_data:
            if s_data['service_type']:
                service, created = Service.objects.get_or_create(
                    name=s_data['name'],
                    defaults=s_data
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Servicio "{service.name}" creado.'))
                else:
                    self.stdout.write(self.style.WARNING(f'Servicio "{service.name}" ya existe.'))