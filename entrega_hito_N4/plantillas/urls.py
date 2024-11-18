from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_plantillas, name='index_plantillas'),
     path('cargar/', views.cargar_archivo, name='cargar_archivo'),
]
