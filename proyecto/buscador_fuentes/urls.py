from django.urls import path
from . import views

urlpatterns = [
    path('', views.mi_vista, name='index'),  # Ruta para la vista principal
]