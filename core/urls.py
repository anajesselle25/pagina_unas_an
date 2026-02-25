from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.index, name='index'),
    path('index1/', views.index1, name='index1'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('maquillaje/', ServiceListView.as_view(), name='maquillaje'),
    path('registro/', UserRegisterView.as_view(), name='registro'),
    path('services/create/', ServiceCreateView.as_view(), name='service_create'),
    path('service/<int:id>/', ServiceDetailView.as_view(), name='service_detail'),
    path('service/<int:id>/update', ServiceUpdateView.as_view(), name='service_update'),
    path('services/<int:id>/delete', ServiceDeleteView.as_view(), name='service_delete'),
    path('reservacion/', ReservationCreateView.as_view() , name='reservacion'),
    path('reservacion/success/<int:reservation_id>', ReservationSuccessView.as_view() , name='reservacion_success'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
]