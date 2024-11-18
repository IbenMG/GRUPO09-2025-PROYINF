from django.shortcuts import render
from .models import ArchivoEntrada
from .forms import ArchivoEntradaForm

def index_plantillas(request):
    return render(request, 'plantillas/index.html')

def lista_plantillas(request):
    # Lógica de ejemplo para mostrar una lista vacía o inicial
    return render(request, 'plantillas/lista_plantillas.html', {})

def cargar_archivo(request):
    if request.method == 'POST':
        form = ArchivoEntradaForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = form.save()
            # Aquí puedes procesar el archivo y extraer texto
            return render(request, 'plantillas/resultados.html', {'archivo': archivo})
    else:
        form = ArchivoEntradaForm()
    return render(request, 'plantillas/cargar.html', {'form': form})
