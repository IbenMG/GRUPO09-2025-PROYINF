from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_pdfs, name='index_pdfs'),  # Vista principal del índice
    path('detalle/<int:pdf_id>/', views.detalle_pdf, name='detalle_pdf'),
    path('agregar/', views.agregar_pdf, name='agregar_pdf'),
    path('buscar/', views.buscar_pdf, name='buscar_pdf'),
    path('pdfs/modificar/<int:pk>/', views.modificar_pdf, name='modificar_pdf'),
    path('descargar/<int:pdf_id>/', views.descargar_pdf, name='descargar_pdf'),
    path('borrar/<int:pdf_id>/', views.borrar_pdf, name='confirmar_borrar'),  # Confirmación de borrado
]