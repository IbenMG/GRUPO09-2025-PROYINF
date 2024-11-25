from django.urls import path
from . import views

urlpatterns = [
    path('entrada_texto', views.process_text, name='entrada_texto'),
    path('listas/', views.lista_plantillas, name='lista_plantillas'),
    path('cargar/', views.cargar_archivo, name='cargar_archivo'),
    path('seleccionar/<int:archivo_id>/', views.seleccionar_plantilla, name='seleccionar_plantilla'),
    path('documento/<int:archivo_id>/', views.ver_documento, name='ver_documento'),
]
