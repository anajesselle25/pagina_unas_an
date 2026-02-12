from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.index, name='index'),
    path('index1/', views.index1, name='index1'),
    path('login/', views.login, name='login'),
    path('maquillaje/', ServiceListView.as_view(), name='maquillaje'),
    path('registro/', views.registro, name='registro'),
    path('reservacion/', views.reservacion , name='reservacion'),
    path('services/create/', ServiceCreateView.as_view(), name='service_create'),
    path('service/<int:id>/', ServiceDetailView.as_view(), name='service_detail'),
    path('service/<int:id>/update', ServiceUpdateView.as_view(), name='service_update'),
    path('services/<int:id>/delete', ServiceDeleteView.as_view(), name='service_delete'),
]