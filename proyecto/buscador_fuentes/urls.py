from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Ruta para la vista principal
    path('agregar_fuentes/', views.agregar_fuentes, name='agregar_fuentes'),
    path('buscar_fuentes/', views.buscar_fuentes, name='buscar_fuentes'),
    path('modificar_fuentes/', views.modificar_fuentes, name='modificar_fuentes'),
    path('borrar_fuentes/', views.borrar_fuentes, name='borrar_fuentes'),
    path('', views.vistas_fuentes, name='vistas_fuentes'),
]