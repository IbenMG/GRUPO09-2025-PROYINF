from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index_pdf'),  # Página principal que muestra todos los PDFs
    path('agregar/', views.agregar_pdf, name='agregar_pdf'),  # Agregar PDF
    path('buscar/', views.buscar_pdf, name='buscar_pdf'),  # Buscar PDF
    path('descargar/<int:pdf_id>/', views.descargar_pdf, name='descargar_pdf'),  # Descargar PDF
    path('borrar/<int:pdf_id>/', views.borrar_pdf, name='borrar_pdf'),  # Borrar PDF
]