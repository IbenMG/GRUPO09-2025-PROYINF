from django.shortcuts import render, get_object_or_404,redirect
from django.conf import settings  # Asegúrate de importar settings
from .models import DocumentoPDF
from .forms import DocumentoPDFForm
from django.http import FileResponse, Http404
import os

# Vista para el index que muestra los PDFs
def index(request):
    return render(request, 'gestor_pdfs/index.html')  # Asegúrate de que el nombre coincide

# Agregar PDF (formulario)
def agregar_pdf(request):
    # Lógica para agregar un PDF
    pass

# Buscar PDF (formulario)
def buscar_pdf(request):
    # Lógica para buscar PDFs
    pass
def subir_pdf(request):
    if request.method == 'POST':
        form = DocumentoPDFForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('listar_pdfs')
    else:
        form = DocumentoPDFForm()
    return render(request, 'gestor_pdfs/subir_pdf.html', {'form': form})

def listar_pdfs(request):
    query = request.GET.get('q')
    if query:
        pdfs = DocumentoPDF.objects.filter(nombre__icontains=query)
    else:
        pdfs = DocumentoPDF.objects.all()
    return render(request, 'gestor_pdfs/listar_pdfs.html', {'pdfs': pdfs})

def descargar_pdf(request, pdf_id):
    documento = get_object_or_404(DocumentoPDF, id=pdf_id)
    file_path = os.path.join(settings.MEDIA_ROOT, documento.archivo.name)
    return FileResponse(open(file_path, 'rb'), content_type='application/pdf')

# Borrar PDF
def borrar_pdf(request, pdf_id):
    documento = get_object_or_404(DocumentoPDF, id=pdf_id)
    documento.delete()  # Eliminar el documento de la base de datos
    return redirect('index_pdf')  # Redirigir al índice después de borrar