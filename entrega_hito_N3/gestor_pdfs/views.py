from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.http import FileResponse, Http404
from .models import DocumentoPDF
from .forms import DocumentoPDFForm
from django.contrib import messages
import os

# Vista para el index que muestra los PDFs
def index(request):
    pdfs = DocumentoPDF.objects.all()  # Obtiene todos los PDFs de la base de datos
    return render(request, 'gestor_pdfs/index.html', {'pdfs': pdfs})

# Vista para agregar un nuevo PDF
def agregar_pdf(request):
    if request.method == 'POST':
        form = DocumentoPDFForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index_pdf')  # Redirige al índice después de agregar el PDF
    else:
        form = DocumentoPDFForm()
    return render(request, 'gestor_pdfs/agregar_pdf.html', {'form': form})

# Vista para buscar PDFs
def buscar_pdf(request):
    query = request.GET.get('q')
    if query:
        pdfs = DocumentoPDF.objects.filter(nombre__icontains=query)
    else:
        pdfs = DocumentoPDF.objects.all()
    return render(request, 'gestor_pdfs/buscar_pdf.html', {'pdfs': pdfs})

# Vista para descargar un PDF
def descargar_pdf(request, pdf_id):
    documento = get_object_or_404(DocumentoPDF, id=pdf_id)
    file_path = os.path.join(settings.MEDIA_ROOT, documento.archivo.name)
    try:
        return FileResponse(open(file_path, 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404("Archivo no encontrado")

# Vista para borrar un PDF
def borrar_pdf(request, pdf_id):
    documento = get_object_or_404(DocumentoPDF, id=pdf_id)
    documento.delete()  # Elimina el PDF de la base de datos
    return redirect('index_pdf')  # Redirige al índice después de borrar el PDF
