from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.http import FileResponse, Http404
from .models import DocumentoPDF
from .forms import DocumentoPDFForm
from django.contrib import messages
from django.db.models import Q
import os

# Vista para el index que muestra los PDFs
def index_pdfs(request):
    pdfs = DocumentoPDF.objects.all()  # Obtener todos los PDFs
    return render(request, 'gestor_pdfs/index_pdfs.html', {'pdfs': pdfs})
# views.py
def detalle_pdf(request, pdf_id):
    documento = get_object_or_404(DocumentoPDF, id=pdf_id)
    return render(request, 'gestor_pdfs/detalle_pdf.html', {'documento': documento})

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
        pdfs = DocumentoPDF.objects.filter(Q(nombre__icontains=query) | Q(etiquetas__icontains=query))
    else:
        pdfs = DocumentoPDF.objects.all()
    return render(request, 'gestor_pdfs/buscar_pdf.html', {'pdfs': pdfs, 'query': query})

def descargar_pdf(request, pdf_id):
    documento = get_object_or_404(DocumentoPDF, id=pdf_id)
    file_path = os.path.join(settings.MEDIA_ROOT, documento.archivo.name)
    try:
        return FileResponse(open(file_path, 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404("Archivo no encontrado")

def borrar_pdf(request, pdf_id):
    documento = get_object_or_404(DocumentoPDF, id=pdf_id)
    if request.method == 'POST':
        documento.delete()
        messages.success(request, "El PDF ha sido eliminado con éxito.")
        return redirect('index_pdf')  # Redirige al índice tras borrar
    return render(request, 'gestor_pdfs/confirmar_borrar.html', {'documento': documento})
